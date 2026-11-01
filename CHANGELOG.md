# Changelog

Version headings below are documentation milestones. No git tag or GitHub release has been cut for any of them yet.

## [0.3.0] - 2026-11-01

Fixes from a whole-repository audit (2026-11-01). The first three closed ways for an entry to merge itself with nothing checked.

### Changed

- `check_submission.py` blocks what it cannot verify instead of noting it: a table row that links outside GitHub, a repository lookup that fails with anything but a 404 (a rate limit, a 5xx, a timeout), a tree it cannot list, and a truncated tree with no `SKILL.md` in it. A note never stopped auto-merge, so each of these merged with no `SKILL.md`, licence or activity check. A failed lookup clears on a re-run; the rest wait for a maintainer to check by hand and apply `maintainer-override`. CONTRIBUTING.md says so.
- A pull request that adds or removes any `README.md` line outside the skill and Collections table rows is held for a maintainer: a bullet in Official, Tools, Tutorials & Articles or Community under any list marker, a bare URL, an autolink, a reference link, HTML, a heading, a table row in a prose section, or prose itself. The gate read table rows only, so all of these passed as "No new entries" and merged themselves. Both sides go through `validate.py --fix` first, as the tidy bot would, so its sorting, re-padding and trimming never count; every other line is then compared in order as written, blank lines and indentation included, because four spaces turn a fence or a paragraph into code, a blank line ends a table and a second code fence swallows what follows. Only a table's header and separator lose their padding, which a wider row changes. Adding, editing or removing a table row still merges itself.
- `validate.py` keeps a table row's name, description and Works with plain text, by character rather than by link shape: a URL, a markdown link, `@` (GitHub autolinks an email on any domain), a backslash, `<`, `>` or an HTML entity (`&#64;` is an `@`) in one is an error, and so is a row with cells after Works with (a fourth cell, or an escaped `\|` that splits one), which GitHub renders and nothing read. So a link cannot ride inside a table row. The issue form refuses the same characters in a name or description. No listed entry had any.
- `validate.py` requires each skill and Collections table to be one block: the header, then the separator, then only entry rows, with no blank or other line inside. A blank line split a table, and a row moved above the separator became its header, while every row still parsed.
- `validate.py` rejects a control character (other than tab) or a Unicode line break (U+0085, U+2028, U+2029) anywhere in `README.md`, and `check_submission.py` now splits lines where `validate.py` and GitHub do. Python's `splitlines()` breaks on those characters and nothing else does, so a row hidden behind one was read by the gate and not by the validator.
- `CHANGELOG.md` no longer merges itself. The gate never read it, so a link added there merged unchecked; `README.md` is the one file a pull request can touch and still auto-merge.

### Fixed

- `auto-merge.yml` arms auto-merge with `--match-head-commit` on the event's head, after checking the head did not move while the changed files were read, so a push landing between the file check and the arm call can no longer be armed. A later change to a file outside the list, or the `no-auto-merge` or `maintainer-override` label, now switches off an auto-merge the workflow armed, so the label stops it as CONTRIBUTING.md says; one a maintainer armed by hand, and the bot pull requests that issue-to-pr.yml and tidy.yml arm, are left alone. Each GitHub read in that step is its own statement, so a failed call fails the step instead of reading as "not armed" or "no files". `star_check.py` pins its direct merge (`sha`) and its auto-merge (`expectedHeadOid`) to the head it checked.
- The health report stops with the error when GitHub's GraphQL API answers a batch with anything other than `NOT_FOUND`. A rate-limited batch had listed all 62 GitHub entries under "Gone: remove these".
- `check_new_links.py` retries a network error or a 5xx up to `max_retries` times, `retry_wait_time` seconds apart, both read from `lychee.toml` (3 and 5), as lychee does. One timeout had turned the required Check links red, which a contributor on a fork cannot re-run.
- On the site at 640px and below, buttons, tabs, category chips and selects are 44px tall (were 34 to 40px), the brand no longer wraps to two lines at 375px, and the sticky search sits under the bar instead of 4px beneath it. Cards on the Skills tab no longer run past a 375px screen: one long, unwrapped source line (`muratcankoylan/Agent-Skills-for-Context-Engineering`) had widened the single column to 405px on a 343px grid, clipping every card's right edge; it now ellipsizes.
- The pull request template's CONTRIBUTING.md link was relative, and GitHub keeps relative links as written in a pull request body, so it 404ed; it is a full URL now.
- `ruff` 0.16.6 to 0.17.3 and `pytest` 9.0.3 to 9.2.0, with `requirements-dev.txt` recompiled. Its regeneration command in `requirements-dev.in` now names `--python-version 3.14`, which the lock header has said since #2, instead of `.python-version`'s 3.15.

## [0.2.0] - 2026-11-01

### Added

