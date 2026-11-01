# Awesome Agent Skills [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

> [Agent Skills](https://agentskills.io/) are folders of instructions, scripts and resources, each with a `SKILL.md` file, that coding agents such as Claude Code, Codex, Cursor, Gemini CLI and GitHub Copilot load on demand. The format is an open standard.

**Browse it as a searchable site: [sagargupta.online/awesome-skills](https://sagargupta.online/awesome-skills/)**, with search, category and agent filters, and live stars. It is rebuilt from this README every hour.

**This list is curated, not exhaustive, and open to anyone.** The point of it is that everything on it has been checked. Curated does not mean famous: your project needs no minimum star count or age, and submitting your own skill is welcome. Every entry:

- is a real skill -- the linked repository, or the folder inside one, holds at least one `SKILL.md` whose frontmatter has a `name` and a `description`
- states an open-source licence -- a `LICENSE` file, or a licence field in its package manifest or its `SKILL.md`
- was pushed within the last 180 days, and is not archived
- has a README that says how to install or use the skill
- appears exactly once, in one category

Those rules are enforced by [CI](.github/workflows/), not by good intentions: a pull request that breaks the format, adds a dead link, or submits a repository with no `SKILL.md` or no licence fails its checks. A [monthly audit](.github/workflows/health.yml) re-checks every listed repository and files what has rotted.

A skill can run scripts on your machine and shapes what your agent does with your files and credentials. Read its `SKILL.md` and its scripts before you install it -- a place on this list is a filter, not an audit. See [using a skill safely](#using-a-skill-safely) and [SECURITY.md](SECURITY.md).

## Contents

- [Official](#official)
- [Skills](#skills)
  - [Development](#development)
  - [Testing & QA](#testing--qa)
  - [DevOps & Cloud](#devops--cloud)
  - [Data & Databases](#data--databases)
  - [Documents & Office](#documents--office)
  - [Design & Frontend](#design--frontend)
  - [Security](#security)
  - [Writing & Content](#writing--content)
  - [Research & Knowledge](#research--knowledge)
  - [Productivity](#productivity)
  - [Skill Authoring](#skill-authoring)
- [Collections](#collections)
- [Tools](#tools)
- [Tutorials & Articles](#tutorials--articles)
- [Community](#community)

---

## Official

Skill repositories maintained by the company behind the product or agent they cover, and the specification itself.

- [Agent Skills specification](https://agentskills.io/specification) - The open format: SKILL.md rules, the clients that support it and guides for skill authors.
- [Anthropic skills](https://github.com/anthropics/skills) - Anthropic's public skills for documents, design, MCP and skill creation. Most are Apache-2.0; the four document skills are source-available.
- [Cloudflare skills](https://github.com/cloudflare/skills) - Skills that teach agents to build on Cloudflare, with plugin installs for Claude Code, Codex and Cursor.
- [GitHub awesome-copilot](https://github.com/github/awesome-copilot) - GitHub's community collection of skills, agents and instructions for Copilot.
- [Google skills](https://github.com/google/skills) - Skills for Google products, including Google Cloud and the Gemini API.
- [Google Stitch skills](https://github.com/google-labs-code/stitch-skills) - Skills that pair with the Stitch MCP server for design-to-code work.
- [Hugging Face skills](https://github.com/huggingface/skills) - Skills for working with the Hugging Face ecosystem and its CLI.
- [Microsoft skills](https://github.com/microsoft/skills) - Skills and agent guidance for Azure and Microsoft Foundry SDKs.
- [OpenAI skills](https://github.com/openai/skills) - The Codex skills catalog, split into curated and system skills and licensed per skill.
- [Sentry skills](https://github.com/getsentry/skills) - Skills the Sentry team uses for its own development, such as commits and settings audits.
- [Stripe AI](https://github.com/stripe/ai) - Stripe's agent toolkit, which includes skills for building with Stripe.
- [Supabase agent skills](https://github.com/supabase/agent-skills) - Skills that help agents build on Supabase.

## Skills

One skill per row. **Works with** names the agents a skill supports; `Any` means it sticks to the open standard and has no agent-specific parts.

### Development

| Skill                                                                  | Description                                                                     | Works with                                      |
| ---------------------------------------------------------------------- | ------------------------------------------------------------------------------- | ----------------------------------------------- |
| [Addy Osmani agent skills](https://github.com/addyosmani/agent-skills) | Production-minded engineering skills covering requirements, review and delivery | Any                                             |
| [Anthony Fu skills](https://github.com/antfu/skills)                   | Anthony Fu's skills for Vue, Nuxt, Vite, Vitest, Pinia, UnoCSS and pnpm         | Any                                             |
| [Expo skills](https://github.com/expo/skills)                          | Skills for building and shipping Expo apps and using Expo Application Services  | Claude Code, Codex, Cursor                      |
| [Firebase agent skills](https://github.com/firebase/agent-skills)      | Firebase skills, shipped as a Gemini CLI extension and as plugins               | Claude Code, Codex, Gemini CLI                  |
| [gstack](https://github.com/garrytan/gstack)                           | Role-based skill pack that turns Claude Code into a virtual engineering team    | Claude Code                                     |
| [mattpocock/skills](https://github.com/mattpocock/skills)              | Engineering and productivity skills from Matt Pocock's own agents directory     | Claude Code, Codex, Cursor, Gemini CLI, Copilot |
| [Superpowers](https://github.com/obra/superpowers)                     | Software development methodology delivered as composable skills                 | Claude Code, Codex, Cursor, Gemini CLI, Copilot |

### Testing & QA

| Skill                                                                          | Description                                                                      | Works with           |
| ------------------------------------------------------------------------------ | -------------------------------------------------------------------------------- | -------------------- |
| [Playwright CLI](https://github.com/microsoft/playwright-cli)                  | Playwright command line tool with a skill for browser automation and web testing | Claude Code, Copilot |
| [Playwright Skill (lackeyjb)](https://github.com/lackeyjb/playwright-skill)    | Skill that has agents write and run Playwright scripts on the fly                | Any                  |
| [Playwright Skill (TestDino)](https://github.com/testdino-hq/playwright-skill) | Playwright skill packs split into core, frontend, QA and CI topics               | Any                  |

### DevOps & Cloud

| Skill                                                               | Description                                                              | Works with                   |
| ------------------------------------------------------------------- | ------------------------------------------------------------------------ | ---------------------------- |
| [AWS Agent Plugins](https://github.com/awslabs/agent-plugins)       | AWS Labs plugins for designing, deploying and operating workloads on AWS | Claude Code, Codex, Cursor   |
| [AWS Agent Skills](https://github.com/itsmostafa/aws-agent-skills)  | Skills for 18 core AWS services, from infrastructure code to debugging   | Claude Code, Codex           |
| [Grafana skills](https://github.com/grafana/skills)                 | Skills for the Grafana stack, including the Grafana app SDK              | Claude Code, Codex, Cursor   |
| [HashiCorp agent skills](https://github.com/hashicorp/agent-skills) | Skills and plugins for HashiCorp tools such as Terraform and Packer      | Claude Code, Cursor, Copilot |
| [terraform-skill](https://github.com/antonbabenko/terraform-skill)  | Terraform and OpenTofu practices for testing, modules and CI pipelines   | Any                          |

### Data & Databases

| Skill                                                             | Description                                                                     | Works with                          |
| ----------------------------------------------------------------- | ------------------------------------------------------------------------------- | ----------------------------------- |
| [dbt agent skills](https://github.com/dbt-labs/dbt-agent-skills)  | Skills from dbt Labs for working with dbt projects, lineage and migrations      | Claude Code, Cursor, Copilot        |
| [MongoDB agent skills](https://github.com/mongodb/agent-skills)   | MongoDB Atlas plugin with skills for connections, queries and stream processing | Claude Code, Codex, Cursor, Copilot |
| [Neon agent skills](https://github.com/neondatabase/agent-skills) | Skills for Neon serverless PostgreSQL and the services around it                | Claude Code, Cursor                 |
| [Redis agent skills](https://github.com/redis/agent-skills)       | Redis skills with Claude Code and Codex plugin packaging                        | Claude Code, Codex                  |

### Documents & Office

| Skill                                                            | Description                                                               | Works with         |
| ---------------------------------------------------------------- | ------------------------------------------------------------------------- | ------------------ |
| [Google Workspace CLI](https://github.com/googleworkspace/cli)   | One CLI for Drive, Gmail, Calendar and Sheets, with a skill per service   | Gemini CLI         |
| [guizang-ppt-skill](https://github.com/op7418/guizang-ppt-skill) | Skill for single-file HTML slide decks, covers and matching image prompts | Claude Code, Codex |

### Design & Frontend

| Skill                                                             | Description                                                                  | Works with                                      |
| ----------------------------------------------------------------- | ---------------------------------------------------------------------------- | ----------------------------------------------- |
| [Archify](https://github.com/tt-a1i/archify)                      | Turns ideas, plans or codebases into interactive architecture diagrams       | Claude Code, Codex, Cursor                      |
| [diagram-design](https://github.com/cathrynlavery/diagram-design) | Editorial diagram skill with 45 diagram types, output as HTML and SVG        | Claude Code, Codex, Cursor, Copilot             |
| [Impeccable](https://github.com/pbakaus/impeccable)               | Design vocabulary and hooks that stop agents shipping generic AI-looking UI  | Claude Code, Codex, Cursor, Gemini CLI, Copilot |
| [orrery](https://github.com/Sagargupta16/orrery)                  | Animated cloud architecture diagrams from YAML with official vendor icons    | Claude Code, Codex, Cursor, Gemini CLI          |
| [svg-forge](https://github.com/Sagargupta16/svg-forge)            | Skills for designing and auditing animated SVGs for READMEs and React scenes | Claude Code                                     |
| [taste-skill](https://github.com/Leonxlnx/taste-skill)            | Art direction and browser checks so agents stop making generic AI pages      | Claude Code, Codex                              |

### Security

| Skill                                                                                 | Description                                                               | Works with         |
| ------------------------------------------------------------------------------------- | ------------------------------------------------------------------------- | ------------------ |
| [Cloudflare security-audit skill](https://github.com/cloudflare/security-audit-skill) | Multi-phase security audit workflow with independently verified findings  | Any                |
| [Trail of Bits skills](https://github.com/trailofbits/skills)                         | Security research, vulnerability detection and audit workflows as plugins | Claude Code, Codex |

### Writing & Content

| Skill                                                                | Description                                                              | Works with         |
| -------------------------------------------------------------------- | ------------------------------------------------------------------------ | ------------------ |
| [Humanizer](https://github.com/blader/humanizer)                     | Removes telltale signs of AI writing from text while keeping its meaning | Claude Code, Codex |
| [Marketing Skills](https://github.com/coreyhaines31/marketingskills) | Marketing skills for CRO, copywriting, SEO, analytics and growth         | Any                |

### Research & Knowledge

| Skill                                                                                                          | Description                                                                    | Works with                 |
| -------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ | -------------------------- |
| [Agent Skills for Context Engineering](https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering) | Context engineering and multi-agent design skills for production agent systems | Claude Code, Cursor        |
| [last30days-skill](https://github.com/mvanhorn/last30days-skill)                                               | Researches a topic across Reddit, X, YouTube and the web into one summary      | Any                        |
| [Obsidian skills](https://github.com/kepano/obsidian-skills)                                                   | Skills that teach agents the Obsidian CLI, Markdown, Bases and JSON Canvas     | Any                        |
| [Scientific Agent Skills](https://github.com/K-Dense-AI/scientific-agent-skills)                               | Large science skill library for biology, chemistry, medicine and data analysis | Claude Code, Codex, Cursor |

### Productivity

| Skill                                                                   | Description                                                                | Works with         |
| ----------------------------------------------------------------------- | -------------------------------------------------------------------------- | ------------------ |
| [Planning with Files](https://github.com/OthmanAdi/planning-with-files) | Persistent markdown plans that survive context resets in long agent tasks  | Any                |
| [PM Skills](https://github.com/phuryn/pm-skills)                        | Product management skills from discovery and strategy to launch and growth | Claude Code, Codex |

### Skill Authoring

| Skill                                                                                            | Description                                                            | Works with  |
| ------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------- | ----------- |
| [book-to-skill](https://github.com/virgiliojr94/book-to-skill)                                   | Converts a technical book PDF or document folder into a reusable skill | Any         |
| [skill-creator (Anthropic)](https://github.com/anthropics/skills/tree/main/skills/skill-creator) | Anthropic's skill for creating, editing and evaluating other skills    | Claude Code |

## Collections

Multi-skill packs and plugin marketplaces, listed once as a whole.

| Collection                                                                      | Description                                                              | Works with                             |
| ------------------------------------------------------------------------------- | ------------------------------------------------------------------------ | -------------------------------------- |
| [Agentic Awesome Skills](https://github.com/sickn33/agentic-awesome-skills)     | Large installable library of SKILL.md playbooks with a catalog and CLI   | Claude Code, Codex, Cursor, Gemini CLI |
| [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills) | Hundreds of skills and plugins across engineering, marketing and product | Claude Code, Codex, Cursor, Gemini CLI |
| [ECC](https://github.com/affaan-m/ECC)                                          | Agent harness collection of skills, memory and security tooling          | Claude Code, Codex                     |
| [wshobson/agents](https://github.com/wshobson/agents)                           | Plugin marketplace of agents, skills and commands for many coding tools  | Claude Code, Codex, Cursor, Copilot    |

## Tools

Validators, linters, installers and registries for skills.

- [Skill Seekers](https://github.com/yusufkaraaslan/Skill_Seekers) - Converts documentation sites, repositories and PDFs into skills, with conflict detection.
- [skill-validator](https://github.com/agent-ecosystem/skill-validator) - CLI that validates skill packages against the spec and scores content quality, links and token cost.
- [skillcheck](https://github.com/Sagargupta16/skillcheck) - Conformance suite that lints SKILL.md against the spec and tests skills on real agent runtimes.
- [SkillOpt](https://github.com/microsoft/SkillOpt) - Microsoft's optimizer that improves skill text through trajectory-driven edits and validation gates.
- [skills CLI](https://github.com/vercel-labs/skills) - The `npx skills` installer that adds skills from GitHub repositories to dozens of coding agents.
- [skills.sh](https://skills.sh) - A directory for discovering and installing agent skills, tied to the skills CLI.
- [SkillSpector](https://github.com/NVIDIA/SkillSpector) - NVIDIA's scanner that checks skills for prompt injection, exfiltration and risky patterns before install.
- [Snyk Agent Scan](https://github.com/snyk/agent-scan) - Snyk's scanner for agent components, MCP servers and skills, looking for prompt injection and vulnerabilities.

## Tutorials & Articles

- [Best practices for skill creators](https://agentskills.io/skill-creation/best-practices) - How to ground a skill in real expertise and keep it well scoped.
- [Equipping agents with Agent Skills](https://www.anthropic.com/research/equipping-agents-for-the-real-world-with-agent-skills) - Anthropic's October 2025 introduction to skills as folders of instructions, scripts and resources.
- [Evaluating skill output quality](https://agentskills.io/skill-creation/evaluating-skills) - How to test whether a skill works reliably, using eval-driven iteration.
- [Extend Claude with skills](https://code.claude.com/docs/en/skills) - Claude Code's guide: writing a SKILL.md, invoking skills and what Claude Code adds on top of the open standard.
- [Optimizing skill descriptions](https://agentskills.io/skill-creation/optimizing-descriptions) - How to test and tune a description so the skill triggers on the right prompts.

## Community

- [Awesome MCP Servers](https://github.com/Sagargupta16/awesome-mcp-servers) - The sister list: MCP servers, curated and checked by the same CI.

---

## Contributing

**Anyone can contribute, including your own skill.** Your project needs no minimum star count and no minimum age -- if it holds a `SKILL.md`, is licensed and is documented, it qualifies. Read [CONTRIBUTING.md](CONTRIBUTING.md) for the details.

To add a skill:

1. Fork the repo and branch off `main`.
2. Add **one** row to the most appropriate existing category. Alphabetical order is preferred, not required.
3. Follow the format: `| [Name](URL) | Description | Works with |` with the description at 80 characters or fewer and the agents from `Claude Code`, `Codex`, `Cursor`, `Gemini CLI`, `Copilot` or `Any`.
4. Run `python scripts/validate.py` and fix what it reports.
5. Star the repository. A pull request only merges itself once its author has starred.
6. Open a pull request and answer the affiliation question. Submitting your own project is welcome; not disclosing it is not.

Rather not open a pull request? The [skill suggestion form](https://github.com/Sagargupta16/awesome-skills/issues/new?template=add-skill.yml) turns into the same one-row pull request and runs the same checks.

Once it merges, a bot thanks you on the pull request with a badge for your project's README. It links back here, so people who find your skill can find the rest of the list:

```markdown
[![Listed in Awesome Agent Skills](https://sagargupta.online/awesome-skills/badge.svg)](https://github.com/Sagargupta16/awesome-skills)
```

A star is what lets your pull request merge itself. Without one it waits, labelled `missing-star`, until you star or a maintainer merges it by hand.

Other ways to help, no pull request needed: report rot (a dead link, an archived upstream, a repository that no longer holds a skill) by [opening an issue](https://github.com/Sagargupta16/awesome-skills/issues/new/choose), since pruning is as useful as adding; fix a description that is too terse or reads like marketing; or triage the monthly [health report](https://github.com/Sagargupta16/awesome-skills/issues?q=is%3Aissue+label%3Amaintenance), where confirming or dismissing an item is a real contribution.

Looking for MCP servers instead? The sister list, listed under Community, holds them to the same kind of checks.

## Footnotes

### Using a skill safely

An agent reads a skill's `name` and `description` up front and loads the rest of `SKILL.md`, and any scripts or reference files it points to, when a task calls for it. That makes a skill closer to a plugin than to a document.

**Read it first.** Open `SKILL.md` and every script in the folder before you install it. Instructions can tell the agent to read, change or send your files, and scripts run with your permissions.

**Check what it pre-approves.** The specification's experimental `allowed-tools` field lists tools the skill may use without asking you each time, where the agent supports it.

**Install from the source.** Copy the folder from the repository listed here, at a commit you have read, rather than from a mirror or a re-upload.

**Start narrow.** Try a new skill in one project before installing it for every project. Claude Code, for example, reads personal skills from `~/.claude/skills/` and a project's own from `.claude/skills/`; other agents use their own folders, so check your agent's docs.

Something on the list behaves maliciously? [Report it privately](https://github.com/Sagargupta16/awesome-skills/security/advisories/new), not in a public issue.
