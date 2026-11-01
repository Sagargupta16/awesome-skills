"""Tests for scripts/check_submission.py.

The behaviours worth pinning: that reordering a table is not read as a batch of
new submissions, that a licence declared outside the root LICENSE is recognised
and one that withholds open-source terms is not, and that an entry passes only
when the repository or folder it links holds a SKILL.md whose frontmatter has a
`name` and a `description`.
"""

from __future__ import annotations

import base64
from datetime import datetime, timezone
from pathlib import Path

import pytest
from conftest import commit_readme

import check_submission

ROW_A = "| [Alpha](https://github.com/acme/alpha) | Alpha widget | Any |"
ROW_B = "| [Beta](https://github.com/acme/beta) | Beta widget | Any |"
ROW_C = "| [Gamma](https://github.com/acme/gamma) | Gamma widget | Any |"

SKILL_MD = "---\nname: alpha\ndescription: Does alpha things. Use when alpha.\n---\n\n# Alpha\n"
README = "# Alpha\n\n## Install\n\nCopy the folder into `.claude/skills/`.\n"


# --- row parsing -------------------------------------------------------------


def test_parse_rows_reads_name_url_and_columns():
    rows = check_submission.parse_rows(ROW_A + "\n")

    (sub,) = rows.values()
    assert sub.name == "Alpha"
    assert sub.url == "https://github.com/acme/alpha"
    assert sub.desc == "Alpha widget"
    assert sub.third == "Any"


def test_parse_rows_is_independent_of_row_order():
    """The invariant that lets added_rows() survive a re-sorted table."""
    forward = check_submission.parse_rows(f"{ROW_A}\n{ROW_B}\n")
    reversed_ = check_submission.parse_rows(f"{ROW_B}\n{ROW_A}\n")

    assert set(forward) == set(reversed_)


def test_parse_rows_normalises_trailing_slashes_and_case():
    with_slash = check_submission.parse_rows(
        "| [Alpha](https://github.com/Acme/Alpha/) | Alpha widget | Any |\n"
    )

    assert set(with_slash) == {"github.com/acme/alpha"}


# --- added_rows against a real git history -----------------------------------


@pytest.fixture
def repo(git_repo: Path) -> Path:
    """A base branch carrying two entry rows."""
    commit_readme(git_repo, f"{ROW_A}\n{ROW_B}\n")
    return git_repo


def test_added_rows_ignores_a_reordered_table(repo: Path, monkeypatch):
    (repo / "README.md").write_text(f"{ROW_B}\n{ROW_A}\n", encoding="utf-8")
    monkeypatch.chdir(repo)

    assert check_submission.added_rows("HEAD") == []


def test_added_rows_reports_a_new_row(repo: Path, monkeypatch):
    (repo / "README.md").write_text(f"{ROW_A}\n{ROW_B}\n{ROW_C}\n", encoding="utf-8")
    monkeypatch.chdir(repo)

    added = check_submission.added_rows("HEAD")

    assert [sub.name for sub in added] == ["Gamma"]


def test_added_rows_reports_one_row_when_a_table_is_both_sorted_and_extended(
    repo: Path, monkeypatch
):
    (repo / "README.md").write_text(f"{ROW_C}\n{ROW_B}\n{ROW_A}\n", encoding="utf-8")
    monkeypatch.chdir(repo)

    added = check_submission.added_rows("HEAD")

    assert [sub.name for sub in added] == ["Gamma"]


# --- GitHub URLs --------------------------------------------------------------


def test_a_repository_url_names_the_root_of_the_default_branch():
    target = check_submission.parse_github_url("https://github.com/acme/skills")

    assert target == check_submission.Target("acme", "skills", "", "")


def test_a_folder_url_names_its_branch_and_folder():
    target = check_submission.parse_github_url(
        "https://github.com/acme/skills/tree/main/skills/pdf/"
    )

    assert target == check_submission.Target("acme", "skills", "main", "skills/pdf")
    assert target.slug == "acme/skills"


def test_an_escaped_folder_segment_is_decoded_once():
    target = check_submission.parse_github_url(
        "https://github.com/acme/skills/tree/main/my%20skill"
    )

    assert target.folder == "my skill"


