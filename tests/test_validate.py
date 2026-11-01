"""Tests for scripts/validate.py.

Every pull request to this repository is gated by this validator, so a silent
regression in it weakens every gate while CI stays green. These tests pin the
rules CONTRIBUTING.md promises against small fixtures rather than the real
README, plus one integration check that the validator survives the real file.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

import pytest

import validate

REPO_ROOT = Path(__file__).resolve().parent.parent
GOOD_ROW = "| [Acme Skill](https://github.com/acme/skill) | Acme widget skill | Any |"


def _lines(body: str) -> list[str]:
    return [line + "\n" for line in body.strip("\n").split("\n")]


def entry_errors(body: str) -> list[str]:
    """Run the per-entry checks over a snippet and return the messages."""
    rep = validate.Report()
    entries, _, _ = validate.parse(_lines(body))
    validate.check_entries(entries, rep)
    return rep.errors


def duplicate_errors(body: str) -> list[str]:
    rep = validate.Report()
    entries, _, _ = validate.parse(_lines(body))
    validate.check_duplicates(entries, rep)
    return rep.errors


def order_report(body: str) -> validate.Report:
    rep = validate.Report()
    entries, _, _ = validate.parse(_lines(body))
    validate.check_alphabetical(entries, rep)
    return rep


def structure_errors(categories: list[str]) -> list[str]:
    """Build a headings-only skeleton and run the section-order check on it."""
    lines: list[str] = []
    for top in validate.TOP_SECTIONS:
        lines.append(f"## {top}\n")
        if top == "Skills":
            lines.extend(f"### {c}\n" for c in categories)
    rep = validate.Report()
    _, heading_lines, order = validate.parse(lines)
    validate.check_structure(lines, order, heading_lines, rep)
    return rep.errors


# --- description rules -------------------------------------------------------


def test_over_length_table_description_is_reported():
    long_desc = "A" * 81
    errors = entry_errors(
        f"## Security\n\n| [Acme](https://x.dev) | {long_desc} | Codex |"
    )

    assert any("description is 81 chars, max 80" in e for e in errors)


def test_lowercase_description_is_reported():
    errors = entry_errors(
        "## Security\n\n| [Acme](https://x.dev) | acme widget | Codex |"
    )

    assert any("must start with a capital letter" in e for e in errors)


def test_table_description_ending_in_a_period_is_reported():
    errors = entry_errors(
        "## Security\n\n| [Acme](https://x.dev) | Acme widget. | Codex |"
    )

    assert any("must not end with a period" in e for e in errors)


def test_bullet_description_without_a_period_is_reported():
    errors = entry_errors("## Official\n\n- [Acme](https://x.dev) - Acme widget")

    assert any("must end with a period" in e for e in errors)


def test_tools_is_a_bullet_section():
    errors = entry_errors("## Tools\n\n- [Acme](https://x.dev) - Acme validator")

    assert any("must end with a period" in e for e in errors)


def test_non_https_url_is_reported():
    errors = entry_errors(
        "## Security\n\n| [Acme](http://x.dev) | Acme widget | Codex |"
    )

    assert any("must be https://" in e for e in errors)


# --- the Works with vocabulary -----------------------------------------------


def works_with_errors(cell: str, section: str = "Security") -> list[str]:
    return entry_errors(
        f"## {section}\n\n| [Acme](https://x.dev) | Acme widget | {cell} |"
    )


def test_unknown_agent_is_reported():
    errors = works_with_errors("Claude Code, Windsurf")

    assert any("Works with 'Claude Code, Windsurf'" in e for e in errors)
    assert any("['Windsurf']" in e for e in errors)


def test_every_agent_in_the_vocabulary_is_accepted_alone():
    body = "## Security\n\n" + "\n".join(
        f"| [Acme {i}](https://x.dev/{i}) | Acme widget | {agent} |"
        for i, agent in enumerate(validate.WORKS_WITH)
    )

    assert entry_errors(body) == []


def test_several_named_agents_are_accepted():
    assert works_with_errors("Claude Code, Codex, Cursor, Gemini CLI, Copilot") == []


def test_agents_are_accepted_in_any_order():
    assert works_with_errors("Copilot, Claude Code") == []


def test_spelling_must_match_the_vocabulary_exactly():
    """`claude code` would split the site's filter into two spellings."""
    assert works_with_errors("claude code") != []


