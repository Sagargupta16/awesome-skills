# Security Policy

This repository contains no code that runs on your machine -- it is a list. The security risk it carries is different, and worth being explicit about.

## Why a list needs a security policy

An Agent Skill loads instructions into your coding agent and can ship scripts the agent runs with your permissions. Once installed, it can steer what the agent reads, changes and sends, and its `allowed-tools` field can pre-approve tools so the agent does not ask first. Installing one is closer to installing a shell plugin than to reading a document.

So an entry on this list is an implicit recommendation, and a malicious entry is a supply-chain attack. Every submission is checked for a real `SKILL.md`, a detectable licence, active maintenance, and an unarchived, non-forked source -- see [CONTRIBUTING.md](CONTRIBUTING.md#quality-standards). Those checks catch spam and abandonware. They do not prove any listed skill is safe.

**Read any skill's `SKILL.md` and scripts before you install it.** A green check on this list is not an audit.

## Reporting a malicious or compromised entry

If a skill on this list exfiltrates data, takes an undisclosed action, tells the agent to fetch and run remote code without saying so, hides instructions in its files, or has had its repository taken over, report it privately:

- Use [GitHub private vulnerability reporting](https://github.com/Sagargupta16/awesome-skills/security/advisories/new), or
- email **sg85207@gmail.com** with `[awesome-skills]` in the subject.

Include the entry name, the repository URL, and what you observed. A proof of concept helps but is not required.

Please do not open a public issue first. A public report tells everyone reading the list where the problem is before it can be removed.

### What happens next

- **Within 72 hours** -- acknowledgement.
- **Confirmed** -- the entry is removed from `README.md` immediately, and the commit message states why.
- **Unclear** -- the maintainer contacts the project's author for a response before acting.
- **Not reproducible** -- you get an explanation of what was checked.

Credit is given in the removal commit unless you ask otherwise.

## Reporting a problem with this repository

For issues in this repository's own tooling -- a workflow with an over-broad token, an injection in `scripts/`, a leaked secret -- use the same private channels above.

## Out of scope

- Bugs in a listed third-party skill that are not malicious behaviour. Report those to that project, then open an issue here if the project is unresponsive and the entry should be removed.
- Broken or dead links. Open a normal issue, or wait for the monthly [health report](.github/workflows/health.yml).
- Disagreement about whether an entry deserves to be listed. That is a curation question -- open an issue.
