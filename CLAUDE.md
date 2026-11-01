# CLAUDE.md

> This file stacks on top of the workspace root at `C:\Code\GitHub\`:
> - Root [`CLAUDE.md`](../../CLAUDE.md) -- voice, rules, routing map, references, skills, slash commands, conventions.
> - Root [`MEMORY.md`](../../MEMORY.md) -- live facts across repos.
> - Root [`STATUS.md`](../../STATUS.md) -- live PR/CI/security dashboard.
> - [`.claude/resources/`](../../.claude/resources/README.md) -- deep reference for collaboration, workflow, git, OSS, debugging, voice.
>
> Read those first. The guidance below only adds **repo-specific context** -- it does not override anything in the root.

## Project

Curated awesome-list of Agent Skills (folders with a `SKILL.md` that Claude Code, Codex, Cursor, Gemini CLI, Copilot and other agents load on demand; open standard at agentskills.io), plus collections, tools and guides, maintained by Sagar and open to community PRs. `README.md` is the product; `scripts/` is the machinery that keeps its promises true.

Sister list of `community/awesome-mcp-servers`, whose system this is ported from (CHANGELOG 0.1.0 lists what was dropped). A fix to a shared script or workflow there usually belongs here too, and the reverse.

## Stack

- **Language**: Markdown (the list) plus Python (the gate scripts in `scripts/`, stdlib only)
- **Framework**: none
- **Database**: none
- **Package manager**: none for the list; `requirements-dev.in` / `requirements-dev.txt` hash-lock `ruff` and `pytest` for the scripts
- **Deploy target**: the GitHub README, plus a static site on GitHub Pages at https://sagargupta.online/awesome-skills/ built from it by `scripts/build_site.py` (`site/` holds the template, CSS and JS; output `_site/` is gitignored)

## Run

```bash
python scripts/validate.py          # structure, format, Works with, duplicates, conflict markers (ordering and empty sections are notes)
python scripts/validate.py --fix    # auto-repair ordering, table alignment, whitespace, dashes; refuses a file with conflict markers
npx --yes awesome-lint README.md     # sindresorhus/awesome's linter; pass the RELATIVE name (an absolute C:\ path reads as a URL)
GITHUB_TOKEN=$(gh auth token) python scripts/check_submission.py --base-ref origin/main
python scripts/check_new_links.py --base-ref origin/main   # only the links a change adds
GITHUB_TOKEN=$(gh auth token) python scripts/thank_contributors.py --dry-run   # who the thank-you bot would comment on
GITHUB_TOKEN=$(gh auth token) python scripts/staleness_report.py
GITHUB_TOKEN=$(gh auth token) python scripts/build_site.py      # site into _site/; without a token it builds with no stars
python -m http.server 8766 --directory _site                   # preview it
```

`.python-version` (3.15) is the interpreter every workflow installs via `python-version-file`.

## Test

```bash
uv venv --python "$(cat .python-version)"
uv pip install --require-hashes -r requirements-dev.txt
.venv/Scripts/python -m pytest -q
.venv/Scripts/ruff check scripts tests
.venv/Scripts/ruff format --check scripts tests
```

`requirements-dev.txt` is a uv-generated universal hash lock; `requirements-dev.in` is the source and carries the regeneration command. Both the pin and `ruff.toml`'s rule set exist so `ruff format --check` cannot flip on a formatter release.

Nine workflows, the same names and behaviour as the sister list:

- [lint.yml](.github/workflows/lint.yml) -- `Validate format` (README structure), `Lint and test the gate scripts` (ruff + pytest), `Check links` (lychee over README, CONTRIBUTING, SECURITY, CHANGELOG). PRs to `main`, pushes to `main`, daily 06:00 UTC.
- [submission-check.yml](.github/workflows/submission-check.yml) -- `Check submitted entries`: the rows a PR adds, against the GitHub API (SKILL.md frontmatter, licence, last push, archived, fork, README). Honours `maintainer-override`. No `paths` filter on purpose: it is a required check, and a path-filtered required check never reports, which hangs auto-merge.
- [auto-merge.yml](.github/workflows/auto-merge.yml) -- arms GitHub auto-merge on `pull_request_target` for PRs touching only `README.md` (not `CHANGELOG.md`, which the gate never reads) whose author has starred, pinned with `--match-head-commit` to the head whose files it read, and switches off an auto-merge it armed (enabled by `github-actions`) when a later file change or a `no-auto-merge` / `maintainer-override` label makes the PR ineligible; never checks out PR code. `star_check.py` pins its merge and auto-merge to the checked head the same way.
- [health.yml](.github/workflows/health.yml) -- monthly (1st, 06:00 UTC) audit of every listed repository into one `maintenance` issue.
- [pages.yml](.github/workflows/pages.yml) -- builds and deploys the site on push, on `workflow_run` of Lint, Submission check, Auto merge and Star check (only when `main` moved past the last deployed sha), and hourly as a fallback.
- [issue-to-pr.yml](.github/workflows/issue-to-pr.yml) -- turns a "Suggest a skill" form (label `addition`) for a skill category or Collections into a one-row PR on `submission/issue-N` via `scripts/issue_to_pr.py`, dispatches `lint.yml` and `submission-check.yml` on the branch, arms auto-merge only if the submitter starred, and an hourly sweep closes merged issues with the thank-you text.
- [thanks.yml](.github/workflows/thanks.yml) -- one thank-you per merged contributor PR, with the site link and the "Listed in" badge; marker `<!-- awesome-skills:thanks -->`, `NOT_BEFORE` 2026-11-01.
- [tidy.yml](.github/workflows/tidy.yml) -- runs `validate.py --fix` on main and opens or refreshes one `chore/tidy-readme` PR with auto-merge armed.
- [star-check.yml](.github/workflows/star-check.yml) -- `missing-star` label and one marker comment on unstarred PRs; on `watch` releases the starrer's held PRs and approves their held runs.

## Entry points

- `README.md` -- the entire list: Official, Skills (11 categories), Collections, Tools, Tutorials & Articles, Community, then Contributing and Footnotes. awesome-lint shapes it: the Awesome badge on the H1, the blockquote describes Agent Skills rather than the list, Contents is the first `##` section, no License section, every list item is `[link](url) - description`, every table pipe-aligned (`validate.py --fix`). Prose that is not part of the list lives under `## Footnotes`; `###` headings under a prose section are not categories.
- `CONTRIBUTING.md` -- entry format, Works with vocabulary, category table, quality standards, PR process
- `scripts/validate.py` -- the format contract, in code. `SKILL_CATEGORIES` is the canonical category list and `WORKS_WITH` the canonical agent list.