@pytest.mark.parametrize(
    "url",
    [
        "https://github.com/acme/skills/tree/main/../../etc",
        "https://github.com/acme/skills/tree/main/a/%2E%2E/b",
        "https://github.com/acme/skills/tree/main/a%2Fb",
        "https://github.com/acme/skills/blob/main/SKILL.md",
        "https://gitlab.com/acme/skills",
        "https://github.com/acme",
    ],
)
def test_anything_but_a_repository_or_plain_folder_is_refused(url: str):
    """The folder becomes part of an API path; `..` would walk it elsewhere."""
    assert check_submission.parse_github_url(url) is None


def test_a_folder_path_is_escaped_segment_by_segment():
    assert check_submission.quote_path("skills/my skill/SKILL.md") == (
        "skills/my%20skill/SKILL.md"
    )


# --- SKILL.md frontmatter ------------------------------------------------------


def _fields(text: str) -> dict | None:
    parsed = check_submission.parse_frontmatter(text)
    return None if parsed is None else parsed[0]


def test_plain_frontmatter_is_read():
    assert _fields(SKILL_MD) == {
        "name": "alpha",
        "description": "Does alpha things. Use when alpha.",
    }


def test_quoted_values_are_unquoted():
    text = '---\nname: \'alpha\'\ndescription: "Say \\"hi\\""\n---\n'

    assert _fields(text) == {"name": "alpha", "description": 'Say "hi"'}


def test_a_folded_block_description_is_joined():
    text = "---\nname: alpha\ndescription: >-\n  Line one\n  line two.\nlicense: MIT\n---\n"

    fields = _fields(text)

    assert fields["description"] == "Line one line two."
    assert fields["license"] == "MIT"


def test_a_literal_block_keeps_its_line_breaks():
    text = "---\nname: alpha\ndescription: |\n  One\n  Two\n---\n"

    assert _fields(text)["description"] == "One\nTwo"


def test_a_plain_value_continued_on_indented_lines_is_joined():
    text = "---\nname: alpha\ndescription: Starts here\n  and goes on\n---\n"

    assert _fields(text)["description"] == "Starts here and goes on"


def test_a_nested_mapping_does_not_swallow_the_next_key():
    text = '---\nname: alpha\nmetadata:\n  author: acme\n  version: "1.0"\ndescription: Alpha.\n---\n'

    fields = _fields(text)

    assert fields["name"] == "alpha"
    assert fields["description"] == "Alpha."


def test_a_comment_after_a_plain_value_is_dropped():
    assert _fields("---\nname: alpha # the id\ndescription: A.\n---\n")["name"] == (
        "alpha"
    )


def test_a_byte_order_mark_and_crlf_endings_are_tolerated():
    text = "\ufeff---\r\nname: alpha\r\ndescription: A.\r\n---\r\n"

    assert _fields(text) == {"name": "alpha", "description": "A."}


@pytest.mark.parametrize(
    "text",
    [
        "# Alpha\n\nNo frontmatter at all.\n",
        "---\nname: alpha\ndescription: never closed\n",
        "",
    ],
)
def test_a_file_without_closed_frontmatter_has_none(text: str):
    assert check_submission.parse_frontmatter(text) is None


def test_an_unquoted_colon_in_a_plain_value_is_flagged():
    """Strict YAML reads `Use when: x` as a nested mapping and rejects it."""
    text = "---\nname: alpha\ndescription: Use when: you need alpha\n---\n"

    _, risky = check_submission.parse_frontmatter(text)

    assert risky == {"description"}


def test_a_quoted_or_block_colon_is_not_flagged():
    text = (
        '---\nname: alpha\ndescription: "Use when: alpha"\nlicense: >-\n  a: b\n---\n'
    )

    _, risky = check_submission.parse_frontmatter(text)

    assert risky == set()


# --- manifest licence detection ----------------------------------------------


def _licence(filename: str, text: str) -> str | None:
    return check_submission.parse_manifest_licence(filename, text)


def test_package_json_licence_is_read():
    assert (
        _licence("package.json", '{\n  "name": "acme",\n  "license": "MIT"\n}') == "MIT"
    )