- 51 entries, taking the list from 69 to 120: 10 in Development, 8 in Design & Frontend, 7 in Writing & Content, 6 in Research & Knowledge, 4 in Documents & Office, 2 in Productivity, 1 each in Testing & QA, Security and Skill Authoring, 7 Collections, 3 Official repositories (Anthropic's plugin directory, NVIDIA, Vercel) and 1 Tool. Candidates came from the repositories that the larger skill lists link to and from GitHub's `agent-skills`, `claude-skills` and `skills` topics, at 1,500 stars or more. Each table row passed `check_submission.py` with no blocking problem and no unreachable lookup; the four bullets, which the gate does not read, were checked by hand against the same bar. Repositories that only use skills for their own development were left out.

## [0.1.0] - 2026-11-01

The list's scaffolding, ported from the sister list [awesome-mcp-servers](https://github.com/Sagargupta16/awesome-mcp-servers) (2.10.3) and adapted from MCP servers to [Agent Skills](https://agentskills.io/). Every section is in place with an empty table or no bullets, ready for the first entries.

### Added

- `README.md` with the Official, Skills (11 categories), Collections, Tools, Tutorials & Articles and Community sections, the inclusion rules, a safety note, and a "Using a skill safely" footnote.
- A **Works with** column on every skill and collection row, from a fixed vocabulary: `Claude Code`, `Codex`, `Cursor`, `Gemini CLI`, `Copilot`, or `Any` on its own for a skill written to the open standard with no agent-specific parts. `validate.py` enforces it; the website filters by it, and picking an agent also shows the `Any` entries.
- `validate.py` notes an empty section instead of failing it, so the list validates while it is being filled.
- `check_submission.py` checks that the linked repository, or the folder inside one (`.../tree/<branch>/<path>`), holds a `SKILL.md` whose YAML frontmatter has a `name` and a `description`. It reads the shallowest five `SKILL.md` files from one recursive tree listing and passes on the first good one. A folder URL is searched on the branch it names; a folder that does not exist blocks. Specification notes that never fail the check: a `name` that is not lowercase letters, digits and single hyphens of at most 64 characters, a `name` that differs from its folder, a description over 1,024 characters, and an unquoted `name` or `description` containing `: `.
- Licences declared outside the root `LICENSE` file are accepted with a maintainer note: a package manifest field (as in the sister list), a `license` in `SKILL.md` that names a licence, or a licence file beside the skill when `license` points at one (`Complete terms in LICENSE.txt`). A `license` that withholds open-source terms, such as the specification's own example `Proprietary. LICENSE.txt has complete terms`, blocks even when the repository root is licensed. `is_open_source()` now also reads the first word of a value, so `Proprietary. ...` and `Commercial licence` are caught as well as the bare words.
- The README check accepts a README in the linked folder before the one at the root, and notes, without failing, a README that never mentions installing, setting up or using the skill.
- `staleness_report.py` resolves a missing root licence with the gate's own lookup, including the folder an entry links, so the monthly report and the gate cannot disagree.
- Tests for the SKILL.md frontmatter parser, folder URLs, the licence fallbacks, the Works with vocabulary, empty sections, and two drift guards that keep the issue form's Category and Works with options equal to `validate.py`.

### Changed from the sister list

- Every workflow sets `permissions: {}` or `contents: read` at the top and grants writes per job. `auto-merge.yml` and `health.yml` granted them workflow-wide.
- Every action is pinned to a full commit SHA with its version in a comment. The sister list pins only `lychee-action`, and uses major tags for `actions/checkout`, `actions/setup-python` and the Pages actions; those are pinned here to the commits their tags pointed at on 2026-11-01.
- `requirements-dev.txt` was recompiled for Python 3.15, the version in `.python-version`, with the command in `requirements-dev.in`.
- The website writes `skills.json` instead of `servers.json`, and its filter is Works with instead of Language.
- The thank-you bot's `NOT_BEFORE` is 2026-11-01.

### Not ported

- The `Remote` exception for hosted servers with no public source: the `Remote` Language value, CONTRIBUTING's hosted-server rules, the MCP `initialize` probe of a documented endpoint in `check_submission.py`, and the hosted-endpoint bucket of the health report. A skill is a folder of files, so there is nothing hosted to probe.
- The manifest-only stub check (`server.json`, `glama.json` and the like with no source beside them) and its build-manifest heuristic. The `SKILL.md` check replaces both.
- The Language column and its vocabulary, replaced by Works with.
- The Clients table and its MCP Support tiers, the Frameworks & Libraries section, and the Videos section. Collections and Tools take their place.
- The usage footnote with `mcpServers` JSON, replaced by "Using a skill safely".
- The `smithery.ai` exclusion in `lychee.toml`, an MCP registry this list has no reason to link.
- The orrery diagram of the submission pipeline (`docs/diagrams/`), which draws the MCP list's workflows.
- The MCP documentation and community links in the issue chooser, replaced by the Agent Skills specification.