## Key files

- `scripts/check_submission.py` -- the submission gate. `find_skill()` (tree listing plus up to `MAX_SKILL_FILES` SKILL.md reads), `parse_frontmatter()` (stdlib YAML subset), `declared_licence()` (manifest, SKILL.md `license`, licence file beside the skill), `check_readme()`
- `scripts/staleness_report.py` -- imports `find_skill`, `declared_licence` and `is_open_source`, so the report and the gate cannot disagree
- `scripts/thank_contributors.py` -- post-merge thank-you; `BADGE_URL` and `BADGE_MARKDOWN` live in `scripts/build_site.py`
- `scripts/star_check.py` -- the star ask and the star requirement
- `scripts/gitref.py` -- the one safe `git show <ref>:<path>` and ref-shape guard for all three `--base-ref` scripts
- `site/badge.svg` -- the "Listed in" badge, served from the Pages site
- `.github/ISSUE_TEMPLATE/add-skill.yml` -- the submission form; a test keeps its Category and Works with options equal to `validate.py`
- `tests/` -- pytest suite for every script, plus drift guards for CONTRIBUTING's category table and the issue form

## Gotchas

- Auto-merge is the only merge path for content PRs and the checks are the only gate, so the required-check list on the `main` ruleset is load-bearing: `Validate format`, `Lint and test the gate scripts`, `Check links`, `Check submitted entries`, and the GitGuardian app's `GitGuardian Security Checks`. Adding a `paths` filter to a required check, or renaming a job, silently breaks it. Change a job name and the ruleset in the same pass.
- An auto-merged PR produces **no push-to-main run** (`GITHUB_TOKEN` pushes start none), so the daily `lint.yml` schedule is the only thing holding `main` to the full bar. Anything that must follow a merge hangs off `workflow_run` of Lint, Submission check, Auto merge and Star check; the crons are a fallback GitHub throttles to every 3 to 7 hours.
- A PR opened with `GITHUB_TOKEN` gets its own `pull_request` runs as `action_required`, so form and tidy PRs wait for Sagar to approve them even though the dispatched checks are green. The form also fires `opened` and `labeled` together, so the workflow triggers on `opened` and `edited` only. Auto-merge on `GITHUB_TOKEN` does not apply `Closes #N`; the sweep closes issues.
- The link check is split by event: on a PR only `check_new_links.py` can fail it; on push, schedule and dispatch lychee sweeps with `fail: true`. `lychee.toml` is the single source of accept codes (405 kept from the sister list) and exclusions (x.com, twitter.com, linkedin.com, discord.gg).
- `parse_frontmatter()` reads the YAML subset SKILL.md files use (plain, quoted, `>`/`|` blocks, indented continuations) and is not a YAML parser. A plain value containing `: ` is flagged soft, because strict parsers reject it. Do not add PyYAML: the scripts are stdlib only and CI installs only the hash lock.
- Folder URLs must be `https://github.com/<owner>/<repo>/tree/<ref>/<path>` with a one-segment ref. A branch with a slash reads as ref plus folder, the tree lookup fails, and the gate goes red with that hint. Anything the gate cannot verify (a link outside GitHub, a non-404 API error, an unreadable or truncated tree, and any README line added or removed outside the skill and Collections table rows, compared in order (`difflib`) as written after `validate.py --fix` runs on both sides, blank lines and indentation included, with only table headers and separators losing their padding) is a blocking finding. `validate.py` keeps names, descriptions and Works with plain text by character (`LINKISH_RE`: URLs, links, `@`, backslash, `<`, `>`, HTML entities), refuses a row with cells after Works with, and requires each table to be one header, separator and rows block (`check_table_shape`), so a link cannot ride inside a row either. Both scripts must split lines the same way: `check_submission.readme_lines()` splits as `validate.py` and GitHub do, and `check_stray_characters` rejects the form feeds and U+2028-style breaks that `str.splitlines()` alone honours. Never type those characters as escapes into a tool call; build them with `chr()`, because a soft note never stops auto-merge; a maintainer clears it with `maintainer-override`. `.`, `..` and encoded `/` segments are refused before they reach an API path.
- A collection passes on its first good SKILL.md, shallowest first; the licence and spec notes are judged on that skill only. A big monorepo (`anthropics/skills`) can fail at the root while its folders pass, because its licences sit beside each skill.
- A `license` that names a bundled file (`Complete terms in LICENSE.txt`, `LICENSE.txt`) is a pointer, followed to a licence file in the skill's folder or a folder above it, below the root. A `license` whose first word is `Proprietary`, `Commercial`, `Unlicensed` and so on blocks even under an open-source root `LICENSE`.
- The submission gate hard-fails at 181 days since last push. Incumbents are held to the same bar through the monthly health report.
- The stargazer list needs authentication. `star_check.py` tries `STARGAZERS_TOKEN`, then `GITHUB_TOKEN`, then the author's public starred list (20 pages, misses heavy starrers; a miss fails safe). In the sister list `GITHUB_TOKEN` reads it, so no secret is set; a log line "stargazer list unavailable" means a read-only fine-grained `STARGAZERS_TOKEN` is needed.
- Fork PR workflow approval should be `first_time_contributors_new_to_github` (repo setting, not in version control). `star_check.py` approves held runs for a starred, list-only PR head it checked twice.
- `renovate.json` extends `Sagargupta16/shared-workflows` and switches the pip manager off, because it bumps pins without regenerating the `--hash=` block. Bump `requirements-dev.in` and run its compile command instead.
- No git tag or GitHub release exists for any CHANGELOG version.

## Repo-specific rules

- Follow `CONTRIBUTING.md` when adding entries: most-appropriate existing category, Works with only from `WORKS_WITH`, `Any` alone and only for skills with no agent-specific parts. One-per-PR and ordering are preferences, not gates.
- Only add entries meeting the bar: a SKILL.md with `name` and `description`, an open-source licence, a README that says how to install or use it, pushed within 180 days, not archived, not a fork, not a duplicate.
- Don't remove entries without a stated reason (dead link, archived, no SKILL.md, over 180 days, no licence, malicious).
- New categories need an issue first. Adding one means editing `SKILL_CATEGORIES`, the CONTRIBUTING table, the README Contents and headings, and the issue form's Category options together; tests fail if they disagree.
- Changing a rule in `CONTRIBUTING.md` means changing `scripts/check_submission.py` in the same commit. A documented bar the gate does not enforce, or a gate stricter than the docs, is the defect the sister list kept producing.