def test_package_json_legacy_object_licence_is_read():
    manifest = '{"name": "acme", "license": {"type": "MIT", "url": "http://x/y"}}'

    assert _licence("package.json", manifest) == "MIT"


def test_composer_array_licence_is_read():
    """CONTRIBUTING.md lists composer.json, which allows an array of licences."""
    assert _licence("composer.json", '{"license": ["MIT", "GPL-3.0"]}') == "MIT"


def test_pyproject_string_licence_is_read():
    assert (
        _licence("pyproject.toml", '[project]\nname = "acme"\nlicense = "Apache-2.0"\n')
        == "Apache-2.0"
    )


def test_pyproject_table_licence_is_read():
    """PEP 621's `license = {text = "..."}` form, which a text search misses."""
    manifest = '[project]\nname = "acme"\nlicense = {text = "Apache-2.0"}\n'

    assert _licence("pyproject.toml", manifest) == "Apache-2.0"


def test_cargo_licence_is_read():
    assert _licence("Cargo.toml", '[package]\nlicense = "MIT OR Apache-2.0"\n') == (
        "MIT OR Apache-2.0"
    )


def test_licence_pointing_at_a_file_is_not_a_declaration():
    """A file pointer names no terms, and GitHub already read the root files."""
    manifest = '[project]\nname = "acme"\nlicense = {file = "LICENSE.txt"}\n'

    assert _licence("pyproject.toml", manifest) is None


def test_pom_xml_licence_is_read():
    pom = "<licenses><license><name>MIT License</name></license></licenses>"

    assert _licence("pom.xml", pom) == "MIT License"


def test_manifest_without_a_licence_reads_as_none():
    assert (
        _licence("package.json", '{\n  "name": "acme",\n  "version": "1.0.0"\n}')
        is None
    )


def test_a_nested_licence_key_is_not_read_as_the_packages_own():
    """The reason this is parsed rather than pattern-matched."""
    manifest = '{"name": "acme", "dependencies": {"dep": {"license": "MIT"}}}'

    assert _licence("package.json", manifest) is None


def test_unparseable_manifest_reads_as_none():
    assert _licence("package.json", "{not json") is None
    assert _licence("pyproject.toml", "[project") is None


# --- open-source check on the declared value ---------------------------------


@pytest.mark.parametrize(
    "value",
    [
        "UNLICENSED",
        "unlicensed",
        "SEE LICENSE IN proprietary.txt",
        "Proprietary",
        "Proprietary. LICENSE.txt has complete terms",
        "none",
    ],
)
def test_a_field_that_withholds_open_source_terms_is_rejected(value: str):
    assert check_submission.is_open_source(value) is False


@pytest.mark.parametrize(
    "value", ["MIT", "Apache-2.0", "Unlicense", "MIT OR Apache-2.0"]
)
def test_a_real_licence_is_accepted(value: str):
    assert check_submission.is_open_source(value) is True


@pytest.mark.parametrize(
    ("value", "pointer"),
    [
        ("Complete terms in LICENSE.txt", True),
        ("LICENSE.txt", True),
        ("See LICENSE in LICENSE.md", True),
        ("MIT", False),
        ("Apache-2.0", False),
        ("Proprietary. LICENSE.txt has complete terms", False),
    ],
)
def test_a_skill_licence_that_names_a_bundled_file_is_a_pointer(value, pointer):
    assert check_submission.is_licence_pointer(value) is pointer


# --- manifest_licence over the API -------------------------------------------


def _b64(text: str) -> dict:
    return {"content": base64.b64encode(text.encode("utf-8")).decode("ascii")}


def _fake_api(files: dict):
    """Stand in for gh_api, serving base64 file contents for the paths given."""

    def fake(path: str):
        for name, text in files.items():
            if path.endswith(f"/contents/{name}"):
                return _b64(text), None
        return None, 404

    return fake


def test_manifest_licence_returns_the_first_manifest_that_declares_one(monkeypatch):
    monkeypatch.setattr(
        check_submission,
        "gh_api",
        _fake_api(
            {
                "package.json": '{"name": "acme"}',
                "pyproject.toml": '[project]\nlicense = {text = "Apache-2.0"}\n',
            }
        ),
    )

    assert check_submission.manifest_licence("acme/alpha") == (
        "pyproject.toml",
        "Apache-2.0",
    )


