#!/usr/bin/env python3
"""Quality gate for newly submitted entries.

Reads the rows a pull request ADDS to README.md, looks each one up on GitHub,
and reports what the maintainer would otherwise have to check by hand: stars,
licence, last push, archived state, repo age, and whether the repository (or
the folder the entry links inside one) really holds an Agent Skill: a SKILL.md
whose YAML frontmatter has a `name` and a `description`.

An entry may link a repository (`https://github.com/org/repo`) or a folder in
one (`https://github.com/org/repo/tree/main/skills/foo`); a folder is searched
on the branch the URL names, a repository on its default branch.

Hard failures block the pull request. Soft warnings are printed for a human to
judge. Both land in the GitHub Actions step summary.

    python scripts/check_submission.py --base-ref origin/main

Set GITHUB_TOKEN to raise the API rate limit from 60 to 5000 requests/hour.
"""

from __future__ import annotations

import argparse
import base64
import http.client
import json
import os
import posixpath
import re
import sys
import tomllib
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

import check_new_links
import gitref
import validate

API = "https://api.github.com"

# Tunables. These encode the quality bar in CONTRIBUTING.md.
#
# There is deliberately no star or repo-age minimum. Anyone may submit their own
# skill, including a brand-new one with no traction. What is checked is whether
# the thing is real: a SKILL.md an agent can load, a licence, documentation, and
# recent activity. Stars measure popularity, which is a different question.
MAX_ENTRIES_PER_PR = 1
STALE_DAYS = 180
OVERRIDE_LABEL = "maintainer-override"

# How many SKILL.md files are read, shallowest first, looking for one with a
# name and a description. A collection can hold hundreds; one good one is the bar.
MAX_SKILL_FILES = 5

# Limits from the Agent Skills specification (https://agentskills.io/specification).
# Breaking them is reported for a maintainer, not blocked: agents still load such
# a skill, and the list's rule is only that the two fields exist.
MAX_NAME = 64
MAX_SKILL_DESC = 1024
SKILL_NAME_RE = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")

# Package manifests that can carry a licence declaration. CONTRIBUTING.md accepts
# one of these when there is no LICENSE file at the root, because GitHub's licence
# API only reads the root file and so reports such a project as unlicensed.
MANIFEST_LICENCE_FILES = (
    "package.json",
    "pyproject.toml",
    "Cargo.toml",
    "pom.xml",
    "composer.json",
    "deno.json",
)

# Values that fill the licence field without granting open-source terms. npm
# documents `UNLICENSED` for a package that is deliberately not open source and
# `SEE LICENSE IN <file>` for terms the API cannot read. `Unlicense` -- the
# public-domain dedication -- is a real licence and is deliberately not here.
NOT_OPEN_SOURCE = {
    "unlicensed",
    "proprietary",
    "commercial",
    "closed",
    "closed-source",
    "none",
    "noassertion",
}
NOT_OPEN_SOURCE_PREFIXES = ("see license in", "see licence in")

# A SKILL.md `license` value that points at a bundled file rather than naming a
# licence, which the specification allows: `Complete terms in LICENSE.txt`.
# The file beside the skill is then the evidence, not the value.
LICENCE_POINTER_RE = re.compile(
    r"^(?:see licen[cs]e in|complete terms in)\b|^[\w.-]*licen[cs]e[\w.-]*$",
    re.IGNORECASE,
)

# A licence file somewhere other than the repository root, which GitHub's licence
# API does not read: `LICENSE`, `LICENSE.txt`, `LICENCE.md`, `COPYING`.
LICENCE_FILE_RE = re.compile(r"(?:licen[cs]e|copying)(?:[.-][\w.-]+)?", re.IGNORECASE)

# Maven has no JSON or TOML form to parse, so this one manifest stays a regex.
# The captured group is deliberately `[^<]*` with no surrounding `\s*`: pairing a
# lazy quantifier with whitespace classes that can match the same characters is
# what makes a pattern backtrack super-linearly. Trimming happens in Python.
POM_LICENCE_RE = re.compile(
    r"<licenses?>.*?<name>([^<]*)</name>", re.DOTALL | re.IGNORECASE
)

