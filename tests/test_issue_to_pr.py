"""Tests for scripts/issue_to_pr.py, which turns the issue form into a README row."""

from __future__ import annotations

import json

import pytest

import issue_to_pr

FORM = """### Name

Acme Review

### Repository or folder URL

https://github.com/acme/skills/tree/main/review/

### Category

Security

### Works with

Codex, Claude Code

### Description

reviews acme code for secrets.

### Affiliation

I am the author or maintainer

### Quality standards

- [X] The repository or folder holds a SKILL.md

### Anything else

_No response_
"""

README = """## Skills

### Security

| Skill | Description | Works with |
|-------|-------------|------------|
| [Beta Review](https://github.com/beta/review) | Beta scanner | Any |
| [Zeta Review](https://github.com/zeta/review) | Zeta scanner | Any |

### Writing & Content

| Skill | Description | Works with |
|-------|-------------|------------|
| [Web Writer](https://github.com/web/writer) | Web pages | Codex |

## Collections

| Collection | Description | Works with |
|------------|-------------|------------|
"""


def _lines(text: str) -> list[str]:
    return text.splitlines(True)


def test_parse_form_reads_answers_and_drops_no_response():
    fields = issue_to_pr.parse_form(FORM)

    assert fields["Name"] == "Acme Review"
    assert fields["Category"] == "Security"
    assert fields["Works with"] == "Codex, Claude Code"
    assert fields["Anything else"] == ""


def test_build_row_normalises_the_answers():
    section, row = issue_to_pr.build_row(issue_to_pr.parse_form(FORM))

    assert section == "Security"
    assert row == (
        "| [Acme Review](https://github.com/acme/skills/tree/main/review) | "
        "Reviews acme code for secrets | Claude Code, Codex |"
    )


def test_works_with_is_matched_without_regard_to_case():
    fields = issue_to_pr.parse_form(FORM)
    fields["Works with"] = "gemini cli, COPILOT"

    _, row = issue_to_pr.build_row(fields)

    assert row.endswith("| Gemini CLI, Copilot |")


def test_a_collection_goes_to_the_collections_table():
    fields = issue_to_pr.parse_form(FORM)
    fields["Category"] = "Collections"

    section, _ = issue_to_pr.build_row(fields)

    assert section == "Collections"


@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        ("Name", "Bad | Name", "cannot contain"),
        ("Repository or folder URL", "http://github.com/a/b", "https://"),
        ("Repository or folder URL", "https://x.com/a b", "https://"),
        ("Description", "x" * 81, "81 characters"),
        ("Works with", "Windsurf", "not a list of agents"),
        ("Works with", "", "not a list of agents"),
        ("Works with", "Any, Codex", "already means every agent"),
        ("Category", "Blockchain", "not a category"),
    ],
)
def test_build_row_rejects_broken_answers(field, value, message):
    fields = issue_to_pr.parse_form(FORM)
    fields[field] = value

    with pytest.raises(issue_to_pr.Rejected, match=message):
        issue_to_pr.build_row(fields)


@pytest.mark.parametrize(
    "section", ["Official", "Tools", "Tutorials & Articles", "Community"]
)
def test_bullet_sections_are_left_to_a_maintainer(section: str):
    fields = issue_to_pr.parse_form(FORM)
    fields["Category"] = section

    with pytest.raises(LookupError):
        issue_to_pr.build_row(fields)


def test_insert_row_lands_in_its_table_in_order():
    row = "| [Gamma Review](https://github.com/gamma/review) | Gamma scanner | Any |"

    out = "".join(issue_to_pr.insert_row(_lines(README), "Security", row))

    security = out.split("### Writing")[0]
    assert (
        security.index("Beta Review")
        < security.index("Gamma Review")
        < security.index("Zeta Review")
    )
    assert out.count("Gamma Review") == 1


def test_insert_row_fills_an_empty_table():
    """The list launched with header-only tables, which a row must still land in."""
    row = "| [Acme Pack](https://github.com/acme/pack) | Acme skills | Any |"

    out = "".join(issue_to_pr.insert_row(_lines(README), "Collections", row))

    assert out.rstrip().endswith("| Any        |")
    assert "[Acme Pack](https://github.com/acme/pack)" in out.split("## Collections")[1]


def test_insert_row_refuses_a_link_already_listed():
    row = "| [Web Again](https://github.com/web/writer/) | Same repo | Codex |"

    with pytest.raises(issue_to_pr.Rejected, match="already on the list"):
        issue_to_pr.insert_row(_lines(README), "Security", row)


def test_main_writes_the_readme_and_reports_ok(tmp_path, monkeypatch):
    (tmp_path / "README.md").write_text(README, encoding="utf-8")
    event = tmp_path / "event.json"
    event.write_text(
        json.dumps({"issue": {"number": 7, "body": FORM}}), encoding="utf-8"
    )
    out = tmp_path / "out.txt"
    monkeypatch.setattr(issue_to_pr, "ROOT", tmp_path)
    monkeypatch.setenv("GITHUB_EVENT_PATH", str(event))
    monkeypatch.setenv("GITHUB_OUTPUT", str(out))

    assert issue_to_pr.main() == 0

    assert "status=ok" in out.read_text(encoding="utf-8")
    assert "name=Acme Review" in out.read_text(encoding="utf-8")
    assert "[Acme Review]" in (tmp_path / "README.md").read_text(encoding="utf-8")


def test_main_explains_a_rejection_without_touching_the_readme(tmp_path, monkeypatch):
    (tmp_path / "README.md").write_text(README, encoding="utf-8")
    body = FORM.replace("Codex, Claude Code", "Windsurf")
    event = tmp_path / "event.json"
    event.write_text(
        json.dumps({"issue": {"number": 7, "body": body}}), encoding="utf-8"
    )
    out = tmp_path / "out.txt"
    monkeypatch.setattr(issue_to_pr, "ROOT", tmp_path)
    monkeypatch.setenv("GITHUB_EVENT_PATH", str(event))
    monkeypatch.setenv("GITHUB_OUTPUT", str(out))

    assert issue_to_pr.main() == 0

    assert "status=invalid" in out.read_text(encoding="utf-8")
    assert "Windsurf" in (tmp_path / "issue-comment.md").read_text(encoding="utf-8")
    assert (tmp_path / "README.md").read_text(encoding="utf-8") == README


def test_main_hands_a_bullet_section_to_a_maintainer(tmp_path, monkeypatch):
    (tmp_path / "README.md").write_text(README, encoding="utf-8")
    body = FORM.replace("### Category\n\nSecurity", "### Category\n\nTools")
    event = tmp_path / "event.json"
    event.write_text(
        json.dumps({"issue": {"number": 7, "body": body}}), encoding="utf-8"
    )
    out = tmp_path / "out.txt"
    monkeypatch.setattr(issue_to_pr, "ROOT", tmp_path)
    monkeypatch.setenv("GITHUB_EVENT_PATH", str(event))
    monkeypatch.setenv("GITHUB_OUTPUT", str(out))

    assert issue_to_pr.main() == 0

    assert "status=manual" in out.read_text(encoding="utf-8")
    assert (tmp_path / "README.md").read_text(encoding="utf-8") == README