def test_manifest_licence_returns_nothing_when_no_manifest_exists(monkeypatch):
    monkeypatch.setattr(check_submission, "gh_api", _fake_api({}))

    assert check_submission.manifest_licence("acme/alpha") == (None, None)


# --- inspect(), with the GitHub API stubbed ----------------------------------

FRESH = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _repo(**changes) -> dict:
    return {
        "pushed_at": FRESH,
        "created_at": FRESH,
        "license": {"spdx_id": "MIT"},
        "stargazers_count": 3,
        "archived": False,
        "fork": False,
        "default_branch": "main",
    } | changes


class FakeRepo:
    """One repository on the GitHub API: metadata, a file tree and file contents.

    Every request is recorded, so a test can say which paths were asked for.
    """

    def __init__(self, files: dict, repo: dict | None = None, ref: str = "main"):
        self.files = files
        self.repo = repo or _repo()
        self.ref = ref
        self.calls: list[str] = []

    def __call__(self, path: str):
        self.calls.append(path)
        base = "repos/acme/alpha"
        if path == base:
            return self.repo, None
        if path == f"{base}/git/trees/{self.ref}?recursive=1":
            tree = [{"path": p, "type": "blob"} for p in self.files]
            return {"tree": tree, "truncated": False}, None
        if path == f"{base}/license":
            return None, 404
        if path.startswith(f"{base}/readme"):
            folder = path.removeprefix(f"{base}/readme").split("?")[0].strip("/")
            name = f"{folder}/README.md" if folder else "README.md"
            return (_b64(self.files[name]), None) if name in self.files else (None, 404)
        if path.startswith(f"{base}/contents/"):
            name = path.removeprefix(f"{base}/contents/").split("?")[0]
            name = name.replace("%20", " ")
            return (_b64(self.files[name]), None) if name in self.files else (None, 404)
        return None, 404


def _inspected(
    files: dict,
    monkeypatch,
    url: str = "https://github.com/acme/alpha",
    repo: dict | None = None,
    ref: str = "main",
) -> check_submission.Submission:
    api = FakeRepo(files, repo, ref)
    monkeypatch.setattr(check_submission, "gh_api", api)
    sub = check_submission.Submission(
        name="Alpha", url=url, desc="Alpha widget", third="Any"
    )
    check_submission.inspect(sub)
    return sub


GOOD = {"README.md": README, "SKILL.md": SKILL_MD}


def test_a_skill_at_the_repository_root_passes(monkeypatch):
    sub = _inspected(GOOD, monkeypatch)

    assert sub.hard == []
    assert sub.soft == []
    assert sub.facts["skill"] == "alpha (`SKILL.md`)"
    assert sub.facts["SKILL.md files"] == 1


def test_a_repository_with_no_skill_md_is_blocked(monkeypatch):
    sub = _inspected({"README.md": README, "prompts/alpha.md": "# Alpha"}, monkeypatch)

    assert any("No SKILL.md" in problem for problem in sub.hard)


def test_a_skill_md_without_a_description_is_blocked(monkeypatch):
    files = {"README.md": README, "SKILL.md": "---\nname: alpha\n---\n"}

    sub = _inspected(files, monkeypatch)

    assert any("both `name` and `description`" in problem for problem in sub.hard)


def test_a_skill_md_without_frontmatter_is_blocked(monkeypatch):
    files = {"README.md": README, "SKILL.md": "# Alpha\n\nname: alpha\n"}

    sub = _inspected(files, monkeypatch)

    assert any("both `name` and `description`" in problem for problem in sub.hard)


def test_a_lowercase_skill_md_is_not_a_skill(monkeypatch):
    """The specification names the file SKILL.md, and agents look for that."""
    sub = _inspected({"README.md": README, "skill.md": SKILL_MD}, monkeypatch)

    assert any("No SKILL.md" in problem for problem in sub.hard)