# Re-exported so the pattern has one definition for all three gate scripts.
REF_RE = gitref.REF_RE

# Words in a README that say how to install or use what it documents.
USAGE_RE = re.compile(
    r"\b(?:install(?:ation|ing)?|usage|getting started|quick ?start|set ?up|how to use)\b",
    re.IGNORECASE,
)

ROW_RE = re.compile(
    r"^\|\s*\[(?P<name>[^\]]+)\]\((?P<url>[^)\s]+)\)\s*\|(?P<rest>.*)\|\s*$"
)
# A repository, or a folder in one. The ref is one path segment, which covers
# `main`, `master` and tags; a branch name with a slash reads as ref plus folder,
# and the tree lookup then fails soft for a maintainer to read.
GH_URL_RE = re.compile(
    r"^https://github\.com/(?P<owner>[\w.-]+)/(?P<repo>[\w.-]+)"
    r"(?:/tree/(?P<ref>[\w.-]+)(?P<folder>(?:/[^/?#\s]+)*))?/?$"
)

# YAML frontmatter keys this parser reads: `key:` at column 0, then the value.
FRONTMATTER_KEY_RE = re.compile(r"^(?P<key>[A-Za-z0-9_-]+):(?:[ \t](?P<value>.*))?$")
BLOCK_SCALAR_RE = re.compile(r"^[|>][+-]?[0-9]?$")


@dataclass
class Submission:
    name: str
    url: str
    desc: str
    third: str
    hard: list = field(default_factory=list)
    soft: list = field(default_factory=list)
    facts: dict = field(default_factory=dict)


@dataclass(frozen=True)
class Target:
    """Where an entry's URL points: a repository, or a folder inside one."""

    owner: str
    repo: str
    ref: str  # "" means the repository's default branch
    folder: str  # "" means the repository root

    @property
    def slug(self) -> str:
        return f"{self.owner}/{self.repo}"


@dataclass
class Skill:
    """One SKILL.md with the two frontmatter fields every skill needs."""

    path: str
    fields: dict
    # keys whose value is a plain scalar holding `: `, which strict YAML rejects
    risky: set = field(default_factory=set)


@dataclass
class Search:
    """What a look through a repository's tree for SKILL.md files found."""

    paths: list = field(default_factory=list)  # every file under the folder
    candidates: list = field(default_factory=list)  # SKILL.md paths, shallowest first
    skill: Skill | None = None
    rejected: list = field(
        default_factory=list
    )  # read, but lacking name or description
    error: str | None = None  # why the tree could not be read
    truncated: bool = False
    folder_found: bool = True


def gh_api(path: str):
    req = urllib.request.Request(
        f"{API}/{path}",
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "awesome-skills-submission-check",
        },
    )
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8")), None
    except urllib.error.HTTPError as exc:
        return None, exc.code
    # OSError covers URLError, timeouts and a dropped connection, which used to
    # escape as RemoteDisconnected and crash the run.
    except (OSError, http.client.HTTPException) as exc:
        return None, f"network: {exc}"


def seg(value: object) -> str:
    """One URL path segment, with anything that could end or climb it escaped."""
    return urllib.parse.quote(str(value), safe="")


def quote_path(path: str) -> str:
    """A repository path for an API URL, each segment escaped on its own."""
    return "/".join(seg(part) for part in path.split("/"))


def parse_github_url(url: str) -> Target | None:
    """The repository and folder a GitHub URL names, or None for any other URL.

    The folder becomes part of API paths, so a `.` or `..` segment is refused
    rather than handed on, and each segment is escaped where it is used.
    """
    m = GH_URL_RE.match(url)
    if not m:
        return None
    parts = [urllib.parse.unquote(p) for p in (m.group("folder") or "").split("/") if p]
    if any(p in (".", "..") or "/" in p for p in parts):
        return None
    return Target(
        m.group("owner"), m.group("repo"), m.group("ref") or "", "/".join(parts)
    )


