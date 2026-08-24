# PearlBook

An open framework for building a private, agent-compatible clinical learning system around an Obsidian vault, authenticated reference browsing, and a vault-first workflow.

PearlBook documents the architecture and operating habits behind **LangostaMD** without depending on a particular agent release, model vendor, or exact command syntax.

> [!IMPORTANT]
> This repository contains the **method, adapters, and sanitized examples**. It does not contain anyone's personal notes, vault, credentials, browser state, patient information, or licensed reference content.

## What this repository covers

- Setting up an Obsidian vault as the agent's durable knowledge base
- A safe, reviewable workflow for answering clinical questions and maintaining notes
- Accessing EM:RAP CorePendium through a browser session created by the clinician
- Converting a legacy Glass Health notebook into linked Markdown
- Portable capability contracts for adapting the design to other agent platforms
- Sanitized templates and checks that keep the system predictable

## Choose a setup

| Platform | Typical path | Setup guide |
|---|---|---|
| OpenClaw | Telegram to a dedicated home computer | [OpenClaw](docs/platforms/openclaw.md) |
| Codex / ChatGPT | Local Codex, Codex Remote, or a private vault tool | [Codex and ChatGPT](docs/platforms/codex-chatgpt.md) |
| Claude Code / Cowork | Platform adapter pending Claude-specific review | [Claude handoff](docs/platforms/claude.md) |

Read [Deployment options](docs/deployment-options.md) before choosing between a local, remote-to-computer, or always-available private-host configuration.

## Start here

1. Read [Architecture](docs/architecture.md).
2. Choose an access pattern in [Deployment options](docs/deployment-options.md).
3. For Codex, run the [guided first-run setup](docs/platforms/codex-chatgpt.md#first-run-setup), or create the vault manually with [Obsidian setup](docs/obsidian-setup.md).
4. Configure the [clinical topic workflow](workflows/clinical-topic.md).
5. Add authenticated reference access with [CorePendium browser workflow](workflows/corependium-browser.md).
6. Review [Security and clinical safety](SECURITY.md).
7. If migrating legacy content, see the [Glass Health case study](workflows/glass-migration.md).

## Design principles

- **Clinician-owned:** Markdown, media, and metadata remain locally inspectable.
- **Vault first:** search existing notes before drafting or editing.
- **Source before synthesis:** read the primary relevant reference before writing.
- **Human-authenticated:** users log into subscription sites; agents reuse the local session without handling credentials.
- **Reviewable:** every meaningful change has a source trail and a direct note link.
- **Portable:** workflows specify capabilities and invariants, not brittle release-specific commands.
- **Minimal:** notes are concise, useful on shift, and expanded only when the task warrants it.

## Non-goals

PearlBook does not host personal vaults, redistribute CorePendium/EM:RAP content, automate credential entry, provide a prebuilt medical corpus, or replace clinician judgment. It is infrastructure for personal learning and knowledge management.

## Project status

Early documentation release. Examples are intentionally sanitized. Contributions that improve portability, testing, accessibility, or clinical-review safeguards are welcome.

## License and attribution

The framework and original repository content are available under the [MIT License](LICENSE). Third-party products and content remain the property of their respective owners.