def test_a_collection_passes_on_its_first_good_skill(monkeypatch):
    files = {
        "README.md": README,
        "skills/beta/SKILL.md": "---\nname: beta\n---\n",
        "skills/alpha/SKILL.md": SKILL_MD,
        "skills/alpha/scripts/run.py": "print()",
    }

    sub = _inspected(files, monkeypatch)

    assert sub.hard == []
    assert sub.facts["skill"] == "alpha (`skills/alpha/SKILL.md`)"
    assert sub.facts["SKILL.md files"] == 2


def test_only_the_shallowest_few_skill_files_are_read(monkeypatch):
    files = {"README.md": README}
    files |= {f"skills/s{n:02}/SKILL.md": "---\nname: x\n---\n" for n in range(20)}
    api = FakeRepo(files)
    monkeypatch.setattr(check_submission, "gh_api", api)

    search = check_submission.find_skill("acme/alpha", "main", "")

    reads = [c for c in api.calls if "/contents/" in c and "SKILL.md" in c]
    assert len(reads) == check_submission.MAX_SKILL_FILES
    assert search.skill is None


def test_a_folder_url_is_searched_on_its_own_branch(monkeypatch):
    files = {
        "README.md": README,
        "skills/alpha/SKILL.md": SKILL_MD,
        "skills/beta/SKILL.md": SKILL_MD.replace("alpha", "beta"),
    }

    sub = _inspected(
        files,
        monkeypatch,
        url="https://github.com/acme/alpha/tree/dev/skills/beta",
        ref="dev",
    )

    assert sub.hard == []
    assert sub.facts["skill"] == "beta (`skills/beta/SKILL.md`)"
    assert sub.facts["SKILL.md files"] == 1


def test_a_folder_that_does_not_exist_is_blocked(monkeypatch):
    sub = _inspected(
        GOOD,
        monkeypatch,
        url="https://github.com/acme/alpha/tree/main/skills/gone",
        repo=_repo(license=None),
    )

    # one finding: a missing folder has no licence or README of its own to judge
    assert len(sub.hard) == 1
    assert "not in the repository" in sub.hard[0]


def test_a_folder_without_a_skill_md_is_blocked(monkeypatch):
    files = GOOD | {"docs/guide.md": "# Guide"}

    sub = _inspected(
        files, monkeypatch, url="https://github.com/acme/alpha/tree/main/docs"
    )

    assert any("No SKILL.md under `docs`" in problem for problem in sub.hard)


def test_an_unreadable_tree_is_left_for_a_maintainer(monkeypatch):
    api = FakeRepo(GOOD, ref="other")
    monkeypatch.setattr(check_submission, "gh_api", api)
    sub = check_submission.Submission("Alpha", "https://github.com/acme/alpha", "", "")

    check_submission.inspect(sub)

    assert any("SKILL.md not verified" in note for note in sub.soft)
    assert not any("SKILL.md" in problem for problem in sub.hard)


def test_a_non_github_url_is_left_for_a_maintainer(monkeypatch):
    sub = _inspected(GOOD, monkeypatch, url="https://acme.dev/skills/alpha")

    assert sub.hard == []
    assert any("Not a GitHub repository or folder URL" in n for n in sub.soft)


# --- the specification notes ---------------------------------------------------


def test_a_name_that_breaks_the_specification_is_noted(monkeypatch):
    files = GOOD | {"SKILL.md": SKILL_MD.replace("name: alpha", "name: Alpha_Skill")}

    sub = _inspected(files, monkeypatch)

    assert sub.hard == []
    assert any("breaks the specification" in note for note in sub.soft)


def test_a_name_that_differs_from_its_folder_is_noted(monkeypatch):
    files = {"README.md": README, "skills/beta/SKILL.md": SKILL_MD}

    sub = _inspected(files, monkeypatch)

    assert any("does not match its folder `beta`" in note for note in sub.soft)


def test_an_over_long_skill_description_is_noted(monkeypatch):
    long_skill = f"---\nname: alpha\ndescription: {'x' * 1025}\n---\n"

    sub = _inspected(GOOD | {"SKILL.md": long_skill}, monkeypatch)

    assert any("1025 characters" in note for note in sub.soft)


def test_an_unquoted_colon_in_the_description_is_noted(monkeypatch):
    risky = "---\nname: alpha\ndescription: Use when: alpha\n---\n"

    sub = _inspected(GOOD | {"SKILL.md": risky}, monkeypatch)

    assert sub.hard == []
    assert any("strict YAML parser rejects" in note for note in sub.soft)