def is_open_source(licence: str) -> bool:
    """False for a licence field that names no open-source terms.

    The field being filled in is not the same as the terms being open source:
    `UNLICENSED` is npm's documented marker for a package that is explicitly not,
    and the Agent Skills specification's own example is
    `Proprietary. LICENSE.txt has complete terms`, so the first word counts too.
    """
    value = licence.strip().lower()
    if value in NOT_OPEN_SOURCE:
        return False
    first = re.split(r"[\s.,;:()]+", value, maxsplit=1)[0]
    if first in NOT_OPEN_SOURCE:
        return False
    return not value.startswith(NOT_OPEN_SOURCE_PREFIXES)


def is_licence_pointer(value: str) -> bool:
    """True for a SKILL.md `license` that names a bundled file, not a licence."""
    return bool(LICENCE_POINTER_RE.search(value.strip()))


def _first_licence_string(value) -> str | None:
    """Pull a licence name out of the shapes the manifest formats allow.

    A plain string, npm's legacy `{"type": "MIT"}` object, a composer array, or
    PEP 621's `{text = "MIT"}` table. A `{file = ...}` or `license-file` pointer
    names no terms, so it is not treated as a declaration.
    """
    if isinstance(value, str):
        return value.strip() or None
    if isinstance(value, dict):
        for key in ("type", "text"):
            found = _first_licence_string(value.get(key))
            if found:
                return found
        return None
    if isinstance(value, list):
        for item in value:
            found = _first_licence_string(item)
            if found:
                return found
    return None


def _licence_from_json(text: str) -> str | None:
    data = json.loads(text)
    if not isinstance(data, dict):
        return None
    return _first_licence_string(data.get("license") or data.get("licenses"))


def _licence_from_toml(text: str) -> str | None:
    data = tomllib.loads(text)
    # `[project]` is PEP 621, `[package]` is Cargo.
    for table in ("project", "package"):
        section = data.get(table)
        if isinstance(section, dict):
            found = _first_licence_string(section.get("license"))
            if found:
                return found
    return None


def _licence_from_pom(text: str) -> str | None:
    match = POM_LICENCE_RE.search(text)
    return match.group(1).strip() if match else None


MANIFEST_READERS = (
    (".json", _licence_from_json),
    (".toml", _licence_from_toml),
    (".xml", _licence_from_pom),
)


def parse_manifest_licence(filename: str, text: str) -> str | None:
    """Read the declared licence out of one manifest, or None.

    Parsed rather than pattern-matched: a regex over the raw text reads a nested
    `"license"` key belonging to some other object as the package's own.
    """
    name = filename.lower()
    try:
        for suffix, reader in MANIFEST_READERS:
            if name.endswith(suffix):
                return reader(text)
    except (json.JSONDecodeError, tomllib.TOMLDecodeError, UnicodeDecodeError):
        return None
    return None


def manifest_licence(slug: str) -> tuple[str | None, str | None]:
    """Return (manifest filename, licence) for the first manifest that declares one.

    GitHub's licence endpoint only looks at a `LICENSE` file in the repository
    root, so a project that declares its licence in `package.json` or
    `pyproject.toml` reports as having none at all. CONTRIBUTING.md accepts a
    manifest declaration, so look for one before blocking a submission.
    """
    for name in MANIFEST_LICENCE_FILES:
        text = file_text(f"repos/{slug}/contents/{name}")
        licence = parse_manifest_licence(name, text) if text else None
        if licence:
            return name, licence
    return None, None


def file_text(path: str) -> str | None:
    """Decode a file from the contents API, or None when there is no such file."""
    data, _ = gh_api(path)
    if not isinstance(data, dict) or not data.get("content"):
        return None
    try:
        return base64.b64decode(data["content"]).decode("utf-8", "replace")
    except ValueError:
        return None


def _unquote(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] == "'":
        return value[1:-1].replace("''", "'")
    if len(value) >= 2 and value[0] == value[-1] == '"':
        return value[1:-1].replace('\\"', '"')
    return value


