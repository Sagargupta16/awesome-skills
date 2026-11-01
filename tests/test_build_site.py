"""Tests for scripts/build_site.py, the website built from README.md."""

from __future__ import annotations

from datetime import datetime, timezone

import build_site
import validate

SNIPPET = """
## Official

- [Agent Skills Specification](https://agentskills.io/specification) - The open SKILL.md format.

## Skills

### Development

| Skill | Description | Works with |
|-------|-------------|------------|
| [Acme Review](https://github.com/acme/review) | Reviews acme code | Claude Code, Codex |
| [Mono Skill](https://github.com/org/mono/tree/main/skills/mono) | Lives in a repository folder | Any |

### Security

| Skill | Description | Works with |
|-------|-------------|------------|
| [Evil <script>](https://example.com/x?a=1&b=2) | Quotes " and <tags> | Cursor |

## Collections

| Collection | Description | Works with |
|------------|-------------|------------|
| [Some Pack](https://github.com/c/pack) | A pack of skills | Claude Code |

## Tools

- [Skill Lint](https://github.com/t/lint) - Lints SKILL.md files.
"""


def _items():
    return build_site.load_items(SNIPPET.strip("\n").splitlines(True))


def _page(template: str) -> str:
    return build_site.render_page(
        _items(), template, datetime(2026, 11, 1, tzinfo=timezone.utc)
    )


def test_items_carry_their_tab_category_and_agents():
    by_name = {i.name: i for i in _items()}

    assert by_name["Acme Review"].tab == "skills"
    assert by_name["Acme Review"].category == "Development"
    assert by_name["Acme Review"].works_with == ["Claude Code", "Codex"]
    assert by_name["Some Pack"].tab == "collections"
    assert by_name["Skill Lint"].tab == "tools"
    assert by_name["Skill Lint"].works_with == []
    assert by_name["Agent Skills Specification"].tab == "official"


def test_github_slug_handles_repo_roots_and_folders():
    assert build_site.github_slug("https://github.com/acme/review") == "acme/review"
    assert build_site.github_slug("https://github.com/acme/skill.git") == "acme/skill"
    assert (
        build_site.github_slug("https://github.com/org/mono/tree/main/skills/mono")
        == "org/mono"
    )
    assert build_site.github_slug("https://example.com/org/repo") == ""


def test_star_counts_are_short():
    assert build_site._stars(None) == ""
    assert build_site._stars(950) == "950"
    assert build_site._stars(1000) == "1k"
    assert build_site._stars(187076) == "187.1k"


def test_rendered_page_escapes_entry_text():
    page = _page("<main>{{CARDS}}</main><p>{{SKILL_COUNT}} {{CATEGORY_COUNT}}</p>")

    assert "<script>" not in page
    assert "Evil &lt;script&gt;" in page
    assert "a=1&amp;b=2" in page
    assert "<p>3 2</p>" in page  # three skills across two categories


def test_each_agent_gets_its_own_chip_and_the_card_lists_them():
    page = _page("{{CARDS}}")

    assert (
        '<span class="chip">Claude Code</span><span class="chip">Codex</span>' in page
    )
    assert 'data-agents="Claude Code,Codex"' in page


def test_the_agent_filter_offers_only_named_agents_in_vocabulary_order():
    page = _page("{{AGENT_OPTIONS}}")

    values = [a for a in validate.WORKS_WITH if f'value="{a}"' in page]
    assert values == ["Claude Code", "Codex", "Cursor", "Any"]
    assert "Any agent (open standard)" in page


def test_the_skills_tab_shows_even_with_no_skills():
    """The list launched empty; the page still needs somewhere to land."""
    page = build_site.render_page(
        [], "{{TABS}}", datetime(2026, 11, 1, tzinfo=timezone.utc)
    )

    assert 'data-tab="skills"' in page
    assert 'data-tab="collections"' not in page


def test_every_placeholder_in_the_real_template_is_filled():
    template = (build_site.SITE_SRC / "index.html").read_text(encoding="utf-8")

    assert "{{" not in _page(template)


def test_the_real_readme_builds():
    lines = (build_site.ROOT / "README.md").read_text(encoding="utf-8").splitlines(True)
    items = build_site.load_items(lines)

    tabs = {key for key, _, _ in build_site.TABS}
    assert all(i.tab in tabs for i in items)
    assert all(
        validate.works_with_problem(", ".join(i.works_with)) is None
        for i in items
        if i.tab in build_site.TAGGED
    )