# --- licences ------------------------------------------------------------------

UNLICENSED_REPO = _repo(license=None)


def test_a_skill_md_that_declares_proprietary_terms_is_blocked(monkeypatch):
    """The specification's own example, and how vendor document skills ship."""
    skill = SKILL_MD.replace(
        "---\n\n", "license: Proprietary. LICENSE.txt has complete terms\n---\n\n"
    )

    sub = _inspected(GOOD | {"SKILL.md": skill}, monkeypatch)

    assert any("Proprietary" in problem for problem in sub.hard)


def test_a_root_licence_does_not_excuse_a_proprietary_skill(monkeypatch):
    skill = SKILL_MD.replace("---\n\n", "license: Proprietary\n---\n\n")

    sub = _inspected(GOOD | {"SKILL.md": skill}, monkeypatch, repo=_repo())

    assert any("not open source" in problem for problem in sub.hard)


def test_a_licence_named_in_skill_md_is_accepted_with_a_note(monkeypatch):
    skill = SKILL_MD.replace("---\n\n", "license: Apache-2.0\n---\n\n")

    sub = _inspected(GOOD | {"SKILL.md": skill}, monkeypatch, repo=UNLICENSED_REPO)

    assert sub.hard == []
    assert sub.facts["license"] == "Apache-2.0 (declared in SKILL.md)"
    assert any("SKILL.md" in note for note in sub.soft)


def test_a_pointer_in_skill_md_is_followed_to_the_licence_file(monkeypatch):
    files = {
        "README.md": README,
        "skills/alpha/SKILL.md": SKILL_MD.replace(
            "---\n\n", "license: Complete terms in LICENSE.txt\n---\n\n"
        ),
        "skills/alpha/LICENSE.txt": "Apache License 2.0",
    }

    sub = _inspected(files, monkeypatch, repo=UNLICENSED_REPO)

    assert sub.hard == []
    assert "skills/alpha/LICENSE.txt" in sub.facts["license"]


def test_a_licence_file_in_a_parent_folder_counts(monkeypatch):
    files = {
        "README.md": README,
        "skills/alpha/SKILL.md": SKILL_MD,
        "skills/LICENSE": "MIT License",
    }

    sub = _inspected(files, monkeypatch, repo=UNLICENSED_REPO)

    assert sub.hard == []
    assert "skills/LICENSE" in sub.facts["license"]


def test_a_licence_file_in_a_sibling_skill_does_not_count(monkeypatch):
    files = {
        "README.md": README,
        "skills/alpha/SKILL.md": SKILL_MD,
        "skills/beta/LICENSE": "MIT License",
    }

    sub = _inspected(files, monkeypatch, repo=UNLICENSED_REPO)

    assert any("No licence anywhere" in problem for problem in sub.hard)


def test_a_manifest_licence_is_accepted_with_a_maintainer_note(monkeypatch):
    files = GOOD | {"package.json": '{"license": "Apache-2.0"}'}

    sub = _inspected(files, monkeypatch, repo=UNLICENSED_REPO)

    assert sub.hard == []
    assert any("package.json" in note for note in sub.soft)
    assert sub.facts["license"] == "Apache-2.0 (declared in package.json)"


def test_a_manifest_that_declares_unlicensed_is_blocked(monkeypatch):
    """npm's marker for a package that is explicitly not open source."""
    files = GOOD | {"package.json": '{"license": "UNLICENSED"}'}

    sub = _inspected(files, monkeypatch, repo=UNLICENSED_REPO)

    assert any("UNLICENSED" in problem for problem in sub.hard)


def test_a_repository_with_no_licence_anywhere_is_blocked(monkeypatch):
    sub = _inspected(GOOD, monkeypatch, repo=UNLICENSED_REPO)

    assert any("No licence anywhere" in problem for problem in sub.hard)


# --- repository state and the README --------------------------------------------


def test_an_archived_repository_is_blocked(monkeypatch):
    sub = _inspected(GOOD, monkeypatch, repo=_repo(archived=True))

    assert any("archived" in problem for problem in sub.hard)