def _scalar(value: str, block: list[str]) -> tuple[str, bool]:
    """Return (text, is a plain scalar) for one frontmatter value.

    Covers the shapes SKILL.md files use: a plain or quoted value on the key's
    line, a folded (`>`) or literal (`|`) block, and a plain value continued
    on indented lines. Anything more exotic still yields some non-empty text,
    which is all the gate needs to know.
    """
    if BLOCK_SCALAR_RE.match(value):
        joiner = "\n" if value.startswith("|") else " "
        return joiner.join(line for line in block if line).strip(), False
    text = " ".join([value, *(line for line in block if line)]).strip()
    if text[:1] in ("'", '"'):
        return _unquote(text), False
    # ` #` starts a comment in a plain scalar
    return text.split(" #", 1)[0].strip(), True


def parse_frontmatter(text: str) -> tuple[dict, set] | None:
    """Top-level keys of a SKILL.md's YAML frontmatter, or None if it has none.

    Returns (fields, risky): `risky` names the keys whose plain value holds `: `,
    which a strict YAML parser rejects as a nested mapping and a lenient one
    truncates. Stdlib only, so this reads the subset of YAML that frontmatter
    uses rather than all of it; nested mappings such as `metadata:` come back as
    flattened text, which nothing here reads.
    """
    lines = text.lstrip("\ufeff").splitlines()
    while lines and not lines[0].strip():
        lines.pop(0)
    if not lines or lines[0].strip() != "---":
        return None
    try:
        end = next(
            i for i in range(1, len(lines)) if lines[i].strip() in ("---", "...")
        )
    except StopIteration:
        return None

    fields: dict = {}
    risky: set = set()
    i = 1
    while i < end:
        m = FRONTMATTER_KEY_RE.match(lines[i])
        i += 1
        if not m:
            continue
        block = []
        while i < end and (lines[i][:1] in (" ", "\t") or not lines[i].strip()):
            block.append(lines[i].strip())
            i += 1
        value, plain = _scalar((m.group("value") or "").strip(), block)
        key = m.group("key")
        fields[key] = value
        if plain and ": " in value:
            risky.add(key)
    return fields, risky


def parse_rows(text: str) -> dict:
    """Map normalised URL to Submission for every table row in a README."""
    rows = {}
    for line in text.splitlines():
        m = ROW_RE.match(line)
        if not m:
            continue
        cells = [c.strip() for c in m.group("rest").split("|")]
        url = m.group("url").strip()
        key = re.sub(r"^https?://(www\.)?", "", url.rstrip("/")).lower()
        rows[key] = Submission(
            name=m.group("name").strip(),
            url=url,
            desc=cells[0] if cells else "",
            third=cells[1] if len(cells) > 1 else "",
        )
    return rows


def base_readme(base_ref: str) -> str | None:
    """README.md at `base_ref`, or None when the ref is malformed or unreadable.

    `base_ref` arrives from a command line, so it is checked against the shape of
    a git ref first. Nothing is run through a shell, but a value beginning with
    `-` would still be read by git as an option rather than a revision.
    """
    if not gitref.is_valid_ref(base_ref):
        print(
            f"error: {base_ref!r} is not a valid git ref for --base-ref",
            file=sys.stderr,
        )
        return None

    text, detail = gitref.show(base_ref, "README.md")
    if text is None:
        print(
            f"warning: could not read README.md at {base_ref}: {detail}",
            file=sys.stderr,
        )
    return text


def added_rows(base_ref: str) -> list:
    """Entries present at HEAD but not at the base.

    Compares the two parsed entry sets rather than reading `+` lines from the
    diff. Reordering a table rewrites every moved row, so a diff-based reading
    reports untouched entries as new submissions and then blocks the pull
    request over rot that was already on the base branch.
    """
    text = base_readme(base_ref)
    if text is None:
        return []
    before = parse_rows(text)
    after = parse_rows(Path("README.md").read_text(encoding="utf-8"))
    return [sub for key, sub in after.items() if key not in before]