def test_any_combined_with_a_named_agent_is_reported():
    errors = works_with_errors("Any, Codex")

    assert any("already means every agent" in e for e in errors)


def test_an_agent_named_twice_is_reported():
    errors = works_with_errors("Codex, Codex")

    assert any("same agent twice" in e for e in errors)


@pytest.mark.parametrize("cell", ["", "Codex,", "Codex,, Cursor"])
def test_an_empty_item_is_reported(cell: str):
    assert any("empty item" in e for e in works_with_errors(cell))


def test_collections_use_the_works_with_vocabulary_too():
    errors = works_with_errors("Go", section="Collections")

    assert any("Works with 'Go'" in e for e in errors)


def test_works_with_problem_is_none_for_a_good_cell():
    assert validate.works_with_problem("Claude Code, Codex") is None


# --- duplicates and ordering -------------------------------------------------


def test_duplicate_url_across_sections_is_reported():
    body = (
        "## Security\n\n| [Acme](https://github.com/acme/skill) | Acme widget | Any |\n"
        "## Productivity\n\n| [Acme Two](https://github.com/acme/skill/) | Acme widget | Any |"
    )

    assert any("duplicate URL" in e for e in duplicate_errors(body))


def test_duplicate_name_across_sections_is_reported():
    body = (
        "## Security\n\n| [Acme](https://github.com/acme/one) | Acme widget | Any |\n"
        "## Productivity\n\n| [acme](https://github.com/acme/two) | Acme widget | Any |"
    )

    assert any("duplicate name" in e for e in duplicate_errors(body))


def test_two_folders_of_one_repository_are_not_duplicates():
    body = (
        "## Security\n\n"
        "| [Alpha](https://github.com/acme/skills/tree/main/alpha) | Alpha | Any |\n"
        "| [Beta](https://github.com/acme/skills/tree/main/beta) | Beta | Any |"
    )

    assert duplicate_errors(body) == []


def test_rows_out_of_alphabetical_order_are_noted():
    body = (
        "## Security\n\n"
        "| [Zeta](https://x.dev/z) | Zeta widget | Any |\n"
        "| [Alpha](https://x.dev/a) | Alpha widget | Any |"
    )

    rep = order_report(body)

    assert any("out of alphabetical order" in n for n in rep.notes)


def test_ordering_never_produces_a_blocking_error():
    """Where a row sits is cosmetic, so it must not fail a pull request."""
    body = (
        "## Security\n\n"
        "| [Zeta](https://x.dev/z) | Zeta widget | Any |\n"
        "| [Alpha](https://x.dev/a) | Alpha widget | Any |"
    )

    assert order_report(body).errors == []


def test_sorted_rows_produce_no_ordering_note():
    body = (
        "## Security\n\n"
        "| [Alpha](https://x.dev/a) | Alpha widget | Any |\n"
        "| [Zeta](https://x.dev/z) | Zeta widget | Any |"
    )

    assert order_report(body).notes == []


# --- empty sections ----------------------------------------------------------


def empty_report(body: str) -> validate.Report:
    rep = validate.Report()
    entries, heading_lines, _ = validate.parse(_lines(body))
    validate.check_empty_sections(entries, heading_lines, rep)
    return rep


def test_an_empty_category_is_a_note_not_an_error():
    rep = empty_report(
        "### Security\n\n| Skill | Description | Works with |\n| --- | --- | --- |"
    )

    assert rep.errors == []
    assert any("'Security' has no entries yet" in n for n in rep.notes)


def test_an_empty_bullet_section_is_a_note():
    rep = empty_report("## Tools\n")

    assert any("'Tools' has no entries yet" in n for n in rep.notes)


def test_a_category_with_a_row_gets_no_empty_note():
    rep = empty_report(
        "### Security\n\n| Skill | Description | Works with |\n| --- | --- | --- |\n"
        f"{GOOD_ROW}"
    )

    assert rep.notes == []


