# Changelog

Version headings below are documentation milestones. No git tag or GitHub release has been cut for any of them yet.

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