def added_links(base_ref: str, rows: list) -> list:
    """Links new to README.md that are not one of `rows`, each held for a maintainer.

    Only a skill table row is checked for a SKILL.md and a licence. Any other
    new link, such as a bullet in Official or Tools (a vendor repository, a tool
    or an article), a bullet with another list marker, a link in prose, or a row
    the table parser cannot read, used to pass as "No new entries" and merge
    itself, so CONTRIBUTING.md has a maintainer add those.
    """
    text = base_readme(base_ref)
    if text is None:
        return []
    known = {validate.normalize_url(u) for u in check_new_links.links_in(text)}
    known |= {validate.normalize_url(s.url) for s in rows}
    head = check_new_links.links_in(Path("README.md").read_text(encoding="utf-8"))
    held = []
    for url in sorted(head):
        if validate.normalize_url(url) in known:
            continue
        sub = Submission(url, url, "", "")
        sub.hard.append(
            "Adds a link outside the skill tables (a bullet, a link in prose, or a "
            "row the table check cannot read), which the gate does not check for a "
            f"SKILL.md or a licence. A maintainer reviews it and applies "
            f"`{OVERRIDE_LABEL}` to merge it."
        )
        held.append(sub)
    return held


def inspect(sub: Submission) -> None:
    target = parse_github_url(sub.url)
    if target is None:
        # Blocking, not a note: a note never stops auto-merge, so the entry would
        # land with no SKILL.md, licence or activity check at all.
        sub.hard.append(
            "Not a GitHub repository or folder URL, so it cannot be checked for a "
            "SKILL.md, a licence or recent activity. A maintainer checks it by hand "
            f"and applies `{OVERRIDE_LABEL}` to merge it."
        )
        return

    data = lookup_repo(sub, target.slug)
    if data is None:
        return

    stale_days = days_since(data["pushed_at"])
    if stale_days > STALE_DAYS:
        sub.hard.append(
            f"Last push was {stale_days} days ago, over the {STALE_DAYS}-day "
            f"maintenance threshold."
        )

    ref = target.ref or data.get("default_branch") or "main"
    search = find_skill(target.slug, ref, target.folder)
    report_skill(sub, target, ref, search)
    if search.error is None and not search.folder_found and not search.truncated:
        return  # a folder that is not there has no licence or README to judge
    check_licence(sub, target.slug, data, search)
    check_readme(sub, target.slug, ref, target.folder)

    # Star count and repo age are reported in the facts table above as context.
    # Neither is a bar: popularity is not quality, and a new skill that works,
    # is licensed and is documented belongs on the list as much as a famous one.


def days_since(stamp: str) -> int:
    then = datetime.fromisoformat(stamp.replace("Z", "+00:00"))
    return (datetime.now(timezone.utc) - then).days


def lookup_repo(sub: Submission, slug: str) -> dict | None:
    """Fetch a repository, record its facts, and block what no entry may be.

    Returns None when there is nothing further to inspect.
    """
    data, err = gh_api(f"repos/{slug}")
    if data is None:
        if err == 404:
            sub.hard.append(
                f"`{slug}` returns 404. The repository is private, renamed, or deleted."
            )
        else:
            # A failed lookup verified nothing, so it fails closed.
            sub.hard.append(
                f"Could not reach the GitHub API for `{slug}` ({err}), so nothing "
                f"about this entry was verified. Re-run the check."
            )
        return None

    stale_days = days_since(data["pushed_at"])
    age_days = days_since(data["created_at"])
    licence = (data.get("license") or {}).get("spdx_id")
    stars = data["stargazers_count"]

    sub.facts = {
        "repo": slug,
        "stars": stars,
        "license": licence or "none",
        "last push": f"{data['pushed_at'][:10]} ({stale_days}d ago)",
        "created": f"{data['created_at'][:10]} ({age_days}d old)",
        "archived": data["archived"],
        "fork": data["fork"],
        "language": data.get("language") or "unknown",
    }

    if data["archived"]:
        sub.hard.append(
            "The repository is archived. Archived projects are not accepted."
        )
    if data["fork"]:
        sub.hard.append(
            "The repository is a fork. Submit the upstream project instead."
        )
    return data


