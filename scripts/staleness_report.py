#!/usr/bin/env python3
"""Health report for every GitHub repository on the list.

Groups entries into what needs action: gone (404), moved, archived, unlicensed,
and stale. Written to be run on a schedule and piped into a single tracking
issue, so the report replaces itself instead of accumulating noise.

    python scripts/staleness_report.py > report.md

Set GITHUB_TOKEN to raise the API rate limit from 60 to 5000 requests/hour.
"""

from __future__ import annotations

import json
import os
import re
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

# Same directory, so this resolves when the script is run as `python
# scripts/staleness_report.py`. The licence rule lives in one place: a report that
# judged a licence declared outside the root differently from the submission gate
# would send the maintainer after entries the gate accepts.
from check_submission import (
    declared_licence,
    find_skill,
    is_open_source,
    parse_github_url,
)

README = Path(__file__).resolve().parent.parent / "README.md"
API = "https://api.github.com/graphql"
STALE_DAYS = 180
BATCH = 50

# Matches an entry link to github.com. The rest of the URL is kept, so an entry
# that points into a folder -- `.../anthropics/skills/tree/main/skills/pdf` --
# resolves to its repository for the API and keeps its folder for the licence
# lookup. In the sister list, requiring a bare `owner/repo)` left 11 of the
# repositories behind the list unchecked.
ENTRY_RE = re.compile(
    r"\[(?P<name>[^\]]+)\]\((?P<url>https://github\.com/(?P<owner>[\w.-]+)/(?P<repo>[\w.-]+)(?:/[^)\s]*)?)\)"
)

# This repository's own links (the issue links, the badge) are not entries.
SELF_SLUG = "sagargupta16/awesome-skills"


def graphql(query: str):
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        sys.exit("error: GITHUB_TOKEN is required for the GraphQL API")
    req = urllib.request.Request(
        API,
        data=json.dumps({"query": query}).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "awesome-skills-staleness",
        },
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def collect(readme: Path = README):
    """Return (name, owner, repo, section, url) for every GitHub entry, deduplicated.

    Two folders in one repository are two entries, so the key is the URL.
    """
    section = None
    seen = set()
    out = []
    for line in readme.read_text(encoding="utf-8").splitlines():
        # One fixed whitespace character, not `\s+`: `.` matches whitespace too,
        # so `\s+(.*)` overlaps and backtracks super-linearly. Strip in Python.
        m = re.match(r"^#{2,3}\s(.*)$", line)
        if m:
            section = m.group(1).strip()
            continue
        for e in ENTRY_RE.finditer(line):
            slug = f"{e.group('owner')}/{e.group('repo')}"
            key = e.group("url").rstrip("/").lower()
            if slug.lower() == SELF_SLUG or key in seen:
                continue
            seen.add(key)
            out.append(
                (
                    e.group("name"),
                    e.group("owner"),
                    e.group("repo"),
                    section or "?",
                    e.group("url"),
                )
            )
    return out


def fetch(entries):
    results = {}
    for start in range(0, len(entries), BATCH):
        chunk = entries[start : start + BATCH]
        parts = [
            f'r{i}: repository(owner: "{entry[1]}", name: "{entry[2]}") '
            f"{{ nameWithOwner stargazerCount pushedAt isArchived defaultBranchRef {{ name }} licenseInfo {{ spdxId }} }}"
            for i, entry in enumerate(chunk)
        ]
        data = graphql("query{" + " ".join(parts) + "}")
        # A repository that no longer exists answers NOT_FOUND on its own alias,
        # which is what "gone" means. Any other error (a rate limit, a timeout)
        # means the batch went unanswered, and reading its empty aliases as gone
        # would tell the maintainer to delete live entries, so stop instead.
        failed = [e for e in data.get("errors") or [] if e.get("type") != "NOT_FOUND"]
        if failed or data.get("data") is None:
            first = (failed or [{}])[0]
            sys.exit(
                f"error: GitHub GraphQL did not answer the batch: "
                f"{first.get('type')} {first.get('message')}"
            )
        payload = data["data"]
        for i, entry in enumerate(chunk):
            results[entry] = payload.get(f"r{i}")
    return results


def classify(results, now) -> dict:
    """Sort the API results into the buckets the report is organised around."""
    buckets = {"gone": [], "archived": [], "stale": [], "moved": [], "no_licence": []}
    for entry, info in results.items():
        name, owner, repo, section, url = entry
        slug = f"{owner}/{repo}"
        if info is None:
            buckets["gone"].append((name, slug, section))
            continue
        # GitHub serves a renamed or transferred repository over a redirect, so the
        # listed URL keeps working right up until someone claims the old name.
        if info["nameWithOwner"].lower() != slug.lower():
            buckets["moved"].append((name, slug, info["nameWithOwner"], section))
        pushed = datetime.fromisoformat(info["pushedAt"].replace("Z", "+00:00"))
        days = (now - pushed).days
        licence = (info.get("licenseInfo") or {}).get("spdxId")
        if info["isArchived"]:
            buckets["archived"].append((name, slug, section, days))
        if licence in (None, "", "NOASSERTION"):
            branch = (info.get("defaultBranchRef") or {}).get("name") or "main"
            buckets["no_licence"].append(
                (
                    name,
                    slug,
                    section,
                    licence or "none",
                    info["stargazerCount"],
                    url,
                    branch,
                )
            )
        if days > STALE_DAYS and not info["isArchived"]:
            buckets["stale"].append((days, name, slug, section, info["stargazerCount"]))
    return buckets