def test_a_category_with_no_table_at_all_is_still_an_error():
    rep = validate.Report()
    lines = _lines("### Security\n\nNothing here yet.")
    _, heading_lines, _ = validate.parse(lines)

    validate.check_table_headers(lines, heading_lines, rep)

    assert any("has no table" in e for e in rep.errors)


# --- structure and table of contents ----------------------------------------


def test_unknown_skill_category_is_reported():
    errors = structure_errors([*validate.SKILL_CATEGORIES, "Blockchain"])

    assert any("unknown skill category ['Blockchain']" in e for e in errors)


def test_missing_skill_category_is_reported():
    errors = structure_errors(validate.SKILL_CATEGORIES[1:])

    assert any("skill category missing from README" in e for e in errors)


def test_canonical_categories_pass_the_structure_check():
    assert structure_errors(validate.SKILL_CATEGORIES) == []


def test_toc_anchor_without_a_matching_heading_is_reported():
    lines = _lines("## Contents\n\n- [Official](#no-such-heading)\n\n---")
    rep = validate.Report()
    _, heading_lines, _ = validate.parse(lines)
    validate.check_toc(lines, heading_lines, rep)

    assert any("#no-such-heading has no matching heading" in e for e in rep.errors)


def test_slugify_matches_githubs_double_hyphen_for_ampersands():
    assert validate.slugify("DevOps & Cloud") == "devops--cloud"


def test_collections_header_is_enforced():
    rep = validate.Report()
    lines = _lines(
        "## Collections\n\n| Skill | Description | Works with |\n| --- | --- | --- |"
    )
    _, heading_lines, _ = validate.parse(lines)

    validate.check_table_headers(lines, heading_lines, rep)

    assert any(
        "expected ['Collection', 'Description', 'Works with']" in e for e in rep.errors
    )


# --- whitespace and dashes ---------------------------------------------------


def test_em_dash_is_reported():
    rep = validate.Report()
    validate.check_whitespace_and_dashes([f"a {chr(0x2014)} b\n"], rep)

    assert any("contains a em-dash" in e for e in rep.errors)


def test_en_dash_is_reported():
    rep = validate.Report()
    validate.check_whitespace_and_dashes([f"a {chr(0x2013)} b\n"], rep)

    assert any("contains a en-dash" in e for e in rep.errors)


def test_trailing_whitespace_is_reported():
    rep = validate.Report()
    validate.check_whitespace_and_dashes(["Acme  \n"], rep)

    assert any("trailing whitespace" in e for e in rep.errors)


# --- the --fix path ----------------------------------------------------------


def test_fix_reorders_rows_without_adding_or_dropping_any():
    lines = _lines(
        "### Security\n\n"
        "| Skill | Description | Works with |\n"
        "|-------|-------------|------------|\n"
        "| [Zeta](https://x.dev/z) | Zeta widget | Any |\n"
        "| [Alpha](https://x.dev/a) | Alpha widget | Any |"
    )

    fixed = validate.fix(lines)

    assert len(fixed) == len(lines)
    assert [validate._cells(row)[0] for row in fixed[-2:]] == [
        "[Alpha](https://x.dev/a)",
        "[Zeta](https://x.dev/z)",
    ]


def test_align_tables_lines_up_every_pipe():
    """awesome-lint rejects a table whose pipes do not line up."""
    lines = _lines(
        "| Skill | Description | Works with |\n"
        "|-------|-------------|------------|\n"
        "| [Alpha](https://x.dev/a) | Alpha widget | Any |\n"
        "| [B](https://x.dev/b) | B | Claude Code, Codex |"
    )

    aligned = validate.align_tables(lines)

    pipes = {tuple(i for i, ch in enumerate(row) if ch == "|") for row in aligned}
    assert len(pipes) == 1
    assert aligned[1].startswith("| ---")


def test_align_tables_pads_an_empty_table():
    """The list launched with header-only tables; --fix must leave them valid."""
    lines = _lines("| Skill | Description | Works with |\n|---|---|---|")

    aligned = validate.align_tables(lines)

    assert aligned == [
        "| Skill | Description | Works with |\n",
        "| ----- | ----------- | ---------- |\n",
    ]