def find_skill(slug: str, ref: str, folder: str) -> Search:
    """Look under `folder` at `ref` for a SKILL.md with a name and a description.

    One recursive tree listing finds every SKILL.md, then the shallowest few are
    read until one has both fields. A skill at the folder's root is the common
    case; a collection holds them a level or two down.
    """
    search = Search()
    tree, err = gh_api(f"repos/{slug}/git/trees/{seg(ref)}?recursive=1")
    if not isinstance(tree, dict) or not isinstance(tree.get("tree"), list):
        search.error = str(err or "no tree in the response")
        return search

    prefix = f"{folder}/" if folder else ""
    search.truncated = bool(tree.get("truncated"))
    search.paths = [
        e["path"]
        for e in tree["tree"]
        if e.get("type") == "blob" and e.get("path", "").startswith(prefix)
    ]
    search.folder_found = not folder or bool(search.paths)
    search.candidates = sorted(
        (p for p in search.paths if posixpath.basename(p) == "SKILL.md"),
        key=lambda p: (p.count("/"), p),
    )
    for path in search.candidates[:MAX_SKILL_FILES]:
        text = file_text(f"repos/{slug}/contents/{quote_path(path)}?ref={seg(ref)}")
        parsed = parse_frontmatter(text) if text else None
        fields, risky = parsed or ({}, set())
        if fields.get("name") and fields.get("description"):
            search.skill = Skill(path, fields, risky)
            return search
        search.rejected.append(path)
    return search


def report_skill(sub: Submission, target: Target, ref: str, search: Search) -> None:
    """Turn what find_skill saw into facts and findings."""
    where = (
        f"`{target.folder}` on `{ref}`"
        if target.folder
        else f"the repository on `{ref}`"
    )
    if search.error:
        sub.hard.append(
            f"Could not list the repository tree at {where} ({search.error}), so "
            f"the SKILL.md was not verified. A branch name with a slash reads as "
            f"part of the folder: link a one-segment ref, or re-run the check."
        )
        return
    if not search.folder_found and not search.truncated:
        sub.hard.append(
            f"The URL names the folder `{target.folder}`, which is not in the "
            f"repository at `{ref}`. Link a folder that exists, or the repository."
        )
        return

    sub.facts["SKILL.md files"] = len(search.candidates)
    if search.skill is None:
        if not search.candidates and search.truncated:
            sub.hard.append(
                "The repository tree is too large for one listing and no SKILL.md "
                "was in the part GitHub returned, so it was not verified. A "
                f"maintainer checks it by hand and applies `{OVERRIDE_LABEL}`."
            )
        elif not search.candidates:
            sub.hard.append(
                f"No SKILL.md under {where}. An entry must link a skill: a folder "
                f"whose SKILL.md has YAML frontmatter with `name` and `description`."
            )
        else:
            read = ", ".join(f"`{p}`" for p in search.rejected)
            sub.hard.append(
                f"None of the SKILL.md files read ({read}) starts with YAML "
                f"frontmatter that has both `name` and `description`."
            )
        return

    skill = search.skill
    sub.facts["skill"] = f"{skill.fields['name']} (`{skill.path}`)"
    check_spec(sub, target, skill)


def check_spec(sub: Submission, target: Target, skill: Skill) -> None:
    """Advisory notes where the skill strays from the Agent Skills specification."""
    name, desc = skill.fields["name"], skill.fields["description"]
    if len(name) > MAX_NAME or not SKILL_NAME_RE.fullmatch(name):
        sub.soft.append(
            f"`name: {name}` breaks the specification: at most {MAX_NAME} lowercase "
            f"letters, digits and single hyphens, with no hyphen at either end."
        )
    parent = posixpath.basename(posixpath.dirname(skill.path))
    if parent and parent != name:
        sub.soft.append(
            f"`name: {name}` does not match its folder `{parent}`, which the "
            f"specification requires."
        )
    if len(desc) > MAX_SKILL_DESC:
        sub.soft.append(
            f"The SKILL.md description is {len(desc)} characters; the specification "
            f"allows {MAX_SKILL_DESC}."
        )
    for key in sorted(skill.risky & {"name", "description"}):
        sub.soft.append(
            f"`{key}` in `{skill.path}` is an unquoted value containing `: `, which "
            f"a strict YAML parser rejects. Quote it or use a `>-` block."
        )