def test_a_fork_is_blocked(monkeypatch):
    sub = _inspected(GOOD, monkeypatch, repo=_repo(fork=True))

    assert any("fork" in problem for problem in sub.hard)


def test_a_repository_not_pushed_in_180_days_is_blocked(monkeypatch):
    sub = _inspected(GOOD, monkeypatch, repo=_repo(pushed_at="2020-01-01T00:00:00Z"))

    assert any("maintenance threshold" in problem for problem in sub.hard)


def test_a_missing_repository_is_blocked(monkeypatch):
    monkeypatch.setattr(check_submission, "gh_api", lambda path: (None, 404))
    sub = check_submission.Submission("Alpha", "https://github.com/acme/alpha", "", "")

    check_submission.inspect(sub)

    assert any("returns 404" in problem for problem in sub.hard)


def test_no_readme_anywhere_is_blocked(monkeypatch):
    sub = _inspected({"SKILL.md": SKILL_MD}, monkeypatch)

    assert any("No README" in problem for problem in sub.hard)


def test_a_readme_in_the_linked_folder_is_used_first(monkeypatch):
    files = {
        "skills/alpha/README.md": README,
        "skills/alpha/SKILL.md": SKILL_MD,
    }

    sub = _inspected(
        files, monkeypatch, url="https://github.com/acme/alpha/tree/main/skills/alpha"
    )

    assert sub.hard == []
    assert sub.soft == []


def test_a_readme_that_never_says_how_to_use_it_is_noted(monkeypatch):
    files = GOOD | {"README.md": "# Alpha\n\nA skill about alpha.\n"}

    sub = _inspected(files, monkeypatch)

    assert sub.hard == []
    assert any("never mentions installing" in note for note in sub.soft)


# --- report rendering --------------------------------------------------------


def _clean_subs(*names):
    return [
        check_submission.Submission(
            name=name, url=f"https://github.com/acme/{name}", desc="Widget", third="Any"
        )
        for name in names
    ]


def test_render_blocks_on_a_hard_failure():
    (sub,) = _clean_subs("alpha")
    sub.hard.append("The repository is archived.")

    report, failing = check_submission.render([sub], override=False)

    assert failing is True
    assert "Result: blocked." in report


def test_render_honours_the_maintainer_override_label():
    (sub,) = _clean_subs("alpha")
    sub.hard.append("The repository is archived.")

    report, failing = check_submission.render([sub], override=True)

    assert failing is False
    assert check_submission.OVERRIDE_LABEL in report


def test_render_passes_several_entries_when_none_has_a_defect():
    report, failing = check_submission.render(
        _clean_subs("alpha", "beta"), override=False
    )

    assert failing is False
    assert "Result: passed." in report


def test_render_notes_the_entry_count_without_failing():
    report, _ = check_submission.render(
        _clean_subs("alpha", "beta", "gamma"), override=False
    )

    assert "adds 3 entries" in report
    assert "does not fail this check" in report


def test_render_omits_the_count_note_for_a_single_entry():
    report, _ = check_submission.render(_clean_subs("alpha"), override=False)

    assert "one skill per" not in report


def test_render_blocks_when_one_of_several_entries_has_a_defect():
    subs = _clean_subs("alpha", "beta")
    subs[1].hard.append("The repository is archived.")

    report, failing = check_submission.render(subs, override=False)

    assert failing is True
    assert "1 blocking problem(s) across 2 entries" in report


def test_render_passes_a_clean_single_entry():
    report, failing = check_submission.render(_clean_subs("alpha"), override=False)

    assert failing is False
    assert "Result: passed." in report


# --- exit code --------------------------------------------------------------


def test_a_maintainer_note_does_not_fail_the_check(monkeypatch):
    """Soft findings are for a person to read; only a hard one turns it red."""
    (sub,) = _clean_subs("alpha")
    sub.soft.append("Confirm the licence by hand.")
    monkeypatch.setattr(check_submission, "added_rows", lambda base: [sub])
    monkeypatch.setattr(check_submission, "inspect", lambda sub: None)
    monkeypatch.delenv("GITHUB_STEP_SUMMARY", raising=False)
    monkeypatch.setattr("sys.argv", ["check_submission.py"])

    assert check_submission.main() == 0
