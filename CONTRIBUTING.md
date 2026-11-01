# Contributing to Awesome Agent Skills

Thanks for wanting to add to this list. **Anyone can contribute, including your own project.** That is the normal way entries get here.

The list aims to be a **curated** collection of [Agent Skills](https://agentskills.io/) -- folders with a `SKILL.md` that coding agents load on demand -- plus the collections, tools and guides around them. Not an exhaustive one. Curated means everything on it is a real skill, is maintained, and says how to use it. It does **not** mean famous: there is no minimum star count and no minimum project age. If you published a skill last week and it works, it belongs here.

Submissions are checked, and the checks are about whether the thing is real, not whether it is popular. CI runs them automatically, so you can see exactly where you stand before a maintainer looks.

## Table of Contents

- [Quick start](#quick-start)
- [Format](#format)
- [Categories](#categories)
- [Quality standards](#quality-standards)
- [What is not accepted](#what-is-not-accepted)
- [Submitting your own project](#submitting-your-own-project)
- [Pull request process](#pull-request-process)
- [Running the checks locally](#running-the-checks-locally)
- [Updating or removing an entry](#updating-or-removing-an-entry)
- [Reporting issues](#reporting-issues)

## Quick start

1. Read [quality standards](#quality-standards) and [what is not accepted](#what-is-not-accepted). Most declined pull requests fail one of those.
2. Fork the repo and branch off `main`.
3. Add **one** row to the most appropriate existing category in `README.md`. Alphabetical order is preferred but not required.
4. Run `python scripts/validate.py` and fix anything it reports.
5. **Star the repository.** A pull request only merges itself once its author has starred.
6. Open a pull request and fill in the template, including the affiliation question.

Rather not use git? The [skill suggestion form](https://github.com/Sagargupta16/awesome-skills/issues/new?template=add-skill.yml) does all of that for you: see [submitting your own project](#submitting-your-own-project).

## Format

Entries in the skill categories and in **Collections** are table rows in this exact shape:

```
| [Name](URL) | Description | Works with |
```

You do not need to line up the pipes with the rows around yours. The tables are padded so the list passes [awesome-lint](https://github.com/sindresorhus/awesome-lint), and a bot re-pads them after new rows land. When a row wider than the rest widens its table, that re-padding can leave an open pull request in conflict with `main`; merging `main` into your branch, keeping `main`'s version of the table plus your row, and running `python scripts/validate.py --fix` clears it, or a maintainer can.

- **Name** -- the skill or collection name, as a user would recognise it. Keep it short.
- **URL** -- a direct `https://` link to the repository, or to the skill's folder inside one (`https://github.com/org/repo/tree/main/skills/foo`). Link the folder when the repository holds several skills and you are adding one of them. No tracking parameters, no redirect shorteners. The checks read GitHub, so a skill hosted anywhere else is held for a maintainer to check by hand.
- **Description** -- what it does, in **80 characters or fewer**. Start with a capital letter. No trailing period. No em-dash or en-dash; write `--` or `-` instead. Describe the function, not the pitch: "Review pull requests for security and style issues" rather than "The ultimate AI code reviewer".
- **Works with** -- the agents the skill supports, comma-separated, from exactly this list: `Claude Code`, `Codex`, `Cursor`, `Gemini CLI`, `Copilot`, or `Any`. Name an agent when the skill's README says it supports it or you have run it there. Use `Any` on its own, and only when the skill sticks to the open standard: plain `SKILL.md` frontmatter, and instructions and scripts that assume no one agent's tools, commands or plugin format.

Example:

```markdown
| [Acme Review](https://github.com/acme/skills/tree/main/review) | Review pull requests against the Acme style guide | Claude Code, Codex |
```

The `Official`, `Tools`, `Tutorials & Articles`, and `Community` sections are bullet lists instead:

```markdown
- [Name](URL) - Description ending in a period.
```

## Categories

Add your skill to the most appropriate **existing** category:

| Category | Scope |
| --- | --- |
| Development | Coding workflows, refactoring, code review, languages and frameworks, git |
| Testing & QA | Writing and running tests, browser testing, accessibility, debugging |
| DevOps & Cloud | CI/CD, containers, infrastructure as code, cloud providers, deploys |
| Data & Databases | SQL, data analysis, notebooks, warehouses, data pipelines |
| Documents & Office | PDF, Word, spreadsheets, slides, document conversion |
| Design & Frontend | UI design, CSS, components, diagrams, images, animation |
| Security | Security review, secrets, threat modelling, audits |
| Writing & Content | Docs, blogs, editing, commit messages, release notes |
| Research & Knowledge | Web research, citations, summaries, knowledge bases, notes |
| Productivity | Planning, task tracking, email, calendars, workflow automation |
| Skill Authoring | Writing, testing and packaging skills themselves |

Beyond the skill categories, the list also has **Official** (vendor-maintained skill repositories and the specification), **Collections** (multi-skill packs and plugin marketplaces, listed once as a whole), **Tools** (validators, linters, installers, registries), **Tutorials & Articles**, and **Community**.

**New categories need an issue first.** Open one describing what does not fit and roughly how many existing entries would move. Do not add a category in a pull request -- CI rejects unknown headings, because the category list lives in `scripts/validate.py`.

### Alphabetical order

Tables are kept alphabetical by name, case-insensitively and ignoring leading punctuation. This is a **preference, not a gate**: putting a row in the wrong place produces a note, never a failing check, because where a row sits says nothing about whether the skill is real. `python scripts/validate.py --fix` sorts everything for you, and a maintainer runs it periodically anyway.

## Quality standards

Every submission must meet all of these. CI checks the mechanical ones automatically and reports the rest for a maintainer. What CI cannot verify is held rather than passed: a link outside GitHub, a lookup that failed, or a repository tree too large to read. A failed lookup clears when the check is re-run; for the others a maintainer checks by hand and applies `maintainer-override`.

1. **It really is a skill.** The linked repository, or the linked folder inside one, holds at least one `SKILL.md` whose YAML frontmatter has a `name` and a `description`, as the [specification](https://agentskills.io/specification) requires. For a collection, one good `SKILL.md` anywhere in it is enough. A repository of prompts, rules files or links to skills elsewhere is not a skill.
2. **Open source with a stated licence.** The skill must state its licence somewhere a reader can find it: a `LICENSE` file at the repository root; a licence field in a package manifest at the root (`package.json`, `pyproject.toml`, `Cargo.toml`, `pom.xml`, `composer.json`, `deno.json`); a `license` field in the skill's `SKILL.md` that names a licence; or a licence file (`LICENSE`, `LICENSE.txt`, `LICENCE.md`, `COPYING`) in the skill's folder or a folder above it. The specification lets `license` point at a bundled file, as in `license: Complete terms in LICENSE.txt`, and the check then looks for that file. A root `LICENSE` file is what GitHub reads for the sidebar, so it is still the better option; the others get flagged for a maintainer to read. If GitHub cannot classify the root file -- the sidebar reads "unknown" and the API reports `NOASSERTION` -- that is not an automatic rejection either, but a maintainer will read the terms by hand. No licence anywhere is a rejection, and so is a value that withholds open-source terms instead of granting them: npm's `UNLICENSED`, `SEE LICENSE IN <file>` in a package manifest, or `Proprietary` in a manifest or in `SKILL.md`, including the specification's own example `Proprietary. LICENSE.txt has complete terms`. A `SKILL.md` that says `Proprietary` is rejected even when the repository root has an open-source `LICENSE`, since the skill's own terms are the more specific ones.
3. **Documented.** A README, in the linked folder or at the repository root, that says what the skill does and how to install or use it.
4. **Maintained.** Pushed within the last **180 days**, and not archived.
5. **Usable by someone else.** A reader should be able to follow your README and get the skill working in the agents the row names. That is the bar, not popularity: there is **no minimum star count and no minimum project age**. A three-day-old skill with ten stars, a licence and clear install steps is a better entry than a famous repository nobody can install.
6. **Not a duplicate.** Not already listed, and not a second copy of a skill already covered. If yours is genuinely better than the listed one, say why in the pull request and propose replacing it.
7. **Not a fork.** Submit the upstream project.

CI also reads the `SKILL.md` it found against the specification and notes, without failing anything, a `name` that is not lowercase letters, digits and single hyphens of at most 64 characters, a `name` that differs from its folder, a description over 1,024 characters, and an unquoted `name` or `description` containing `: `, which strict YAML parsers reject.

Entries that stop meeting these get removed. A monthly [health workflow](.github/workflows/health.yml) posts dead links, archived projects, missing licences and stale entries into a tracking issue.

## What is not accepted

Short list, and none of it is about how big your project is:

- **Repositories with no `SKILL.md`.** A prompt library, a `.cursorrules` or `AGENTS.md` file, slash-command files, or a list of links to skills elsewhere. A plugin marketplace qualifies as a collection only when it holds at least one skill itself.
- **Undisclosed self-promotion.** Submitting your own work is welcome and common. Just tick the affiliation box.
- **Nothing about how many skills you add at once.** One per pull request is preferred and CI will say so, but it does not fail the check, and a batch of genuinely good entries is not a reason to decline.
- **Skills that hide what they do**: obfuscated scripts, or instructions that fetch and run remote code without saying so. Report a listed one privately, as [SECURITY.md](SECURITY.md) describes.
- **Descriptions written as marketing copy.** Say what it does. This is usually a one-line fix, not a rejection.
- **Changes that remove or reorder unrelated entries** alongside your addition.

If a submission is declined it will say which of these applies and what would change the answer. "Too new" and "too few stars" are not on the list and will not be the reason.

## Submitting your own project

That is fine and normal -- much of this list exists because authors submitted their own work. Two requirements:

1. **Disclose it.** Tick the affiliation box in the pull request template. That is all: the disclosure is not held against you, it just means nobody has to guess. Self-promotion that was hidden and later discovered gets the entry removed, which is the only reason this matters.
2. **Meet the same bar as everyone else.** A real `SKILL.md`, a licence, documentation, maintenance. Being the author neither helps nor hurts.

Being new is not a reason to hold back. If you would rather not open a pull request, the [skill suggestion form](https://github.com/Sagargupta16/awesome-skills/issues/new?template=add-skill.yml) works just as well: for a skill or a collection, a bot turns the form into the same one-row pull request, runs the same checks, and merges it when they pass and you have starred the repository. If a field breaks a rule it comments on the issue, and editing the issue retries. The bullet sections are added by a maintainer, and a pull request that adds any link outside the skill tables is held for one.

## Pull request process

1. **One skill per pull request, preferred.** It keeps review and revert independent. This is a preference, not a gate: CI notes the count and carries on, so a pull request adding several good entries still comes back green. A maintainer may still ask you to split a large one.
2. Branch off `main`, add your row, and commit with a clear message such as `Add Acme Review to Development`.
3. Fill in the pull request template, including the affiliation question.
4. Make sure all checks pass:
   - **Validate format** -- structure, duplicates, description length, the Works with list
   - **Check links** -- every URL resolves
   - **Check submitted entries** -- the `SKILL.md`, licence, maintenance and archived state; it holds any other new link (a bullet, a link in prose), or a row it cannot verify, for a maintainer

   On a pull request, **Validate format** only fails on problems your change
   introduces. If `main` already has a bad row, it is listed for the record but
   marked as pre-existing and does not count against you.
5. **It merges itself once you have starred.** If your pull request only touches `README.md` or `CHANGELOG.md` and you have starred the repository, auto-merge is switched on for you: GitHub squash-merges it the moment every required check passes. No approval, no waiting for a maintainer to be awake. It will not merge while any required check is red, star or not.

A maintainer still reads what lands, and may follow up if a description reads promotionally or it is unclear what the skill does. Four things keep a pull request from merging itself:

- **It touches anything beyond the list** -- a workflow, a script, a test, tooling config. Those change what the checks verify, so a person looks first.
- **It adds a link outside the skill tables, or a row the checks cannot verify.** Only a table row is checked for a `SKILL.md`; the bullet sections hold vendor repositories, tools and articles, and a link outside GitHub has no `SKILL.md` the checks can read. **Check submitted entries** stays red until a maintainer reviews it, applies `maintainer-override` and merges it by hand.
- **You have not starred the repository.** A star is required before a pull request merges itself. Without one it waits, marked `missing-star`, and starring releases it: the label comes off and it merges once the checks pass. A maintainer can also merge it by hand. A star never gets an entry past a failing check.
- **It carries the `maintainer-override` label**, which bypasses the submission gate. That is a maintainer's judgement call, so whoever applied it merges by hand.

Anyone can also stop auto-merge on a specific pull request by adding the `no-auto-merge` label.

Maintainers can apply the `maintainer-override` label when a submission is genuinely fine but trips a threshold.

### When you open it

If you have not starred the repository, a bot adds the `missing-star` label and comments once to ask. A star is required before your pull request merges itself, so until you star it waits. The label comes off by itself when you do, the comment turns into a thank-you, and the pull request merges once the checks pass.

### After it merges

Within the hour, a bot comments once on your pull request (or on your issue, if you used the form) with a link to your entry on the [website](https://sagargupta.online/awesome-skills/) and a badge for your project's README:

```markdown
[![Listed in Awesome Agent Skills](https://sagargupta.online/awesome-skills/badge.svg)](https://github.com/Sagargupta16/awesome-skills)
```

The badge links back to the list, so people who find your skill can find the others. The badge is optional. Edits to an existing entry, such as a reworded description, get no comment.

## Running the checks locally

```bash
python scripts/validate.py
```

```bash
python scripts/validate.py --fix
```

`--fix` repairs alphabetical order, table alignment, trailing whitespace, and dashes. Everything else -- an over-long description, a duplicate, an unknown category, an agent outside the Works with list -- needs a real edit. It will not touch a file that still has merge conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`), because re-padding would mangle the table around them: resolve the conflict first. `validate.py` reports any marker left behind as an error.

To preview the submission gate the way CI runs it:

```bash
GITHUB_TOKEN=$(gh auth token) python scripts/check_submission.py --base-ref origin/main
```

The link check needs [lychee](https://github.com/lycheeverse/lychee):

```bash
lychee --config lychee.toml README.md CONTRIBUTING.md
```

## Updating or removing an entry

**Updating** -- open a pull request and explain what changed. Renames, moved repositories, new agents in Works with, and corrected descriptions are all welcome, and correcting someone else's entry is a genuinely useful contribution.

**Removing** -- if a listed skill is dead, archived, no longer holds a `SKILL.md`, or has become malicious, open an issue or a pull request that says which and why. Removals need a stated reason: people rely on this list, so entries are not dropped silently.

## Reporting issues

Use the [issue templates](https://github.com/Sagargupta16/awesome-skills/issues/new/choose) to suggest a skill, report a broken link, propose a category, or raise anything else.

Found something on this list that behaves maliciously? That is a security matter -- see [SECURITY.md](SECURITY.md) and report it privately rather than in a public issue.

## Code of Conduct

This project follows the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md). By participating you agree to uphold it.

---

Thanks for helping keep this list worth reading.