def check_licence(sub: Submission, slug: str, data: dict, search: Search) -> None:
    """Block a skill that withholds open-source terms, wherever it says so."""
    skill = search.skill
    declared = (skill.fields.get("license") or "").strip() if skill else ""
    if declared and not is_licence_pointer(declared) and not is_open_source(declared):
        sub.hard.append(
            f"`{skill.path}` declares `license: {declared}`, which says the terms "
            f"are not open source. CONTRIBUTING.md requires an open-source licence."
        )
        return

    licence = (data.get("license") or {}).get("spdx_id")
    if licence in (None, "", "NOASSERTION"):
        check_unclassified_licence(sub, slug, search)


def declared_licence(slug: str, search: Search) -> tuple:
    """(where, licence, kind) for a repository GitHub reports as unlicensed.

    `kind` is "manifest" for a package manifest at the root, "frontmatter" for a
    licence named in the skill's SKILL.md, and "file" for a licence file beside
    the skill, whose terms GitHub cannot classify outside the root. All three are
    None when the repository declares nothing anywhere. staleness_report.py calls
    this too, so the health report and the gate cannot disagree.
    """
    man_file, man_lic = manifest_licence(slug)
    if man_lic:
        return man_file, man_lic, "manifest"
    skill = search.skill
    declared = (skill.fields.get("license") or "").strip() if skill else ""
    if declared and not is_licence_pointer(declared):
        return skill.path, declared, "frontmatter"
    found = licence_file(search)
    if found:
        return found, posixpath.basename(found), "file"
    return None, None, None


def licence_file(search: Search) -> str | None:
    """A licence file in the skill's folder or a folder above it, below the root."""
    if search.skill is None:
        return None
    files = set(search.paths)
    folder = posixpath.dirname(search.skill.path)
    while folder:
        for path in sorted(files):
            if posixpath.dirname(path) == folder and LICENCE_FILE_RE.fullmatch(
                posixpath.basename(path)
            ):
                return path
        folder = posixpath.dirname(folder)
    return None


def check_unclassified_licence(sub: Submission, slug: str, search: Search) -> None:
    """Resolve a licence GitHub could not classify, or block if there is none.

    "NOASSERTION" means GitHub found a licence file it could not classify, which
    is a different thing from having none. Only a genuinely absent licence blocks.
    """
    lic_file, lic_err = gh_api(f"repos/{slug}/license")
    if isinstance(lic_file, dict) and lic_file.get("name"):
        sub.facts["license"] = f"{lic_file['name']} (unrecognised by GitHub)"
        sub.soft.append(
            f"GitHub cannot classify `{lic_file['name']}`, so it reports no SPDX "
            f"licence. Confirm by hand that the terms are open source. Common for "
            f"a vendor repo with a customised header, suspicious for a small one."
        )
        return

    where, licence, kind = declared_licence(slug, search)
    if kind is None:
        sub.hard.append(
            f"No licence anywhere ({lic_err}): no `LICENSE` file at the root or "
            f"beside the skill, no licence field in a package manifest, and no "
            f"`license` in SKILL.md. CONTRIBUTING.md requires a clearly stated licence."
        )
        return

    if kind == "file":
        sub.facts["license"] = f"`{where}` (outside the root, unclassified)"
        sub.soft.append(
            f"No `LICENSE` file at the repository root; the skill has `{where}` "
            f"beside it. CONTRIBUTING.md accepts that, but GitHub only classifies "
            f"the root file. Confirm by hand that the terms are open source."
        )
        return

    sub.facts["license"] = f"{licence} (declared in {where})"
    if not is_open_source(licence):
        sub.hard.append(
            f"`{where}` declares `{licence}`, which states that the terms are not "
            f"open source rather than naming a licence. CONTRIBUTING.md requires an "
            f"open-source licence."
        )
        return
    sub.soft.append(
        f"No `LICENSE` file at the repository root; the licence is declared as "
        f"`{licence}` in `{where}`. CONTRIBUTING.md accepts that, but a root "
        f"`LICENSE` file is what GitHub reads. Confirm the terms."
    )


