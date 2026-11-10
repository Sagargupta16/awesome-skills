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
- [Anthropic plugin directory](https://github.com/anthropics/claude-plugins-official) - Anthropic's curated Claude Code plugin marketplace, with first-party plugins and vetted partner plugins that can bundle skills.
- [Anthropic skills](https://github.com/anthropics/skills) - Anthropic's public skills for documents, design, MCP and skill creation. Most are Apache-2.0; the four document skills are source-available.
- [Cloudflare skills](https://github.com/cloudflare/skills) - Skills that teach agents to build on Cloudflare, with plugin installs for Claude Code, Codex and Cursor.
- [GitHub awesome-copilot](https://github.com/github/awesome-copilot) - GitHub's community collection of skills, agents and instructions for Copilot.
- [Google skills](https://github.com/google/skills) - Skills for Google products, including Google Cloud and the Gemini API.
- [Google Stitch skills](https://github.com/google-labs-code/stitch-skills) - Skills that pair with the Stitch MCP server for design-to-code work.
- [Hugging Face skills](https://github.com/huggingface/skills) - Skills for working with the Hugging Face ecosystem and its CLI.
- [Microsoft skills](https://github.com/microsoft/skills) - Skills and agent guidance for Azure and Microsoft Foundry SDKs.
- [NVIDIA skills](https://github.com/NVIDIA/skills) - NVIDIA-verified skills for CUDA-X, robotics, simulation and RAG, mirrored daily from NVIDIA's product repositories.
- [OpenAI skills](https://github.com/openai/skills) - The Codex skills catalog, split into curated and system skills and licensed per skill.
- [Sentry skills](https://github.com/getsentry/skills) - Skills the Sentry team uses for its own development, such as commits and settings audits.
- [Stripe AI](https://github.com/stripe/ai) - Stripe's agent toolkit, which includes skills for building with Stripe.
- [Supabase agent skills](https://github.com/supabase/agent-skills) - Skills that help agents build on Supabase.
- [Vercel agent skills](https://github.com/vercel-labs/agent-skills) - Vercel's skills for React and Next.js performance, web design review, React Native, view transitions and Vercel deploys.

## Skills

One skill per row. **Works with** names the agents a skill supports; `Any` means it sticks to the open standard and has no agent-specific parts.

### Development

| Skill                                                                                                  | Description                                                                      | Works with                                      |
| ------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------- | ----------------------------------------------- |
| [Addy Osmani agent skills](https://github.com/addyosmani/agent-skills)                                 | Production-minded engineering skills covering requirements, review and delivery  | Any                                             |
| [Aegis](https://github.com/GanyuanRan/Aegis)                                                           | Baseline-first change planning and evidence-checked completion for coding agents | Claude Code, Codex                              |
| [Agent Rules Books](https://github.com/ciembor/agent-rules-books)                                      | Refactoring, architecture and DDD skills distilled from engineering books        | Claude Code, Codex, Cursor                      |
| [Agent Vision Toolkit](https://github.com/Anionex/agent-vision-toolkit)                                | Image Q and A, screenshot OCR and UI restoration for text-only agents            | Claude Code, Codex                              |
| [AgentOps](https://github.com/boshu2/agentops)                                                         | Plan, implement and validate skills that apply engineering practice to agents    | Claude Code, Codex, Cursor, Gemini CLI          |
| [agents-best-practices](https://github.com/DenisSergeevitch/agents-best-practices)                     | Design, audit and refactor agentic harnesses with provider-neutral guidance      | Claude Code, Codex                              |
| [Android skills](https://github.com/android/skills)                                                    | Android development skills from Google, installed with the Android CLI           | Claude Code, Codex                              |
| [Anthony Fu skills](https://github.com/antfu/skills)                                                   | Anthony Fu's skills for Vue, Nuxt, Vite, Vitest, Pinia, UnoCSS and pnpm          | Any                                             |
| [Anti Slop](https://github.com/miqdadbadjuber/anti-slop)                                               | Rules that stop coding agents writing generic AI comments, code and UI           | Claude Code, Codex                              |
| [BAMA](https://github.com/daveebbelaar/bama)                                                           | Skills to research, design and build native macOS apps in SwiftUI                | Claude Code, Codex                              |
| [Beautiful Rust](https://github.com/morganlinton/BeautifulRust)                                        | Skills to write, review and port idiomatic Rust, plus a clippy lints config      | Claude Code, Codex, Cursor, Gemini CLI, Copilot |
| [Birdview](https://github.com/Qiuner/birdview)                                                         | Map architecture and change scope on one HTML page before coding                 | Claude Code, Codex                              |
| [brooks-lint](https://github.com/hyhmrright/brooks-lint)                                               | Code quality reviews that cite classic software engineering books                | Claude Code, Codex, Cursor, Gemini CLI, Copilot |
| [builder-skills](https://github.com/waynesutton/builder-skills)                                        | Ten workflow, security and writing skills for builders shipping apps             | Claude Code, Codex, Cursor                      |
| [Callstack Agent Skills](https://github.com/callstackincubator/agent-skills)                           | React Native skills for performance, navigation, upgrades, testing and migration | Claude Code, Codex, Cursor, Gemini CLI, Copilot |
| [cc-sdd](https://github.com/gotalab/cc-sdd)                                                            | Spec-driven workflow from requirements to design, tasks and implementation       | Claude Code, Codex, Cursor, Gemini CLI, Copilot |
| [Claude Code Harness](https://github.com/Chachamaru127/claude-code-harness)                            | Plan, work, review and ship workflow with quality checks for coding agents       | Claude Code, Codex, Cursor                      |
| [Claude Code Java](https://github.com/decebals/claude-code-java)                                       | Java skills for code review, testing, commits and architecture decisions         | Claude Code                                     |
| [Claude Skills Marketplace (mhattingpete)](https://github.com/mhattingpete/claude-skills-marketplace)  | Claude Code plugins for Git automation, testing, review and code execution       | Claude Code                                     |
| [Claude Workflow v2](https://github.com/CloudAI-X/claude-workflow-v2)                                  | Workflow plugin with agents, skills, hooks and mode commands for any project     | Claude Code, Codex, Cursor                      |
| [Codex on Crack](https://github.com/ethanplusai/codex-on-crack)                                        | Plan, delegate and review work across several models from Codex                  | Codex                                           |
| [Compound Engineering](https://github.com/EveryInc/compound-engineering-plugin)                        | Plan, build, review and capture lessons in a repeatable engineering loop         | Claude Code, Codex, Cursor                      |
| [Delegate Skills](https://github.com/amElnagdy/delegate-skills)                                        | Delegate coding tasks to other agent CLIs in named lanes, then review            | Any                                             |
| [dryforge](https://github.com/prekuter/dryforge)                                                       | Bounded-autonomy plugin harness from intent to reviewed implementation           | Claude Code, Codex, Copilot                     |
| [dzhng Skills](https://github.com/dzhng/skills)                                                        | Composable skills to explore ideas, write specs and implement autonomously       | Claude Code, Codex, Cursor                      |
| [Elephant-Goldfish Model](https://github.com/google/elephant-goldfish-model)                           | Draft design specs with one agent, then stress-test them with fresh reviewers    | Claude Code, Codex                              |
| [evo](https://github.com/evo-hq/evo)                                                                   | Optimize a codebase through measured experiments in an autoresearch loop         | Claude Code, Codex, Cursor                      |
| [Expo skills](https://github.com/expo/skills)                                                          | Skills for building and shipping Expo apps and using Expo Application Services   | Claude Code, Codex, Cursor                      |
| [Fable Method](https://github.com/Sahir619/fable-method)                                               | Four-skill method: classify the ask, define done, verify before finishing        | Claude Code, Codex                              |
| [FableCodex](https://github.com/baskduf/FableCodex/tree/main/plugins/codex-fable5/skills/codex-fable5) | Codex workflow skill: inspect first, record evidence and verify before done      | Codex                                           |
| [FDEOps](https://github.com/suboss87/FDEOps)                                                           | Forward deployed engineering skills from customer discovery to verified rollout  | Any                                             |
| [Finding Unknowns](https://github.com/Neeeophytee/finding-unknowns-skills)                             | Fourteen skills that surface unknowns before an agent starts building            | Claude Code, Codex, Cursor, Copilot             |
| [Firebase agent skills](https://github.com/firebase/agent-skills)                                      | Firebase skills, shipped as a Gemini CLI extension and as plugins                | Claude Code, Codex, Gemini CLI                  |
| [Flutter AI Skills](https://github.com/evanca/flutter-ai-rules)                                        | Flutter and Dart skills from official docs, covering Firebase and Riverpod       | Claude Code, Codex, Cursor                      |
| [Fullstack Dev Skills](https://github.com/Jeffallan/claude-skills)                                     | Full-stack developer skills covering languages, frameworks, testing and DevOps   | Claude Code                                     |
| [Gemini API skills](https://github.com/google-gemini/gemini-skills)                                    | Skills for building apps with the Gemini API, Live API and Omni video models     | Claude Code, Codex, Cursor                      |
| [Golang Skills (samber)](https://github.com/samber/cc-skills-golang)                                   | Go skills for performance, testing, design and review                            | Claude Code, Codex, Cursor, Copilot             |
| [gstack](https://github.com/garrytan/gstack)                                                           | Role-based skill pack that turns Claude Code into a virtual engineering team     | Claude Code                                     |
| [guard-skills](https://github.com/amElnagdy/guard-skills)                                              | Second-pass quality gates for AI-generated code, tests and docs                  | Claude Code, Codex, Cursor                      |
| [Han](https://github.com/testdouble/han)                                                               | Planning, TDD implementation, review and docs skills with specialist agents      | Claude Code, Codex                              |
| [iOS Simulator Skill](https://github.com/conorluddy/ios-simulator-skill)                               | Build, test and drive iOS apps with xcodebuild and simulator scripts             | Claude Code, Codex                              |
| [KiCad Happy](https://github.com/aklofas/kicad-happy)                                                  | Review KiCad schematics, PCB layouts and Gerbers for design bugs                 | Claude Code, Codex, Copilot                     |
| [Kotlin Footguns](https://github.com/maxrave-dev/kotlin-footguns)                                      | Kotlin and Compose Multiplatform traps as skills plus a change scanner           | Claude Code, Codex, Cursor, Copilot             |
| [mattpocock/skills](https://github.com/mattpocock/skills)                                              | Engineering and productivity skills from Matt Pocock's own agents directory      | Claude Code, Codex, Cursor, Gemini CLI, Copilot |
| [mcode-stack](https://github.com/MiniMax-AI/mcode-stack)                                               | Coding workflows and skills for subagent use, long sessions and code quality     | Claude Code, Codex                              |
| [.NET Skills](https://github.com/dotnet/skills)                                                        | Skills from the .NET team for C# and .NET coding work                            | Claude Code, Codex, Cursor, Copilot             |
| [NovelToGame](https://github.com/zenstory-ai/novel-to-game)                                            | Adapt a novel into a playable game with design, build and QA skills              | Claude Code, Codex                              |
| [Open Code Review](https://github.com/alibaba/open-code-review)                                        | Line-level AI code review of Git diffs with a multi-language ruleset             | Claude Code, Codex, Cursor                      |
| [OpenQodex](https://github.com/openqodex/openqodex)                                                    | Independent code review of each agent change before you push                     | Claude Code, Codex, Cursor                      |
| [Paperthin](https://github.com/LilMGenius/paperthin)                                                   | Skillbook of low-level agentic design patterns for coding agents                 | Claude Code, Codex, Cursor                      |
| [PavedPath Code](https://github.com/Jia-Ethan/pavedpath-code)                                          | Find proven implementation paths in GitHub evidence for code problems            | Claude Code, Codex, Cursor                      |
| [Plinth](https://github.com/jabrena/plinth)                                                            | Skills, agents and commands for Java enterprise development                      | Claude Code, Codex, Cursor, Copilot             |
| [Ponytail](https://github.com/DietrichGebert/ponytail)                                                 | Makes agents write the least code that works, reusing what the repo already has  | Claude Code, Codex, Cursor, Gemini CLI, Copilot |
| [Power Platform Skills](https://github.com/microsoft/power-platform-skills)                            | Microsoft skills for building on Power Pages, Power Apps and Power Platform      | Claude Code, Copilot                            |
| [pstack](https://github.com/backnotprop/pstack)                                                        | Engineering skills for design, TDD, review and cleanup of agent code             | Claude Code, Codex, Cursor                      |
| [Rails Upgrade Assistant](https://github.com/ombulabs/claude-code_rails-upgrade-skill)                 | Plan Ruby on Rails upgrades from 2.3 to 8.1 with reports and previews            | Claude Code                                     |
| [Robotics Agent Skills](https://github.com/arpitg1304/robotics-agent-skills)                           | ROS1 and ROS2 skills for nodes, QoS, launch files, Docker and tests              | Claude Code, Cursor                             |
| [skill-codex](https://github.com/skills-directory/skill-codex)                                         | Let Claude Code delegate analysis and edit tasks to the Codex CLI                | Claude Code                                     |
| [Spring Boot Skills](https://github.com/rrezartprebreza/spring-boot-skills)                            | Spring Boot skills for architecture, patterns and project conventions            | Claude Code, Codex                              |
| [Stop That Shit](https://github.com/lennney/stop-that-shit)                                            | Skills and guard hooks that stop scope creep and needless extra work by agents   | Claude Code, Codex                              |
| [Super Board](https://github.com/EricTechPro/super-board)                                              | GitHub Project build, QA and review loop with merge gates                        | Claude Code                                     |
| [Superpowers](https://github.com/obra/superpowers)                                                     | Software development methodology delivered as composable skills                  | Claude Code, Codex, Cursor, Gemini CLI, Copilot |
| [Superpowers Lab](https://github.com/obra/superpowers-lab)                                             | Experimental skills for Superpowers such as duplicate function detection         | Claude Code                                     |
| [Swift Concurrency Skill](https://github.com/AvdLee/Swift-Concurrency-Agent-Skill)                     | Swift 6 concurrency guidance for data races, isolation errors and migration      | Claude Code, Codex, Cursor, Gemini CLI          |
| [SwiftUI Expert Skill](https://github.com/AvdLee/SwiftUI-Agent-Skill)                                  | SwiftUI guidance on state, view composition, performance and Liquid Glass        | Any                                             |
| [Turbo](https://github.com/tobihagemann/turbo)                                                         | Human-gated software factory skills from plan through build and review           | Claude Code, Codex                              |
| [Understand Anything](https://github.com/Egonex-AI/Understand-Anything)                                | Builds an explorable knowledge graph of a codebase or docs, with a dashboard     | Claude Code, Codex, Cursor, Gemini CLI, Copilot |
| [Waza](https://github.com/tw93/Waza)                                                                   | Eight engineering-habit skills for planning, review, debugging, UI and writing   | Claude Code, Codex, Cursor, Gemini CLI, Copilot |
| [WebPerf Snippets](https://github.com/nucliweb/webperf-snippets)                                       | Web performance measurement snippets and workflows packaged as agent skills      | Claude Code, Cursor, Gemini CLI                 |
| [WordPress agent skills](https://github.com/WordPress/agent-skills)                                    | WordPress skills for blocks, themes, plugins, REST API, WP-CLI and performance   | Claude Code, Codex, Cursor, Copilot             |
| [Xcode Build Optimization](https://github.com/AvdLee/Xcode-Build-Optimization-Agent-Skill)             | Benchmark and speed up Xcode clean and incremental builds and SwiftPM overhead   | Claude Code                                     |

### Testing & QA

| Skill                                                                          | Description                                                                      | Works with                               |
| ------------------------------------------------------------------------------ | -------------------------------------------------------------------------------- | ---------------------------------------- |
| [Dev Browser](https://github.com/SawyerHood/dev-browser)                       | Browser automation CLI that lets agents drive Chrome with short scripts          | Claude Code, Codex                       |
| [Playwright CLI](https://github.com/microsoft/playwright-cli)                  | Playwright command line tool with a skill for browser automation and web testing | Claude Code, Copilot                     |
| [Playwright Skill (lackeyjb)](https://github.com/lackeyjb/playwright-skill)    | Skill that has agents write and run Playwright scripts on the fly                | Any                                      |
| [Playwright Skill (TestDino)](https://github.com/testdino-hq/playwright-skill) | Playwright skill packs split into core, frontend, QA and CI topics               | Any                                      |
| [TestMu AI Skills](https://github.com/LambdaTest/agent-skills)                 | Vendor skills for test automation frameworks across 15 plus languages            | Claude Code, Cursor, Gemini CLI, Copilot |
| [Web Quality Skills](https://github.com/addyosmani/web-quality-skills)         | Lighthouse, Core Web Vitals, accessibility and SEO audit and fix skills          | Claude Code, Codex, Cursor               |

### DevOps & Cloud

| Skill                                                                                  | Description                                                                      | Works with                                      |
| -------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- | ----------------------------------------------- |
| [App Store Connect CLI Skills](https://github.com/rorkai/app-store-connect-cli-skills) | Builds, TestFlight, metadata, signing and submission with the asc CLI            | Claude Code, Codex                              |
| [AWS Agent Plugins](https://github.com/awslabs/agent-plugins)                          | AWS Labs plugins for designing, deploying and operating workloads on AWS         | Claude Code, Codex, Cursor                      |
| [AWS Agent Skills](https://github.com/itsmostafa/aws-agent-skills)                     | Skills for 18 core AWS services, from infrastructure code to debugging           | Claude Code, Codex                              |
| [AWS Skills (zxkane)](https://github.com/zxkane/aws-skills)                            | AWS plugins for CDK, serverless, cost operations and Bedrock AgentCore           | Claude Code                                     |
| [Azure Skills](https://github.com/microsoft/azure-skills)                              | Azure workflows for preparing, validating, deploying and diagnosing apps         | Claude Code, Codex, Cursor, Gemini CLI, Copilot |
| [cc-devops-skills](https://github.com/akin-ozer/cc-devops-skills)                      | Generators and validators for Ansible, Kubernetes and CI configs, plus debugging | Claude Code, Codex                              |
| [CloudBase AI Toolkit](https://github.com/TencentCloudBase/CloudBase-AI-Toolkit)       | Skills and plugin for building backends on Tencent CloudBase                     | Claude Code, Codex, Cursor, Copilot             |
| [GoLive](https://github.com/mikehasa/golive-skill)                                     | Take an agent-built app live: hosting, database, domain, email, payments         | Claude Code, Codex                              |
| [Grafana skills](https://github.com/grafana/skills)                                    | Skills for the Grafana stack, including the Grafana app SDK                      | Claude Code, Codex, Cursor                      |
| [HashiCorp agent skills](https://github.com/hashicorp/agent-skills)                    | Skills and plugins for HashiCorp tools such as Terraform and Packer              | Claude Code, Cursor, Copilot                    |
| [Home Assistant Manager](https://github.com/komal-SkyNET/claude-skill-homeassistant)   | Manage Home Assistant config, deployments, automations and Lovelace dashboards   | Claude Code                                     |
| [KubeShark Kubernetes Skill](https://github.com/LukasNiessen/kubernetes-skill)         | Kubernetes manifest skill that reduces hallucinated APIs                         | Claude Code, Codex                              |
| [modulestf](https://github.com/modulestf/modulestf)                                    | Review reusable Terraform modules against a profile of the family rules          | Claude Code, Codex                              |
| [terraform-skill](https://github.com/antonbabenko/terraform-skill)                     | Terraform and OpenTofu practices for testing, modules and CI pipelines           | Any                                             |
| [TerraShark](https://github.com/LukasNiessen/terrashark)                               | Terraform and OpenTofu skill that reduces hallucinated configuration             | Claude Code, Codex, Gemini CLI                  |

### Data & Databases

| Skill                                                                                                              | Description                                                                     | Works with                             |
| ------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------- | -------------------------------------- |
| [ClickHouse Best Practices](https://github.com/ClickHouse/agent-skills/tree/main/skills/clickhouse-best-practices) | Official ClickHouse rules for schema design, query tuning and data ingestion    | Any                                    |
| [Datacircle](https://github.com/waynehamadi/datacircle-plugin/tree/main/skills/datacircle)                         | Compare and price GTM APIs from one file of every plan                          | Any                                    |
| [dbt agent skills](https://github.com/dbt-labs/dbt-agent-skills)                                                   | Skills from dbt Labs for working with dbt projects, lineage and migrations      | Claude Code, Cursor, Copilot           |
| [Finance Skills](https://github.com/himself65/finance-skills)                                                      | Skills for financial analysis, market data and trading research                 | Claude Code, Codex, Cursor             |
| [MongoDB agent skills](https://github.com/mongodb/agent-skills)                                                    | MongoDB Atlas plugin with skills for connections, queries and stream processing | Claude Code, Codex, Cursor, Copilot    |
| [Neon agent skills](https://github.com/neondatabase/agent-skills)                                                  | Skills for Neon serverless PostgreSQL and the services around it                | Claude Code, Cursor                    |
| [pg-aiguide](https://github.com/timescale/pg-aiguide)                                                              | PostgreSQL table design and query skills with version-aware manual search       | Claude Code, Codex, Cursor, Gemini CLI |
| [Redis agent skills](https://github.com/redis/agent-skills)                                                        | Redis skills with Claude Code and Codex plugin packaging                        | Claude Code, Codex                     |
| [Trading Skills](https://github.com/staskh/trading_skills)                                                         | Options and equity analysis skills with technicals, Greeks and risk metrics     | Claude Code, Cursor                    |

### Documents & Office

| Skill                                                              | Description                                                                   | Works with                          |
| ------------------------------------------------------------------ | ----------------------------------------------------------------------------- | ----------------------------------- |
| [Codex PPT](https://github.com/ningzimu/codex-ppt-skill)           | Generate image-based PPT decks from articles with GPT-Image-2                 | Claude Code, Codex                  |
| [Frontend Slides](https://github.com/zarazhangrui/frontend-slides) | Build HTML slide decks from scratch or by converting PowerPoint files         | Claude Code, Codex, Gemini CLI      |
| [Google Workspace CLI](https://github.com/googleworkspace/cli)     | One CLI for Drive, Gmail, Calendar and Sheets, with a skill per service       | Gemini CLI                          |
| [guizang-ppt-skill](https://github.com/op7418/guizang-ppt-skill)   | Skill for single-file HTML slide decks, covers and matching image prompts     | Claude Code, Codex                  |
| [huashu-md-html](https://github.com/alchaincyf/huashu-md-html)     | Convert files to markdown, then to styled HTML or publisher-ready docx        | Claude Code, Codex, Cursor          |
| [Kami](https://github.com/tw93/Kami)                               | Layout rules and templates for agent-made PDF, PNG and PowerPoint documents   | Claude Code, Codex, Cursor          |
| [Mck PPT Design](https://github.com/likaku/Mck-ppt-design-skill)   | Consulting-style editable PowerPoint decks with native shapes and charts      | Claude Code, Cursor                 |
| [OfficeCLI](https://github.com/iOfficeAI/OfficeCLI)                | Single-binary CLI that lets agents create and edit Word, Excel and PowerPoint | Claude Code, Codex, Cursor, Copilot |
| [translate-book](https://github.com/deusyu/translate-book)         | Translate whole PDF, DOCX or EPUB books in parallel with subagents            | Claude Code, Codex                  |

### Design & Frontend

| Skill                                                                                      | Description                                                                      | Works with                                      |
| ------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------- | ----------------------------------------------- |
| [3dviz Pro Max](https://github.com/viettranx/3dviz-pro-max)                                | Design and build interactive Three.js and Blender 3D scenes                      | Claude Code, Codex                              |
| [Agent Sprite Forge](https://github.com/0x0funky/agent-sprite-forge)                       | Generate game-ready 2D sprite sheets, maps and animated GIFs from prompts        | Claude Code, Codex                              |
| [AI Promo Video Maker](https://github.com/liyupi/ai-promo-video-maker)                     | Produce a 4K product promo video from a product name or URL                      | Claude Code, Codex, Cursor                      |
| [AI Shortfilm Prompts](https://github.com/jnMetaCode/ai-shortfilm-prompts)                 | Turn an idea into multi-shot cinematic prompts for AI video models               | Claude Code                                     |
| [Anatomy](https://github.com/wheresryan22/anatomy)                                         | Build interactive isometric SVG figures that explain technical ideas             | Claude Code, Codex                              |
| [Anidoodle](https://github.com/alexgreensh/anidoodle)                                      | Illustrations, loops, films and interactive web art written as code in 32 styles | Claude Code, Codex                              |
| [App Store Screenshots](https://github.com/ParthJadhav/app-store-screenshots)              | Scaffold a Next.js editor that exports App Store and Google Play screenshots     | Claude Code, Codex, Cursor                      |
| [Appllama Skills](https://github.com/Appllama/appllama-skills)                             | Mobile app design research and native-feeling Expo screen building skills        | Claude Code, Codex, Cursor                      |
| [Archify](https://github.com/tt-a1i/archify)                                               | Turns ideas, plans or codebases into interactive architecture diagrams           | Claude Code, Codex, Cursor                      |
| [Auteur](https://github.com/agiwhitelist/auteur)                                           | Direct a website like a film with locked art direction and anti-slop gates       | Claude Code, Codex, Cursor, Gemini CLI, Copilot |
| [Awwwards Skill](https://github.com/juliobsz/skills)                                       | Build and score award-style websites from a one-line prompt                      | Claude Code, Codex, Cursor                      |
| [Bitwize Music](https://github.com/bitwize-music-studio/claude-ai-music-skills)            | Album production workflow for Suno from lyrics to release                        | Claude Code                                     |
| [Blender Agent Skills](https://github.com/EL4CTEO/blender-skills)                          | Blender skills covering the 3D pipeline from modeling to rendering               | Claude Code, Codex, Cursor, Gemini CLI, Copilot |
| [Blender Skills](https://github.com/arjun988/blender-skills)                               | Blender modeling, lighting and animation skills driven through Blender MCP       | Claude Code, Codex, Cursor                      |
| [Brag](https://github.com/latent-spaces/brag)                                              | Turn a finished project into a short launch video with music and share copy      | Claude Code, Codex                              |
| [Brand Identity](https://github.com/fatihaydost/brand-identity-skill)                      | Design a logo, typography and palette together with a brand guidelines kit       | Claude Code                                     |
| [CapCut CLI](https://github.com/renezander030/capcut-cli)                                  | Edit CapCut and JianYing projects from the terminal with a bundled edit skill    | Claude Code, Codex, Cursor                      |
| [Cinematic Director](https://github.com/wuwangzhang1216/DirectorSKILL)                     | Turn a script into beats, a shot list and keyframe prompts for AI film           | Claude Code                                     |
| [Cinetic](https://github.com/Leonxlnx/cinetic)                                             | Direct and render launch films and motion design from code                       | Claude Code, Codex, Cursor                      |
| [Classical Poem Silk Video](https://github.com/Mr-funny/hbg-classical-poem-silk-video)     | Turn Chinese classical poems into vertical ink-painting motion videos            | Claude Code, Codex                              |
| [Claude Remotion Skill](https://github.com/haidrrrry/claude-remotion-skill)                | Motion graphics videos with Remotion, with motion design craft rules             | Claude Code                                     |
| [ComfyUI Skills](https://github.com/HuangYuChuh/ComfyUI_Skills_OpenClaw)                   | Turn ComfyUI workflows into callable agent skills through a CLI                  | Claude Code, Codex                              |
| [Dashboard Design](https://github.com/abdiraimov-otabek/dashboard-design-skill)            | Design and critique dashboards with KPI tiles, charts and filters                | Claude Code                                     |
| [Design DNA](https://github.com/zanwei/design-dna)                                         | Extract design tokens, style and effects from reference UIs as JSON              | Claude Code, Cursor                             |
| [designlang](https://github.com/Manavarya09/design-extract)                                | Extract a site's design system into tokens, Tailwind and shadcn themes           | Claude Code, Codex, Cursor                      |
| [diagram-design](https://github.com/cathrynlavery/diagram-design)                          | Editorial diagram skill with 45 diagram types, output as HTML and SVG            | Claude Code, Codex, Cursor, Copilot             |
| [Diorama](https://github.com/sloemo01/diorama)                                             | Playbook and code kit for detailed Three.js dioramas                             | Any                                             |
| [draw-your-font](https://github.com/danilo-znamerovszkij/draw-your-font)                   | Turn a photo of handwriting into an installable TTF or WOFF2 font                | Claude Code                                     |
| [drawio-skill](https://github.com/Agents365-ai/drawio-skill)                               | Editable draw.io diagrams from prompts, code, Terraform, SQL and OpenAPI         | Claude Code, Codex, Cursor, Copilot             |
| [Effective HTML](https://github.com/plannotator/effective-html)                            | Skills for HTML wireframes, prototypes, one-pagers and design artifacts          | Claude Code, Codex                              |
| [ffmpeg-skill](https://github.com/kajisho5/ffmpeg-skill)                                   | Local video editing for agents with 42 FFmpeg tools and output checks            | Claude Code, Codex, Cursor                      |
| [ghost-editor](https://github.com/kurbaitaev/ghost-editor)                                 | Edit raw talking-head recordings into finished reels with preset styles          | Claude Code                                     |
| [GPT Image Skill](https://github.com/wuyoscar/GPT-Image2-Skill)                            | GPT Image prompt gallery and CLI for generating and editing images               | Claude Code, Codex                              |
| [GSAP Skills](https://github.com/greensock/gsap-skills)                                    | Official GSAP skills for the core API, timelines, ScrollTrigger and plugins      | Claude Code, Codex, Cursor, Copilot             |
| [gtrk](https://github.com/Gitruck/cli)                                                     | Video editing CLI skills that turn spoken footage into editable projects         | Claude Code, Codex, Cursor                      |
| [Guizang Social Card](https://github.com/op7418/guizang-social-card-skill)                 | Social carousel and cover card sets in editorial and Swiss visual styles         | Claude Code, Codex, Cursor                      |
| [Higgsfield Prompt Skill](https://github.com/OSideMedia/higgsfield-ai-prompt-skill)        | Cinematic video and image prompts for Higgsfield with camera and model guidance  | Claude Code                                     |
| [Huashu Art Motion](https://github.com/alchaincyf/huashu-art-motion)                       | Animate 36 art styles as code-drawn video clips and explainers                   | Claude Code, Codex                              |
| [Huashu Design](https://github.com/alchaincyf/huashu-design)                               | HTML prototypes, slide decks, animation and infographics with a style library    | Any                                             |
| [Huashu Motion](https://github.com/alchaincyf/huashu-motion)                               | Produce editable launch films and explainers as code with music                  | Claude Code, Codex                              |
| [hue](https://github.com/dominikmartn/hue)                                                 | Learn a brand from a URL or screenshot and generate a full design system skill   | Claude Code, Codex                              |
| [HyperFrames](https://github.com/heygen-com/hyperframes)                                   | Write HTML, CSS and seekable animations, then render deterministic MP4 video     | Claude Code, Codex, Cursor, Gemini CLI, Copilot |
| [HyperFrames Motion Director](https://github.com/geekjourneyx/hyperframes-motion-director) | Plan, produce and review Chinese-first HyperFrames motion videos                 | Any                                             |
| [Image Prompt Reverse](https://github.com/LunarXuan/image-prompt-reverse)                  | Turn a reference image into a detailed AI image generation prompt                | Codex                                           |
| [Imagera](https://github.com/alexadams6ix/imagera-skills/tree/main/skills/imagera-media)   | Generate and edit images, video, voice and music through Imagera's remote MCP    | Claude Code, Codex, Cursor, Gemini CLI          |
| [Impeccable](https://github.com/pbakaus/impeccable)                                        | Design vocabulary and hooks that stop agents shipping generic AI-looking UI      | Claude Code, Codex, Cursor, Gemini CLI, Copilot |
| [Logo Design Skill](https://github.com/kaankiziltug/logo-design-skill)                     | Logo design from brief to SVG, with a reference library of 1,400+ logos          | Claude Code, Codex, Cursor, Gemini CLI, Copilot |
| [Machine Skill](https://github.com/AirsupHQ/machine-skill)                                 | Build an interactive physics-based 3D model of any machine as an HTML file       | Claude Code                                     |
| [Motion Design Skill](https://github.com/LottieFiles/motion-design-skill)                  | Motion design principles for timing, easing and choreography in UI animation     | Claude Code, Codex, Cursor, Copilot             |
| [Motion Graphics Skills](https://github.com/charlie947/motion-graphics-skills)             | Skills for launch videos and animated charts rendered from code                  | Claude Code, Codex                              |
| [motionmaxxing](https://github.com/Tejashmakwana/motionmaxxing)                            | Turn flat AI-generated videos into designed motion graphics                      | Claude Code                                     |
| [Narrator AI CLI Skill](https://github.com/NarratorAI-Studio/narrator-ai-cli-skill)        | Create movie narration videos by driving the narrator-ai-cli tool                | Claude Code, Cursor                             |
| [Native Subtitle Quote Image](https://github.com/chengyi-ai/native-subtitle-quote-image)   | Turn video frames and subtitles into 3:4 quote images for social posts           | Claude Code, Codex                              |
| [Oil Motion](https://github.com/oil-oil/oil-motion)                                        | Turn video or frames into scroll and pointer driven web animations               | Claude Code, Codex                              |
| [Oil UI](https://github.com/oil-oil/oil-ui)                                                | Pick, compare and refine UI design directions against real screenshots           | Claude Code, Codex                              |
| [OnlyShot](https://github.com/A-cat-with-carrots/OnlyShot)                                 | AI short drama pipeline from idea to script, storyboard, video and rough cut     | Claude Code                                     |
| [Open Design Agent Kit](https://github.com/feimacode/open-design-agent-kit)                | Design skills, brand systems and remixable examples inside your coding agent     | Claude Code, Codex, Cursor, Copilot             |
| [Orkas Video Studio](https://github.com/Orkas-AI/Orkas-VideoStudio)                        | Compose, generate and edit video from a coding agent via a plan file             | Claude Code, Codex, Cursor                      |
| [orrery](https://github.com/Sagargupta16/orrery)                                           | Animated cloud architecture diagrams from YAML with official vendor icons        | Claude Code, Codex, Cursor, Gemini CLI          |
| [Papermorph](https://github.com/DozenTwelve/Papermorph)                                    | Turn books and textbook PDFs into animated, narrated, interactive web lessons    | Claude Code                                     |
| [Pixel2Motion](https://github.com/nolangz/pixel2motion)                                    | Turn raster logos into clean SVG and animated logo motion demos                  | Claude Code, Codex                              |
| [Pretty Mermaid](https://github.com/imxv/Pretty-mermaid-skills)                            | Render Mermaid diagrams to themed SVG, PNG or terminal ASCII locally             | Claude Code, Codex, Cursor, Gemini CLI          |
| [Product Launch Motion](https://github.com/AbubakrChan/product-launch-motion)              | Turn a website URL into a product launch video with rendered motion and music    | Claude Code                                     |
| [Qiaomu Design](https://github.com/joeseesun/qiaomu-design)                                | Design advisor that proposes four directions, then builds and verifies the UI    | Claude Code, Codex                              |
| [rea-video](https://github.com/JuneYaooo/rea-video)                                        | Break down a video shot by shot and plan how to remake it                        | Claude Code, Codex                              |
| [Reelbench Skills](https://github.com/eternityspring/reelbench-skills)                     | Video analysis skills: shot detection, scrubbing and audio sync                  | Claude Code, Codex                              |
| [Scenario Skills](https://github.com/scenario-labs/skills)                                 | Generate images, video, audio and 3D through the Scenario MCP server             | Claude Code, Codex, Cursor, Copilot             |
| [scroll-craft](https://github.com/nateherkai/scroll-craft)                                 | Scroll-driven landing pages with a design standard and browser checks            | Claude Code, Codex                              |
| [SeeCode](https://github.com/Aryanutkarsh/SeeCode)                                         | Animated, explorable diagrams in 45 types from a short brief                     | Claude Code, Codex, Cursor                      |
| [Smart Illustrator](https://github.com/axtonliu/smart-illustrator)                         | Article illustrations and cover images via Gemini, Excalidraw or Mermaid         | Claude Code                                     |
| [Stickman Video Director](https://github.com/kaomei/stickman-video-director)               | Turn a script into animated stickman videos with visuals, voice and captions     | Claude Code, Codex, Cursor                      |
| [StyleSeed](https://github.com/bitjaru/styleseed)                                          | Keep a UI design system consistent across screens with checks on rendered output | Claude Code, Codex, Cursor                      |
| [Superdesign](https://github.com/superdesigndev/superdesign-skill)                         | Design judgment for UI, slides and graphics generated by coding agents           | Claude Code, Codex, Cursor                      |
| [svg-diagram](https://github.com/bybit-exchange/svg-diagram)                               | House style and linter for hand-written SVG architecture diagrams                | Claude Code, Codex, Cursor, Gemini CLI, Copilot |
| [svg-forge](https://github.com/Sagargupta16/svg-forge)                                     | Skills for designing and auditing animated SVGs for READMEs and React scenes     | Claude Code                                     |
| [taste-skill](https://github.com/Leonxlnx/taste-skill)                                     | Art direction and browser checks so agents stop making generic AI pages          | Claude Code, Codex                              |
| [Tastemaker](https://github.com/codeswithroh/tastemaker)                                   | Ground generated UI in reference images and a palette for real design taste      | Claude Code, Gemini CLI                         |
| [Three.js Skills](https://github.com/CloudAI-X/threejs-skills)                             | Guidance on three.js, React Three Fiber and WebGPU for 3D web apps               | Claude Code                                     |
| [UI Craft](https://github.com/educlopez/ui-craft)                                          | Design engineering skill with a build bar, theme presets and review agents       | Claude Code, Codex, Cursor, Gemini CLI          |
| [UI UX Pro Max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill)                   | Searchable UI styles, color palettes and font pairings for UI and UX work        | Claude Code, Codex, Cursor, Gemini CLI, Copilot |
| [UX/UI Agent Skills](https://github.com/plugin87/ux-ui-agent-skills)                       | Design-system skills with tokens, WCAG checks and measured quality gates         | Claude Code, Codex, Cursor                      |
| [vibeX](https://github.com/Raja0sama/vibex)                                                | Diagrams and checkable docs generated from schemas, APIs and source code         | Claude Code, Codex                              |
| [Video Podcast Maker](https://github.com/Agents365-ai/video-podcast-maker)                 | Turn a topic into a narrated 4K video with TTS and Remotion                      | Claude Code, Codex                              |
| [Video Recap Skills](https://github.com/zenstory-ai/video-recap-skills)                    | Turn videos into Chinese narrated recaps with JianYing draft export              | Claude Code, Codex                              |
| [Video Shotcraft](https://github.com/Vincentwei1021/video-shotcraft)                       | Cinematic product promo videos from your pages with Remotion shot recipes        | Claude Code, Codex                              |
| [Visual Explainer](https://github.com/nicobailon/visual-explainer)                         | Turn diagrams, diff reviews and plans into styled HTML pages                     | Claude Code, Codex, Cursor                      |
| [Visual Skills](https://github.com/smixs/visual-skills)                                    | Video and image prompt skills written with a film director's craft               | Claude Code, Codex, Cursor                      |
| [Vox Director](https://github.com/Alisa0808/vox-director)                                  | Turn a topic into a paper-collage explainer video with script, voice, captions   | Claude Code, Codex                              |
| [web-design](https://github.com/xiaopu-ai/web-design)                                      | Write a DESIGN.md spec first, then generate consistent web pages                 | Claude Code                                     |

### Security

| Skill                                                                                              | Description                                                                     | Works with                          |
| -------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- | ----------------------------------- |
| [AIG Agent Red Team](https://github.com/Tencent/AI-Infra-Guard/tree/main/skills/aig-agent-redteam) | Authorized red-team assessment of agents, MCP servers and skills                | Claude Code, Cursor                 |
| [Cloudflare security-audit skill](https://github.com/cloudflare/security-audit-skill)              | Multi-phase security audit workflow with independently verified findings        | Any                                 |
| [ctf-skills](https://github.com/ljagiello/ctf-skills)                                              | CTF skills for web exploitation, pwn, crypto, reverse engineering and forensics | Any                                 |
| [GRC Skills](https://github.com/Sushegaad/Claude-Skills-Governance-Risk-and-Compliance)            | Compliance guidance for ISO 27001, SOC 2, GDPR, HIPAA and more                  | Claude Code                         |
| [OWASP Security](https://github.com/agamm/claude-code-owasp)                                       | Review code against current OWASP Top 10 security practices                     | Claude Code                         |
| [Pashov Audit Group Skills](https://github.com/pashov/skills)                                      | Solidity security audit skills for smart contract codebases                     | Claude Code, Codex, Cursor, Copilot |
| [Trail of Bits skills](https://github.com/trailofbits/skills)                                      | Security research, vulnerability detection and audit workflows as plugins       | Claude Code, Codex                  |

### Writing & Content

| Skill                                                                              | Description                                                                      | Works with                                      |
| ---------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- | ----------------------------------------------- |
| [Aaron Marketing Skills](https://github.com/aaron-he-zhu/aaron-marketing-skills)   | 120 marketing skills across seven disciplines including SEO, GEO and content     | Claude Code, Codex, Cursor, Gemini CLI, Copilot |
| [Affiliate Skills](https://github.com/Affitor/affiliate-skills)                    | Affiliate marketing skills from program research to content and landing pages    | Claude Code, Cursor, Gemini CLI                 |
| [Agentic SEO Skill](https://github.com/Bhanunamikaze/Agentic-SEO-Skill)            | SEO audits with 16 sub-skills and evidence-collecting scripts                    | Claude Code, Codex, Cursor, Copilot             |
| [Amazon Skills (Nexscope)](https://github.com/nexscope-ai/Amazon-Skills)           | Keyword research, listing, FBA and PPC skills for Amazon sellers                 | Claude Code, Codex, Cursor                      |
| [Anti-Defensive Writing](https://github.com/Kiterlin/anti-defensive-writing)       | Remove hedging and stacked disclaimers from academic and technical prose         | Claude Code, Codex                              |
| [ASO Skills](https://github.com/appeeky/aso-skills)                                | App Store Optimization skills for keywords, metadata and competitor analysis     | Claude Code, Cursor                             |
| [avoid-ai-writing](https://github.com/conorbronsdon/avoid-ai-writing)              | Audits and rewrites text to remove AI writing patterns, with voice profiles      | Claude Code, Codex                              |
| [Baoyu Skills](https://github.com/JimLiu/baoyu-skills)                             | Skills for illustrations, covers, slide decks, translation and social posts      | Claude Code, Codex                              |
| [Beautify GitHub README](https://github.com/oil-oil/beautify-github-readme)        | Redesign repository READMEs so value, examples and install steps read clearly    | Claude Code, Codex                              |
| [Claude Ads](https://github.com/AgriciDaniel/claude-ads)                           | Paid media audits across twelve ad platforms from your account data exports      | Claude Code                                     |
| [Claude Content Skills](https://github.com/Ootto-AI/claude-content-skills)         | Instagram reel hooks, scripts, repurposing and a two-week posting calendar       | Claude Code                                     |
| [Claude SEO](https://github.com/AgriciDaniel/claude-seo)                           | SEO audits covering technical SEO, Core Web Vitals, schema, local and AI search  | Claude Code                                     |
| [Digital Marketing Pro](https://github.com/indranilbanerjee/digital-marketing-pro) | Marketing plugin covering strategy, SEO, paid media, content and CRM analytics   | Claude Code                                     |
| [Email Marketing Bible](https://github.com/CosmoBlk/email-marketing-bible)         | Audit email setups, build flows and draft copy for email marketing               | Claude Code, Codex, Cursor                      |
| [Fire Your SEO Agency](https://github.com/leopard627/fire-your-seo-agency)         | Audit and fix site SEO and AI search visibility                                  | Claude Code, Codex                              |
| [Founder Skills (ognjengt)](https://github.com/ognjengt/founder-skills)            | Copywriting, marketing and product skills for founders and creators              | Claude Code                                     |
| [Human Writing](https://github.com/KKKKhazix/human-writing)                        | Chinese writing and revision skill that checks facts and avoids filler prose     | Claude Code, Codex                              |
| [Humanize (harshaneel)](https://github.com/harshaneel/humanize)                    | Two skills that make AI writing sound human, grounded in research                | Claude Code, Codex, Cursor, Gemini CLI, Copilot |
| [Humanize Korean](https://github.com/epoko77-ai/im-not-ai)                         | Rewrite AI-generated Korean text to read naturally without changing facts        | Claude Code, Codex, Gemini CLI, Copilot         |
| [Humanizer](https://github.com/blader/humanizer)                                   | Removes telltale signs of AI writing from text while keeping its meaning         | Claude Code, Codex                              |
| [humanizer-ru](https://github.com/ilyautov/humanizer-ru)                           | Remove bureaucratic and template phrasing from Russian text while keeping facts  | Claude Code, Codex, Cursor, Copilot             |
| [Instagram Skills](https://github.com/sergebulaev/instagram-skills)                | Write Instagram captions, Reels hooks and carousels with approval before publish | Claude Code, Codex                              |
| [korean-privacy-terms](https://github.com/kimlawtech/korean-privacy-terms)         | Generate privacy policies and terms of service from Korean and global laws       | Claude Code, Codex                              |
| [LinkedIn Marketing Skills](https://github.com/sergebulaev/linkedin-skills)        | Write LinkedIn posts, comments and replies in your voice, with approval first    | Claude Code, Codex                              |
| [Marketing OS](https://github.com/Yuzzyuk/marketing-os)                            | One marketing skill with scored audits, hooks and copy across 14 modules         | Claude Code, Codex, Cursor                      |
| [Marketing Skills](https://github.com/coreyhaines31/marketingskills)               | Marketing skills for CRO, copywriting, SEO, analytics and growth                 | Any                                             |
| [Marketing Skills (kostja94)](https://github.com/kostja94/marketing-skills)        | Marketing and SEO workflows covering research, content, channels and launches    | Any                                             |
| [natural-japanese](https://github.com/coji/natural-japanese)                       | Rewrite AI-written Japanese work documents to read naturally, adding no facts    | Claude Code, Codex, Cursor                      |
| [NotFair Plugin](https://github.com/nowork-studio/notfair-plugin)                  | SEO, GEO, paid media and analytics marketing workflows for agents                | Claude Code, Codex, Cursor                      |
| [Oh Story](https://github.com/zenstory-ai/oh-story-claudecode)                     | Web novel writing skills from trend scanning to outline, drafting and covers     | Claude Code, Codex                              |
| [Open SEO MCP Skills](https://github.com/Ryze-AI-Adgent/open-seo-mcp-skills)       | SEO and GEO skills for keyword research, rank tracking and site audits           | Claude Code                                     |
| [Prompt Master](https://github.com/nidhinjs/prompt-master)                         | Writes tool-specific prompts for AI tools, from coding agents to image models    | Claude Code                                     |
| [Resume Skills](https://github.com/Paramchoudhary/ResumeSkills)                    | Skills for resume optimization, job applications and career development          | Claude Code                                     |
| [Self Media Skills](https://github.com/yanhua1010/self-media-content-workflow)     | Social media content skills from brief and research to copy and review           | Claude Code, Codex, Cursor                      |
| [Sepia](https://github.com/Nanako0129/sepia)                                       | De-AI editing for fiction and professional documents, with a general router      | Claude Code, Codex                              |
| [shuorenhua](https://github.com/MrGeDiao/shuorenhua)                               | Chinese rewrite skill that cuts filler and stock phrases while keeping facts     | Claude Code, Codex, Cursor                      |
| [sloptrim](https://github.com/seyedehsanhadi/sloptrim)                             | Detect AI-writing patterns in prose files and ask the agent to fix them          | Claude Code, Codex, Cursor                      |
| [Social Account Doctor](https://github.com/JuneYaooo/social-account-doctor)        | Account checkups and top-post teardowns for Chinese social platforms             | Claude Code, Codex, Cursor                      |
| [speak-human-tw](https://github.com/Raymondhou0917/speak-human-tw)                 | Traditional Chinese rewrite skill that fixes AI-sounding phrasing and marks      | Claude Code, Codex, Cursor                      |
| [Story Skills](https://github.com/danjdewhurst/story-skills)                       | Fiction project format with story bible, continuity checks and drafting          | Claude Code, Codex, Cursor, Gemini CLI, Copilot |
| [SuperSEO Skills](https://github.com/inhouseseo/superseo-skills)                   | SEO page audits, content briefs, articles and link plans without paste-in data   | Claude Code, Cursor                             |
| [WeChat Article Skills](https://github.com/aiworkskills/wechat-article-skills)     | WeChat account workflow from topics to writing, layout, images and publish       | Claude Code, Codex, Cursor                      |
| [X Mentor](https://github.com/alchaincyf/x-mentor-skill)                           | Writing and growth playbook for X distilled from six creators' methods           | Claude Code, Codex, Cursor                      |
| [yomiyasu](https://github.com/nanaism/yomiyasu)                                    | Refine AI-generated Japanese into natural, readable technical writing            | Claude Code, Codex, Cursor                      |

### Research & Knowledge

| Skill                                                                                                          | Description                                                                      | Works with                                      |
| -------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- | ----------------------------------------------- |
| [Agent Reach](https://github.com/Panniantong/Agent-Reach)                                                      | Read-only access to X, Reddit, YouTube, Bilibili and more for agents             | Any                                             |
| [Agent Skills for Context Engineering](https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering) | Context engineering and multi-agent design skills for production agent systems   | Claude Code, Cursor                             |
| [Answer Me With HTML](https://github.com/QingYunA/answer-me-with-html)                                         | Answer hard questions with a readable one-page HTML from a short Markdown draft  | Claude Code, Codex, Cursor                      |
| [ARIS](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep)                                       | Autonomous ML research workflows from idea discovery to paper and review         | Claude Code, Codex, Cursor, Copilot             |
| [arXiv Review Paper Harness](https://github.com/appautomaton/latex-arxiv-SKILL)                                | Write verified LaTeX review papers for arXiv from a topic                        | Claude Code, Codex                              |
| [Chubby Skills](https://github.com/chubbyguan/chubbyskills)                                                    | Save videos, podcasts and articles as searchable Markdown notes with sources     | Claude Code, Codex                              |
| [claude-obsidian](https://github.com/AgriciDaniel/claude-obsidian)                                             | Files sources into a linked Obsidian wiki that the agent maintains and queries   | Claude Code, Codex, Cursor, Gemini CLI          |
| [Claudemy](https://github.com/assafkip/claudemy)                                                               | Research any topic and turn it into short audio lessons                          | Claude Code                                     |
| [COG Second Brain](https://github.com/huytieu/COG-second-brain)                                                | Markdown second brain with skills for notes, people and review, kept in Git      | Claude Code, Codex, Cursor, Gemini CLI          |
| [Deep Research Skills](https://github.com/Weizhena/Deep-Research-skills)                                       | Two-phase deep research with an outline, parallel agents and a final report      | Claude Code, Codex                              |
| [DeepPaperNote](https://github.com/917Dhj/DeepPaperNote)                                                       | Read a paper in full and write an illustrated Obsidian deep-reading note         | Claude Code, Codex                              |
| [ex-USSR Kinship Research](https://github.com/DenisSergeevitch/ex-ussr-kinship-research)                       | Evidence-first genealogy research across former Soviet archives and church books | Claude Code, Codex                              |
| [fastCRW Skills](https://github.com/fastcrw/crw/tree/main/skills)                                              | Web search, scrape and crawl skills for the fastCRW CLI and MCP server           | Claude Code, Codex, Cursor, Gemini CLI          |
| [Hyperresearch](https://github.com/jordan-gibbs/hyperresearch)                                                 | Deep research pipeline with audited reports and a searchable source vault        | Claude Code, Codex                              |
| [ir-search](https://github.com/djfksjd/ir-search)                                                              | Survey Korean government startup grants and rank them against your project       | Claude Code, Codex, Cursor, Gemini CLI          |
| [Journalism Skills](https://github.com/jamditis/claude-skills-journalism)                                      | Skills for journalists and researchers: verification, FOIA and data work         | Claude Code, Codex                              |
| [Karpathy LLM Wiki](https://github.com/Astro-Han/karpathy-llm-wiki)                                            | Build a Karpathy-style LLM wiki with ingest, cited queries and linting           | Any                                             |
| [Lab Rat](https://github.com/fcakyon/labrat)                                                                   | ML research skills for paper reproduction, experiment design and run checks      | Claude Code, Codex, Cursor, Gemini CLI          |
| [last30days-skill](https://github.com/mvanhorn/last30days-skill)                                               | Researches a topic across Reddit, X, YouTube and the web into one summary        | Any                                             |
| [Learn From Materials](https://github.com/dmoshehun-prog/learn-from-materials)                                 | Turn books, PDFs and slides into traceable knowledge bases and learning pages    | Claude Code, Codex, Copilot                     |
| [MedSci Skills](https://github.com/Aperivue/medsci-skills)                                                     | Clinical research skills for literature, statistics, figures and manuscripts     | Claude Code, Codex, Cursor, Copilot             |
| [notebooklm-py](https://github.com/teng-lin/notebooklm-py)                                                     | Python API, CLI and skill for driving Google NotebookLM from agents              | Claude Code, Codex                              |
| [Obsidian skills](https://github.com/kepano/obsidian-skills)                                                   | Skills that teach agents the Obsidian CLI, Markdown, Bases and JSON Canvas       | Any                                             |
| [obsidian-wiki](https://github.com/Ar9av/obsidian-wiki)                                                        | Build and maintain an interlinked Obsidian wiki that agents keep current         | Claude Code, Codex, Cursor, Gemini CLI          |
| [rederive](https://github.com/EricJujianZou/rederive)                                                          | Learn a codebase by re-deriving its design decisions through questions           | Claude Code, Codex, Cursor, Gemini CLI, Copilot |
| [Scientific Agent Skills](https://github.com/K-Dense-AI/scientific-agent-skills)                               | Large science skill library for biology, chemistry, medicine and data analysis   | Claude Code, Codex, Cursor                      |
| [Serenity Stock Choke](https://github.com/fadewalk/serenity-stock-choke)                                       | Supply chain bottleneck framework for screening A-share, HK and US stocks        | Claude Code, Codex, Cursor                      |
| [Social Media Research Skills](https://github.com/ScrapeCreators/social-media-research-skills)                 | Social media research workflows across TikTok, Instagram, YouTube and Reddit     | Claude Code, Codex, Cursor, Gemini CLI, Copilot |
| [Startup Skill](https://github.com/ferdinandobons/startup-skill)                                               | Market research, competitor analysis and planning skills for startup ideas       | Claude Code                                     |
| [Video Fetcher to Markdown](https://github.com/JimmySadek/video-fetcher-to-markdown)                           | Turn video links into Obsidian-ready Markdown notes with transcripts             | Claude Code, Codex, Cursor, Gemini CLI          |
| [YouTube Skills](https://github.com/ZeroPointRepo/youtube-skills)                                              | YouTube transcripts, video search, channel and playlist data for agents          | Claude Code, Codex, Cursor                      |

### Productivity

| Skill                                                                              | Description                                                                     | Works with                                      |
| ---------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- | ----------------------------------------------- |
| [agmsg](https://github.com/fujibee/agmsg)                                          | Cross-agent messaging over a local SQLite database                              | Claude Code, Codex, Gemini CLI, Copilot         |
| [Attention Span](https://github.com/alexgreensh/attention-span)                    | ADHD-friendly answer-first output styles that cut agent verbosity               | Claude Code, Codex, Cursor                      |
| [Baidu Netdisk](https://github.com/baidu-netdisk/bdpan-storage)                    | Upload, search, read and manage Baidu Netdisk files                             | Claude Code, Codex, Cursor, Gemini CLI          |
| [Bro](https://github.com/luchasarie/bro-skill)                                     | Re-explain the last dense reply in plain language with one command              | Claude Code, Codex, Cursor                      |
| [Caveman](https://github.com/JuliusBrussee/caveman)                                | Terse agent replies and compressed tool output to cut token use                 | Claude Code, Codex, Gemini CLI                  |
| [CCPM](https://github.com/automazeio/ccpm)                                         | Spec-driven project management with PRDs, GitHub issues and parallel agents     | Claude Code, Codex, Cursor                      |
| [Chisle](https://github.com/JayPokale/Chisle)                                      | Cut token spend with terse replies, minimal code and trimmed tool output        | Claude Code, Codex, Cursor, Gemini CLI, Copilot |
| [claude-reflect](https://github.com/BayramAnnakov/claude-reflect)                  | Capture corrections and turn them into permanent memory and skills              | Claude Code                                     |
| [COMPASS Skills](https://github.com/dongshuyan/compass-skills)                     | Ten skills for agent collaboration, clear writing and skill engineering         | Claude Code, Codex                              |
| [Flowtrace](https://github.com/AIScientists-Dev/Flowtrace)                         | Run agent work as reusable, checkable steps instead of one long text stream     | Claude Code, Codex, Cursor                      |
| [Founder Skills (Emotix)](https://github.com/emotixco/claude-skills-founder)       | Startup validation, competitor research, pricing and pitch deck planning skills | Claude Code                                     |
| [huashu-mac-use](https://github.com/alchaincyf/huashu-mac-use)                     | Drive macOS native apps without APIs and keep evidence of each step             | Claude Code, Codex, Cursor                      |
| [i-have-adhd](https://github.com/ayghri/i-have-adhd)                               | Makes agents lead with the answer in short, skimmable, ADHD-friendly replies    | Claude Code, Codex, Cursor, Gemini CLI, Copilot |
| [itr-wala](https://github.com/karanb192/itr-wala)                                  | Compute and file Indian income tax returns with tested tax code                 | Claude Code, Codex, Gemini CLI                  |
| [Loopy](https://github.com/Forward-Future/loopy)                                   | Find, audit, craft and run reusable AI agent loops from a catalog               | Claude Code, Codex, Cursor                      |
| [makerskills](https://github.com/coreyhaines31/makerskills)                        | Skills for indie operators: decisions, research, second brain, content          | Claude Code, Codex, Cursor                      |
| [n8n-skills](https://github.com/czlonkowski/n8n-skills)                            | Skills for building n8n workflows with the n8n-mcp server                       | Claude Code                                     |
| [NoPUA](https://github.com/wuji-labs/nopua)                                        | Trust-based prompting skill that makes agents admit uncertainty and verify work | Claude Code, Codex, Cursor                      |
| [Offer Toolkit](https://github.com/yanliudesign/offer-toolkit-skill)               | Job hunt skills for job search, resume, interviews and offer negotiation        | Claude Code                                     |
| [Open Steps](https://github.com/kharmanskyi/open-steps)                            | Plain-language session reports and next steps for non-engineer builders         | Claude Code, Codex, Cursor, Gemini CLI          |
| [Operator Memory](https://github.com/aerovato/operator-memory)                     | Persistent markdown memory of specs, decisions and lessons for coding agents    | Claude Code, Codex                              |
| [Paperasse](https://github.com/romainsimon/paperasse)                              | Skills for French accounting, tax, invoicing and notary paperwork               | Claude Code, Codex, Cursor, Gemini CLI, Copilot |
| [Planning with Files](https://github.com/OthmanAdi/planning-with-files)            | Persistent markdown plans that survive context resets in long agent tasks       | Any                                             |
| [PM Skills](https://github.com/phuryn/pm-skills)                                   | Product management skills from discovery and strategy to launch and growth      | Claude Code, Codex                              |
| [PM Skills (product-on-purpose)](https://github.com/product-on-purpose/pm-skills)  | Product management skills across discover, define, develop and deliver          | Claude Code, Codex, Cursor, Copilot             |
| [prd-taskmaster](https://github.com/anombyte93/prd-taskmaster)                     | Turn a goal into a graded PRD, dependency-ordered tasks and verified delivery   | Claude Code                                     |
| [Project Butler](https://github.com/JamesShi96/project-butler)                     | Project memory that saves progress and resumes work across agent sessions       | Claude Code, Codex, Cursor                      |
| [shinkoku](https://github.com/kazukinagata/shinkoku)                               | Japanese tax return plugin from bookkeeping to e-Tax filing steps               | Claude Code, Cursor, Gemini CLI, Copilot        |
| [Squadra](https://github.com/dagoSte/squadra)                                      | Coordinate coding agent windows with shared tasks and independent reviews       | Claude Code, Codex, Cursor                      |
| [suyuan-skill](https://github.com/suyuan2022/suyuan-skill)                         | Skills to explain concepts, challenge AI output and export Get notes            | Claude Code                                     |
| [Thinking Skills](https://github.com/tjboudreaux/cc-thinking-skills)               | Structured reasoning skills for decisions, diagnosis, strategy and risk         | Claude Code, Codex, Cursor, Copilot             |
| [TourMind Booking Skills](https://github.com/tourmind-com/Tourmind-Booking-Skills) | Search and book hotels and flights with live rates from your agent              | Claude Code, Codex                              |
| [travel-plan-viz](https://github.com/zexuanw958-svg/travel-plan-viz)               | Offline mobile-first single-file HTML travel plans with map and daily timeline  | Claude Code, Codex                              |

### Skill Authoring

| Skill                                                                                            | Description                                                                   | Works with                  |
| ------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------- | --------------------------- |
| [Agent Skills Platform](https://github.com/FrancyJGLisboa/agent-skills-platform)                 | Turn a real workflow into a tested skill and publish it to a team marketplace | Claude Code, Codex, Copilot |
| [book-to-skill](https://github.com/virgiliojr94/book-to-skill)                                   | Converts a technical book PDF or document folder into a reusable skill        | Any                         |
| [Darwin Skill](https://github.com/alchaincyf/darwin-skill)                                       | Evaluate, improve and test skills with keep or rollback of each change        | Claude Code                 |
| [Harness (revfactory)](https://github.com/revfactory/harness)                                    | Design agent teams and the skills they use from a domain description          | Claude Code                 |
| [skill-creator (Anthropic)](https://github.com/anthropics/skills/tree/main/skills/skill-creator) | Anthropic's skill for creating, editing and evaluating other skills           | Claude Code                 |
| [skill-up](https://github.com/alibaba/skill-up)                                                  | Evaluate Agent Skills against test cases and evolve them with evidence        | Claude Code, Codex          |
| [SkillForge](https://github.com/tripleyak/SkillForge)                                            | Create, test and maintain skills with baseline and with-skill behavior checks | Claude Code, Codex          |
| [task-observer](https://github.com/rebelytics/one-skill-to-rule-them-all)                        | Meta-skill that logs corrections and gaps and suggests skill improvements     | Claude Code                 |
| [Yao Meta Skill](https://github.com/yaojingang/yao-meta-skill)                                   | Create, evaluate, package and govern reusable agent skills                    | Codex                       |

## Collections

Multi-skill packs and plugin marketplaces, listed once as a whole.

| Collection                                                                                                        | Description                                                                     | Works with                             |
| ----------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- | -------------------------------------- |
| [Agentic Awesome Skills](https://github.com/sickn33/agentic-awesome-skills)                                       | Large installable library of SKILL.md playbooks with a catalog and CLI          | Claude Code, Codex, Cursor, Gemini CLI |
| [AgentSys](https://github.com/agent-sh/agentsys)                                                                  | Plugins, agents and skills for PR, review, CI and branch workflows              | Claude Code, Codex, Cursor             |
| [AI Research Skills](https://github.com/Orchestra-Research/AI-Research-SKILLs)                                    | Large library of skills for AI research, training, inference and paper writing  | Claude Code, Codex, Cursor, Gemini CLI |
| [AI Skills (sanjay3290)](https://github.com/sanjay3290/ai-skills)                                                 | Portable skills for databases, messaging, research, TTS, DevOps and Google apps | Claude Code, Codex, Cursor, Gemini CLI |
| [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills)                                   | Hundreds of skills and plugins across engineering, marketing and product        | Claude Code, Codex, Cursor, Gemini CLI |
| [Build with Claude](https://github.com/davepoon/buildwithclaude)                                                  | Plugin marketplace of Claude Code agents, commands, hooks and skills            | Claude Code                            |
| [Claude Code Settings (feiskyer)](https://github.com/feiskyer/claude-code-settings)                               | Plugin of deep research, GitHub automation, image and handoff skills and agents | Claude Code                            |
| [Claude Code Templates](https://github.com/davila7/claude-code-templates)                                         | Catalog and CLI for Claude Code agents, commands, hooks, MCPs and skills        | Claude Code                            |
| [Claude Night Market](https://github.com/athola/claude-night-market)                                              | Plugin marketplace for Git, review, spec-driven development and agents          | Claude Code                            |
| [Claude-Codex Skills](https://github.com/levnikolaevich/claude-code-skills)                                       | Plugin suites for discovery, architecture, planning, delivery and deployment    | Claude Code, Codex                     |
| [ClaudeSkills](https://github.com/staruhub/ClaudeSkills)                                                          | Skill packages for research, product docs, decks and article writing            | Any                                    |
| [Context Engineering Kit](https://github.com/NeoLabHQ/context-engineering-kit)                                    | Marketplace of context engineering plugins for better agent results             | Claude Code, Cursor, Gemini CLI        |
| [DDC Skills for Construction](https://github.com/datadrivenconstruction/DDC_Skills_for_AI_Agents_in_Construction) | Construction skills for BIM, cost estimation, scheduling and document control   | Claude Code, Cursor, Copilot           |
| [Developer Kit](https://github.com/giuseppe-trisciuoglio/developer-kit)                                           | Plugin marketplace of spec-driven development skills and agents                 | Claude Code, Codex, Copilot            |
| [DevOps and Security Agent Skills](https://github.com/BagelHole/DevOps-Security-Agent-Skills)                     | Over 160 skills for DevOps, infrastructure, security and compliance             | Claude Code, Codex, Cursor             |
| [ECC](https://github.com/affaan-m/ECC)                                                                            | Agent harness collection of skills, memory and security tooling                 | Claude Code, Codex                     |
| [eCommerce Skills](https://github.com/nexscope-ai/eCommerce-Skills)                                               | Skills for Amazon, Shopify, eBay, Etsy, TikTok Shop and Walmart sellers         | Claude Code, Codex, Cursor             |
| [Garden Skills](https://github.com/ConardLi/garden-skills)                                                        | Six skills for code video, web design, image prompts, articles and retrieval    | Claude Code, Codex, Cursor, Gemini CLI |
| [Gleb Kalinin Skills](https://github.com/glebis/claude-skills)                                                    | About 100 skills for meetings, research, image generation, TDD and publishing   | Claude Code                            |
| [Jezweb Skills](https://github.com/jezweb/claude-skills)                                                          | Ten plugins of workflow skills for Cloudflare, React, Tailwind and dev tools    | Claude Code                            |
| [Khazix Skills](https://github.com/KKKKhazix/khazix-skills)                                                       | Six everyday skills for AI news, research analysis, writing and docs cleanup    | Claude Code, Codex, Cursor             |
| [oh-my-agent](https://github.com/first-fluke/oh-my-agent)                                                         | Skill library with 33 domain skills and specialist roles for coding agents      | Claude Code, Codex, Cursor             |
| [OK Skills](https://github.com/mxyhi/ok-skills)                                                                   | Curated skills and AGENTS.md playbooks for docs, browsers and planning          | Claude Code, Codex, Cursor             |
| [OneWave Claude Skills](https://github.com/OneWave-AI/claude-skills)                                              | Large library of sales, marketing, everyday life and coding skills              | Claude Code, Codex, Cursor, Gemini CLI |
| [PM Claude Skills](https://github.com/mohitagw15856/pm-claude-skills)                                             | Large library of product management Agent Skills with a one-command installer   | Codex, Cursor                          |
| [Posit Skills](https://github.com/posit-dev/skills)                                                               | Skills for R, Python, Quarto and data science from Posit                        | Claude Code, Codex, Cursor             |
| [Rampstack Skills](https://github.com/rampstackco/claude-skills)                                                  | Skills for brand, design, content, SEO, dev, ops and growth of websites         | Claude Code                            |
| [SenseNova Skills](https://github.com/OpenSenseNova/SenseNova-Skills)                                             | Skills for slides, infographics, Excel analysis, research and code-driven video | Any                                    |
| [Skills for Architects](https://github.com/AlpacaLabsLLC/skills-for-architects)                                   | Skills for architecture studios, real estate and workplace strategy             | Claude Code, Codex                     |
| [Sno Station Skills](https://github.com/sno-ai/sno-station-skills)                                                | Team-workflow skills such as cross-vendor peer review and verified delivery     | Claude Code, Codex                     |
| [Tons of Skills](https://github.com/jeremylongshore/tons-of-skills-marketplace)                                   | Plugin marketplace of 400+ plugins and skills with the ccpi installer CLI       | Claude Code                            |
| [Wondelai skills](https://github.com/wondelai/skills)                                                             | Skills built on business, UX and coding books, plus guided journeys             | Claude Code, Codex, Cursor             |
| [wshobson/agents](https://github.com/wshobson/agents)                                                             | Plugin marketplace of agents, skills and commands for many coding tools         | Claude Code, Codex, Cursor, Copilot    |

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
- [UI Skills](https://github.com/ibelick/ui-skills) - Registry, CLI and MCP server of UI skills for design engineers, plus its own baseline UI skills.

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