def resolve_declared_licences(no_root_licence) -> tuple[list, list]:
    """Split repositories with no root LICENSE into declared-elsewhere and unlicensed.

    GitHub reads the root `LICENSE` file only, so a skill that declares its
    licence in a package manifest, in its SKILL.md, or in a licence file beside
    it arrives here reporting `none`. CONTRIBUTING.md accepts all three, and the
    lookup is the submission gate's own, so the two cannot disagree.
    """
    declared, unlicensed = [], []
    for name, slug, section, licence, stars, url, branch in no_root_licence:
        if licence != "none":
            unlicensed.append((name, slug, section, licence, stars))
            continue
        target = parse_github_url(url)
        folder = target.folder if target else ""
        ref = (target.ref if target else "") or branch
        where, value, kind = declared_licence(slug, find_skill(slug, ref, folder))
        if kind == "file":
            declared.append((name, slug, section, "file, unclassified", where, stars))
        elif value and is_open_source(value):
            declared.append((name, slug, section, value, where, stars))
        elif value:
            unlicensed.append((name, slug, section, f"{value} in {where}", stars))
        else:
            unlicensed.append((name, slug, section, licence, stars))
    return declared, unlicensed


def section_block(
    title: str, intro: str, header: str, divider: str, rows: list
) -> list:
    """One report section, or nothing at all when the bucket is empty."""
    if not rows:
        return []
    return [f"## {title}", "", intro, "", header, divider, *rows, ""]


def main() -> int:
    entries = collect()
    results = fetch(entries)
    now = datetime.now(timezone.utc)

    buckets = classify(results, now)
    gone = buckets["gone"]
    archived = buckets["archived"]
    stale = buckets["stale"]
    moved = buckets["moved"]
    declared, unlicensed = resolve_declared_licences(buckets["no_licence"])

    checked = len(entries)
    out = [
        f"Automated health check of the {checked} GitHub entries in `README.md`. "
        f"Entries hosted elsewhere are covered only by the lychee link check in "
        f"`.github/workflows/lint.yml`.",
        "",
        f"- **{len(gone)}** gone (404 -- deleted or made private)",
        f"- **{len(moved)}** reachable only through a rename or transfer redirect",
        f"- **{len(archived)}** archived upstream",
        f"- **{len(unlicensed)}** with no licence the automated checks can find",
        f"- **{len(stale)}** not pushed in over {STALE_DAYS} days",
        f"- **{len(declared)}** licensed outside a root `LICENSE` file (a package "
        f"manifest, SKILL.md, or a licence file beside the skill), which "
        f"CONTRIBUTING.md accepts (listed for information, no action needed)",
        "",
        "This issue is rewritten in place on every run, so it always reflects the current state.",
        "",
    ]

    out += section_block(
        "Gone: remove these",
        "These URLs 404. Per CONTRIBUTING.md they should be removed.",
        "| Entry | Repo | Section |",
        "|-------|------|---------|",
        [f"| {n} | `{s}` | {sec} |" for n, s, sec in sorted(gone)],
    )

    out += section_block(
        "Moved: update the URL",
        "These resolve through a redirect, which only holds while the old name stays "
        "unclaimed. Rewrite the URL, and check the entry name and description too if "
        "the project was renamed rather than just transferred.",
        "| Entry | Listed as | Now | Section |",
        "|-------|-----------|-----|---------|",
        [
            f"| {n} | `{s}` | `{actual}` | {sec} |"
            for n, s, actual, sec in sorted(moved)
        ],
    )

    out += section_block(
        "Archived upstream",
        "The maintainer has archived these. Remove them, or note them as unmaintained.",
        "| Entry | Repo | Section | Last push |",
        "|-------|------|---------|-----------|",
        [f"| {n} | `{s}` | {sec} | {d}d ago |" for n, s, sec, d in sorted(archived)],
    )

    out += section_block(
        f"Stale: no push in over {STALE_DAYS} days",
        "Over the bar CONTRIBUTING.md sets for new entries. A finished skill can sit "
        "still, so check whether each still works with the agents its row names "
        "before removing it.",
        "| Days | Entry | Repo | Section | Stars |",
        "|------|-------|------|---------|-------|",
        [
            f"| {d} | {n} | `{s}` | {sec} | {st} |"
            for d, n, s, sec, st in sorted(stale, reverse=True)
        ],
    )

    out += section_block(
        "No recognised licence",
        "CONTRIBUTING.md requires a clearly stated licence. `NOASSERTION` means "
        "GitHub found a licence file it could not identify -- usually fine for a "
        "large vendor repo, suspicious for a small one, and not automatically a "
        "rejection. `none` means no root `LICENSE` file, no licence field in a "
        "package manifest or SKILL.md, and no licence file beside the skill, which "
        "is a rejection. A named value below is a field that withholds open-source "
        "terms rather than granting them, such as npm's `UNLICENSED` or "
        "`Proprietary` in SKILL.md.",
        "| Entry | Repo | Section | Licence | Stars |",
        "|-------|------|---------|---------|-------|",
        [
            f"| {n} | `{s}` | {sec} | {lic} | {st} |"
            for n, s, sec, lic, st in sorted(unlicensed, key=lambda x: x[4])
        ],
    )

    out += section_block(
        "Licensed outside a root LICENSE file",
        "No action needed. GitHub's licence API reads the root `LICENSE` file only, "
        "so these report as unlicensed in the sidebar while declaring real terms "
        "somewhere else. CONTRIBUTING.md accepts that.",
        "| Entry | Repo | Section | Licence | Declared in | Stars |",
        "|-------|------|---------|---------|-------------|-------|",
        [
            f"| {n} | `{s}` | {sec} | {lic} | `{f}` | {st} |"
            for n, s, sec, lic, f, st in sorted(declared, key=lambda x: x[5])
        ],
    )

    if not (gone or moved or archived or stale or unlicensed):
        out.append(
            "Every entry is live, licensed, maintained, and unarchived. Nothing to do."
        )

    print("\n".join(out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