def check_readme(sub: Submission, slug: str, ref: str, folder: str) -> None:
    """A README in the linked folder, or else at the root, that says how to use it."""
    text = None
    if folder:
        text = file_text(f"repos/{slug}/readme/{quote_path(folder)}?ref={seg(ref)}")
    if text is None:
        text = file_text(f"repos/{slug}/readme?ref={seg(ref)}")
    if text is None:
        sub.hard.append(
            "No README in the linked folder or at the repository root. "
            "CONTRIBUTING.md requires one that says how to install or use the skill."
        )
        return
    if not USAGE_RE.search(text):
        sub.soft.append(
            "The README never mentions installing, setting up or using the skill. "
            "Confirm by hand that a reader could follow it."
        )


def render(subs: list, override: bool) -> tuple[str, bool]:
    lines = ["## Submission check", ""]
    hard_total = sum(len(s.hard) for s in subs)

    if not subs:
        lines.append("No new entries detected in `README.md`. Nothing to check.")
        return "\n".join(lines) + "\n", False

    count = len(subs)
    lines.append(f"Found **{count}** new entr{'y' if count == 1 else 'ies'}.")
    lines.append("")

    # Adding several entries at once is a process preference, not a defect in the
    # entries. It is surfaced for the maintainer and never fails the build: a
    # contributor whose entries are all fine should not see a red check.
    if count > MAX_ENTRIES_PER_PR:
        lines.append("> [!NOTE]")
        lines.append(
            f"> This adds {count} entries. CONTRIBUTING.md prefers one skill per "
            f"pull request, so each can be reviewed and reverted on its own. That is "
            f"a preference, not a requirement, and it does not fail this check -- a "
            f"maintainer may still ask you to split it."
        )
        lines.append("")

    for s in subs:
        lines.extend(render_submission(s))

    # Only a real defect in a submitted entry fails the check.
    failing = hard_total > 0 and not override
    lines.append(render_result(subs, hard_total, override, failing))

    return "\n".join(lines) + "\n", failing


def render_submission(s: Submission) -> list:
    """The per-entry block: facts table, then blocking and advisory findings."""
    lines = [f"### {s.name}", f"{s.url}", ""]
    if s.facts:
        lines.append("| Check | Value |")
        lines.append("|-------|-------|")
        lines.extend(f"| {k} | {v} |" for k, v in s.facts.items())
        lines.append("")
    if s.hard:
        lines.append("**Blocking:**")
        lines.extend(f"- {h}" for h in s.hard)
        lines.append("")
    if s.soft:
        lines.append("**Needs a maintainer decision:**")
        lines.extend(f"- {w}" for w in s.soft)
        lines.append("")
    if not s.hard and not s.soft:
        lines.append("Passes every automated check.")
        lines.append("")
    return lines


def render_result(subs: list, hard_total: int, override: bool, failing: bool) -> str:
    if override:
        return f"Gate bypassed by the `{OVERRIDE_LABEL}` label."
    if not failing:
        return "**Result: passed.** No blocking problems."
    entries = "entry" if len(subs) == 1 else "entries"
    return (
        f"**Result: blocked.** {hard_total} blocking problem(s) across "
        f"{len(subs)} {entries}. Fix those, or a maintainer can add the "
        f"`{OVERRIDE_LABEL}` label to merge anyway."
    )


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--base-ref", default="origin/main", help="ref to diff against")
    ap.add_argument("--labels", default="", help="comma-separated pull request labels")
    args = ap.parse_args()

    subs = added_rows(args.base_ref)
    for s in subs:
        inspect(s)
    subs += added_links(args.base_ref, subs)

    override = OVERRIDE_LABEL in {label.strip() for label in args.labels.split(",")}
    report, failing = render(subs, override)

    print(report)
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with Path(summary).open("a", encoding="utf-8") as fh:
            fh.write(report)

    return 1 if failing else 0


if __name__ == "__main__":
    sys.exit(main())
