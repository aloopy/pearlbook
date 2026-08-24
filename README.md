# Pearlbook

A release-agnostic blueprint for a clinician-owned medical knowledge agent built around an Obsidian vault, authenticated reference browsing, and a vault-first clinical workflow.

Pearlbook documents the architecture and operating habits behind **LangostaMD** without depending on a particular OpenClaw release, model vendor, or exact command syntax.

## What this repository covers

- Setting up an Obsidian vault as the agent's durable knowledge base
- A safe, reviewable workflow for answering clinical questions and maintaining notes
- Accessing EM:RAP CorePendium through a browser session created by the clinician
- Converting a legacy Glass Health notebook into linked Markdown
- Portable capability contracts for adapting the design to other agent platforms
- Sanitized templates and checks that keep the system predictable

## Start here

1. Read [Architecture](docs/architecture.md).
2. Create the vault with [Obsidian setup](docs/obsidian-setup.md).
3. Configure the [clinical topic workflow](workflows/clinical-topic.md).
4. Add authenticated reference access with [CorePendium browser workflow](workflows/corependium-browser.md).
5. Review [Security and clinical safety](SECURITY.md).
6. If migrating legacy content, see the [Glass Health case study](workflows/glass-migration.md).

## Design principles

- **Clinician-owned:** Markdown, media, and metadata remain locally inspectable.
- **Vault first:** search existing notes before drafting or editing.
- **Source before synthesis:** read the primary relevant reference before writing.
- **Human-authenticated:** users log into subscription sites; agents reuse the local session without handling credentials.
- **Reviewable:** every meaningful change has a source trail and a direct note link.
- **Portable:** workflows specify capabilities and invariants, not brittle release-specific commands.
- **Minimal:** notes are concise, useful on shift, and expanded only when the task warrants it.

## Non-goals

Pearlbook does not redistribute CorePendium/EM:RAP content, automate credential entry, provide a prebuilt medical corpus, or replace clinician judgment. It is infrastructure for personal learning and knowledge management.

## Project status

Early documentation release. Examples are intentionally sanitized. Contributions that improve portability, testing, accessibility, or clinical-review safeguards are welcome.

## License and attribution

Choose a repository license before accepting broad outside contributions. Third-party products and content remain the property of their respective owners.
