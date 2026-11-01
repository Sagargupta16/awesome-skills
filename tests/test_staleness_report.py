"""Tests for scripts/staleness_report.py.

The monthly audit is the mechanism that catches rot, so what matters is that its
entry regex actually reaches every listed repository, including entries that
point into a folder, and that it judges a licence the way the submission gate
does.
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import check_submission
import staleness_report


def slugs(line: str) -> list[str]:
    return [
        f"{m.group('owner')}/{m.group('repo')}"
        for m in staleness_report.ENTRY_RE.finditer(line)
    ]


def test_plain_repository_link_is_matched():
    row = "| [Acme](https://github.com/acme/review) | Acme widget | Any |"

    assert slugs(row) == ["acme/review"]


def test_trailing_slash_link_is_matched():
    row = "| [Acme](https://github.com/acme/review/) | Acme widget | Any |"

    assert slugs(row) == ["acme/review"]


def test_folder_link_resolves_to_the_parent_repository():
    row = "| [PDF](https://github.com/anthropics/skills/tree/main/skills/pdf) | PDF | Any |"

    assert slugs(row) == ["anthropics/skills"]


def test_bullet_link_is_matched():
    bullet = (
        "- [Skill Lint](https://github.com/acme/skill-lint) - Lints SKILL.md files."
    )

    assert slugs(bullet) == ["acme/skill-lint"]


def test_non_github_link_is_not_matched():
    row = "| [Acme](https://acme.dev/skills/review) | Hosted docs | Any |"

    assert slugs(row) == []


README = """## Skills

### Documents & Office

| Skill | Description | Works with |
| ----- | ----------- | ---------- |
| [PDF](https://github.com/acme/skills/tree/main/skills/pdf) | PDF files | Any |
| [DOCX](https://github.com/acme/skills/tree/main/skills/docx) | Word files | Any |

## Contributing

Open an [issue](https://github.com/Sagargupta16/awesome-skills/issues/new/choose).
"""


def _collected(tmp_path: Path) -> list:
    readme = tmp_path / "README.md"
    readme.write_text(README, encoding="utf-8")
    return staleness_report.collect(readme)


def test_collect_skips_this_repositorys_own_links(tmp_path):
    """The issue links and the badge are not list entries."""
    collected = _collected(tmp_path)

    assert staleness_report.SELF_SLUG not in {
        f"{owner}/{repo}".lower() for _, owner, repo, _, _ in collected
    }


def test_collect_keeps_two_folders_of_one_repository_apart(tmp_path):
    collected = _collected(tmp_path)

    assert [(name, section) for name, _, _, section, _ in collected] == [
        ("PDF", "Documents & Office"),
        ("DOCX", "Documents & Office"),
    ]


def test_collect_survives_the_real_readme():
    assert isinstance(staleness_report.collect(), list)


# --- classification --------------------------------------------------------------

STALE_UNLICENSED = {
    "nameWithOwner": "acme/skills",
    "stargazerCount": 0,
    "pushedAt": "2020-01-01T00:00:00Z",
    "isArchived": False,
    "defaultBranchRef": {"name": "trunk"},
    "licenseInfo": None,
}
URL = "https://github.com/acme/skills/tree/main/skills/pdf"
ENTRY = ("PDF", "acme", "skills", "Documents & Office", URL)
NOW = datetime.now(timezone.utc)


def test_an_entry_is_judged_on_licence_and_push():
    buckets = staleness_report.classify({ENTRY: STALE_UNLICENSED}, NOW)

    assert len(buckets["stale"]) == 1
    assert len(buckets["no_licence"]) == 1


def test_an_archived_repository_is_reported_and_not_called_stale():
    archived = STALE_UNLICENSED | {"isArchived": True}

    buckets = staleness_report.classify({ENTRY: archived}, NOW)

    assert len(buckets["archived"]) == 1
    assert buckets["stale"] == []


def test_a_renamed_repository_is_reported_as_moved():
    moved = STALE_UNLICENSED | {"nameWithOwner": "acme-org/skills"}

    buckets = staleness_report.classify({ENTRY: moved}, NOW)

    assert buckets["moved"] == [("PDF", "acme/skills", "acme-org/skills", ENTRY[3])]


def test_a_missing_repository_is_reported_as_gone():
    buckets = staleness_report.classify({ENTRY: None}, NOW)

    assert buckets["gone"] == [("PDF", "acme/skills", ENTRY[3])]


# --- licences declared outside the root -----------------------------------------


def _no_licence(url: str = URL, branch: str = "trunk") -> list:
    return [("PDF", "acme/skills", "Documents & Office", "none", 4, url, branch)]


def _stub_gate(monkeypatch, declared: tuple) -> list:
    """Replace the gate's lookups; return the (slug, ref, folder) each was asked."""
    asked = []

    def find(slug, ref, folder):
        asked.append((slug, ref, folder))
        return check_submission.Search()

    monkeypatch.setattr(staleness_report, "find_skill", find)
    monkeypatch.setattr(staleness_report, "declared_licence", lambda s, x: declared)
    return asked


def test_the_folder_and_branch_in_the_url_are_what_the_gate_is_asked(monkeypatch):
    asked = _stub_gate(monkeypatch, (None, None, None))

    staleness_report.resolve_declared_licences(_no_licence())

    assert asked == [("acme/skills", "main", "skills/pdf")]


def test_a_repository_root_url_is_read_on_its_default_branch(monkeypatch):
    asked = _stub_gate(monkeypatch, (None, None, None))

    staleness_report.resolve_declared_licences(
        _no_licence(url="https://github.com/acme/skills")
    )

    assert asked == [("acme/skills", "trunk", "")]


def test_a_licence_named_in_skill_md_is_information_not_a_finding(monkeypatch):
    _stub_gate(monkeypatch, ("skills/pdf/SKILL.md", "MIT", "frontmatter"))

    declared, unlicensed = staleness_report.resolve_declared_licences(_no_licence())

    assert unlicensed == []
    assert declared[0][3:5] == ("MIT", "skills/pdf/SKILL.md")


def test_a_licence_file_beside_the_skill_is_information(monkeypatch):
    _stub_gate(monkeypatch, ("skills/pdf/LICENSE.txt", "LICENSE.txt", "file"))

    declared, unlicensed = staleness_report.resolve_declared_licences(_no_licence())

    assert unlicensed == []
    assert declared[0][4] == "skills/pdf/LICENSE.txt"


def test_proprietary_terms_in_skill_md_are_a_finding(monkeypatch):
    _stub_gate(monkeypatch, ("skills/pdf/SKILL.md", "Proprietary", "frontmatter"))

    _, unlicensed = staleness_report.resolve_declared_licences(_no_licence())

    assert unlicensed[0][3] == "Proprietary in skills/pdf/SKILL.md"


def test_noassertion_is_reported_without_a_lookup(monkeypatch):
    asked = _stub_gate(monkeypatch, (None, None, None))
    rows = [("PDF", "acme/skills", "Documents & Office", "NOASSERTION", 4, URL, "main")]

    _, unlicensed = staleness_report.resolve_declared_licences(rows)

    assert asked == []
    assert unlicensed[0][3] == "NOASSERTION"