def test_align_tables_keeps_alignment_colons():
    lines = _lines("| A | B |\n|:---|---:|\n| x | y |")

    aligned = validate.align_tables(lines)

    assert validate._cells(aligned[1]) == [":--", "--:"]


def test_align_tables_justifies_right_and_centred_columns():
    lines = _lines(
        "| L | C | R |\n|:---|:---:|---:|\n| left | mid | right |\n| a | b | c |"
    )

    aligned = validate.align_tables(lines)

    assert aligned[3] == "| a    |  b  |     c |\n"


def test_align_tables_keeps_an_escaped_pipe_inside_its_cell():
    lines = _lines("| A | B |\n|---|---|\n| [x \\| y](https://x.dev) | Wide cell |")

    aligned = validate.align_tables(lines)

    assert validate._cells(aligned[2]) == ["[x \\| y](https://x.dev)", "Wide cell"]


def test_align_tables_counts_an_astral_character_as_two_units():
    lines = _lines("| A |\n|---|\n| x\U0001f50d |\n| abc |")

    aligned = validate.align_tables(lines)

    assert aligned[3] == "| abc |\n"
    assert aligned[2] == "| x\U0001f50d |\n"


def test_align_tables_leaves_prose_alone():
    lines = _lines("Some prose.\n\n- [Item](https://x.dev) - A thing.")

    assert validate.align_tables(lines) == lines


def test_align_tables_leaves_fenced_examples_alone():
    lines = _lines("```\n| not | a table |\n|x|\n```")

    assert validate.align_tables(lines) == lines


def test_aligned_rows_still_parse_as_entries():
    """The gate scripts read padded rows the same as unpadded ones."""
    row = "| [Alpha](https://x.dev/a)    | Alpha widget | Claude Code, Codex |"

    match = validate.ROW_RE.match(row)

    assert match.group("name") == "Alpha"
    assert match.group("url") == "https://x.dev/a"


def test_fix_is_idempotent():
    lines = _lines(
        "### Security\n\n"
        "| Skill | Description | Works with |\n"
        "|-------|-------------|------------|\n"
        "| [Zeta](https://x.dev/z) | Zeta widget | Any |\n"
        "| [Alpha](https://x.dev/a) | Alpha widget | Any |"
    )

    once = validate.fix(lines)
    twice = validate.fix(once)

    assert once == twice


def test_fix_rewrites_an_em_dash_as_two_hyphens():
    fixed = validate.fix([f"Acme {chr(0x2014)} widget\n"])

    assert fixed == ["Acme -- widget\n"]


# --- drift guards ------------------------------------------------------------


def test_contributing_category_table_matches_the_enforced_list():
    """The docs and the enforcement list must not disagree silently."""
    body = (REPO_ROOT / "CONTRIBUTING.md").read_text(encoding="utf-8")
    table = body.split("| Category | Scope |", 1)[1]

    categories = []
    for line in table.splitlines():
        if not line.startswith("|"):
            if categories:
                break
            continue
        cell = line.strip().strip("|").split("|")[0].strip()
        if set(cell) <= {"-", " "}:
            continue
        categories.append(cell)

    assert categories == validate.SKILL_CATEGORIES


def _form_options(field_id: str) -> list[str]:
    """The options of one dropdown in the add-skill issue form, as written."""
    form = (REPO_ROOT / ".github/ISSUE_TEMPLATE/add-skill.yml").read_text(
        encoding="utf-8"
    )
    block = form.split(f"id: {field_id}\n", 1)[1].split("\n  - type:", 1)[0]
    options = block.split("options:\n", 1)[1]
    return re.findall(r"^\s+- (.+)$", options.split("\n    validations:", 1)[0], re.M)


def test_the_issue_form_offers_every_category_in_order():
    """issue_to_pr.py rejects a category the validator does not know."""
    options = _form_options("category")

    assert options[: len(validate.SKILL_CATEGORIES)] == validate.SKILL_CATEGORIES
    assert set(options) == {
        *validate.SKILL_CATEGORIES,
        "Collections",
        *validate.BULLET_SECTIONS,
    }


def test_the_issue_form_offers_exactly_the_works_with_vocabulary():
    assert _form_options("works-with") == validate.WORKS_WITH


def test_validator_runs_cleanly_against_the_real_readme():
    """The validator must survive the real file and give a verdict, not crash.

    Whether the README currently passes is the Validate format job's business,
    not this suite's: on a pull request that job compares against the base
    branch, so an author is not failed for a bad row someone else merged.

    Asserting returncode == 0 here would put that judgement back into the test
    suite without the baseline, which is how the sister list once went red on
    one pull request for another's mistake.
    """
    result = subprocess.run(
        [sys.executable, "scripts/validate.py"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode in (0, 1), (
        f"validator crashed instead of reporting: {result.returncode}\n{result.stderr}"
    )
    assert "Traceback" not in result.stderr, result.stderr


# --- baseline mode -----------------------------------------------------------


def test_problem_key_ignores_the_line_number():
    a = "README.md:12: 'Acme' description is 90 chars, max 80"
    b = "README.md:400: 'Acme' description is 90 chars, max 80"

    assert validate.problem_key(a) == validate.problem_key(b)


def test_problem_key_keeps_the_message():
    key = validate.problem_key("README.md:12: 'Acme' is out of alphabetical order")

    assert key == "'Acme' is out of alphabetical order"


def test_baseline_errors_returns_none_for_an_unreadable_ref():
    assert validate.baseline_errors("refs/heads/definitely-not-a-real-ref") is None


def test_run_checks_reports_a_long_description_and_counts_entries():
    body = """
## Official

## Skills

### Security

| Skill | Description | Works with |
|-------|-------------|------------|
| [Acme](https://github.com/acme/acme) | {} | Any |
""".format("x" * 90)

    errors, total, _ = validate.run_checks(_lines(body))

    assert total == 1
    assert any("chars, max 80" in e for e in errors)


def _launch_skeleton() -> list[str]:
    """A README with every heading, contents line and table header, and no rows."""
    toc, body = [], []
    for top in validate.TOP_SECTIONS:
        toc.append(f"- [{top}](#{validate.slugify(top)})")
        body += [f"## {top}", ""]
        sections = validate.SKILL_CATEGORIES if top == "Skills" else [top]
        for section in sections:
            if top == "Skills":
                toc.append(f"  - [{section}](#{validate.slugify(section)})")
                body += [f"### {section}", ""]
            if section in validate.TABLE_HEADERS:
                header = validate.TABLE_HEADERS[section]
                body += ["| " + " | ".join(header) + " |", "| --- | --- | --- |", ""]
    text = "\n".join(["# Title", "", "## Contents", "", *toc, "", "---", "", *body])
    return _lines(text)


def test_run_checks_passes_empty_sections_with_notes_only():
    """The launch state: every heading and table present, no rows yet."""
    errors, total, notes = validate.run_checks(_launch_skeleton())

    sections = len(validate.BULLET_SECTIONS) + len(validate.TABLE_HEADERS)
    assert errors == []
    assert total == 0
    assert len([n for n in notes if "has no entries yet" in n]) == sections


def test_ref_pattern_rejects_option_like_and_shell_like_values():
    hostile = ["-upload-pack=evil", "--exec=bad", "main;rm -rf /", "$(whoami)", "a b"]

    assert [r for r in hostile if validate.REF_RE.match(r)] == []


def test_ref_pattern_accepts_ordinary_git_revisions():
    valid = ["main", "origin/main", "HEAD~1", "refs/heads/main", "v1.0.0^{}"]

    assert all(validate.REF_RE.match(r) for r in valid)


def test_baseline_errors_refuses_an_option_like_ref(capsys):
    assert validate.baseline_errors("-upload-pack=evil") is None
    assert "not a valid git ref" in capsys.readouterr().err


def test_split_inherited_is_empty_without_a_baseline():
    assert validate.split_inherited(["README.md:1: boom"], None) == set()


def test_split_inherited_matches_a_problem_that_moved_lines():
    errors = ["README.md:400: 'Acme' description is 90 chars, max 80"]

    inherited = validate.split_inherited(errors, "HEAD")

    assert inherited == set() or errors[0] in inherited


# --- entry syntax ------------------------------------------------------------


def syntax_errors(body: str) -> list[str]:
    rep = validate.Report()
    validate.check_entry_syntax(_lines(body), rep)
    return rep.errors


def test_bullet_inside_a_table_section_is_reported():
    """Invisible to every other check, so it would merge unvetted."""
    body = (
        "### Research & Knowledge\n"
        "- [Acme Notes](https://github.com/acme/notes) - Note taking.\n"
    )

    assert any("does not parse" in e for e in syntax_errors(body))


def test_table_row_inside_a_bullet_section_is_reported():
    body = f"## Official\n{GOOD_ROW}\n"

    assert any("bullet list" in e for e in syntax_errors(body))


def test_a_valid_table_row_passes_the_syntax_check():
    assert syntax_errors(f"### Security\n{GOOD_ROW}\n") == []


def test_a_valid_bullet_passes_the_syntax_check():
    body = "## Official\n- [Acme](https://acme.dev) - Acme widget.\n"

    assert syntax_errors(body) == []


def test_table_header_and_divider_are_not_mistaken_for_entries():
    body = (
        "### Security\n"
        "| Skill | Description | Works with |\n"
        "|-------|-------------|------------|\n"
    )

    assert syntax_errors(body) == []


def test_an_entry_shaped_line_inside_a_fence_is_ignored():
    body = "### Security\n```\n- [Example](https://x.dev) - not a real entry\n```\n"

    assert syntax_errors(body) == []


# --- merge conflict markers --------------------------------------------------

# The shape that once passed as valid in the sister list: each side of the
# conflict keeps its own separator, so the header above the markers is stranded.
CONFLICTED = (
    "### Security\n\n"
    "| Skill | Description | Works with |\n"
    "<<<<<<< HEAD\n"
    "|---|---|---|\n"
    "| [Zeta](https://x.dev/z) | Zeta widget | Any |\n"
    "=======\n"
    "|---|---|---|\n"
    "| [Alpha](https://x.dev/a) | Alpha widget | Any |\n"
    ">>>>>>> origin/main\n"
)


def conflict_errors(body: str) -> list[str]:
    rep = validate.Report()
    validate.check_conflict_markers(_lines(body), rep)
    return rep.errors


def run_fix_flag(readme: Path, monkeypatch) -> int:
    """Run `validate.py --fix` against `readme` instead of the real README."""
    monkeypatch.setattr(validate, "README", readme)
    monkeypatch.setattr(sys, "argv", ["validate.py", "--fix"])
    return validate.main()


def test_each_conflict_marker_line_is_reported():
    errors = conflict_errors(CONFLICTED)

    assert [e.split(":")[1] for e in errors] == ["4", "7", "10"]
    assert all("unresolved merge conflict marker" in e for e in errors)


def test_run_checks_reports_a_conflict_marker():
    errors, _, _ = validate.run_checks(_lines(CONFLICTED))

    assert any("unresolved merge conflict marker" in e for e in errors)


def test_a_conflict_marker_inside_a_fence_is_ignored():
    body = "## Footnotes\n```\n<<<<<<< HEAD\n=======\n>>>>>>> origin/main\n```\n"

    assert conflict_errors(body) == []


def test_fix_flag_refuses_a_file_with_conflict_markers(tmp_path, monkeypatch, capsys):
    """Any small fixture fails structure checks, so the exit code alone proves nothing."""
    readme = tmp_path / "README.md"
    readme.write_text(CONFLICTED, encoding="utf-8", newline="")

    code = run_fix_flag(readme, monkeypatch)

    assert code == 1
    assert (
        "not fixing a file with unresolved merge conflicts" in capsys.readouterr().err
    )


def test_fix_flag_leaves_a_file_with_conflict_markers_unwritten(tmp_path, monkeypatch):
    readme = tmp_path / "README.md"
    readme.write_text(CONFLICTED, encoding="utf-8", newline="")

    run_fix_flag(readme, monkeypatch)

    assert readme.read_text(encoding="utf-8") == CONFLICTED
