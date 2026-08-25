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

Start with the computer you can keep available, then choose the agent surface.

### If you have an extra computer that can stay on

- **Run an agent on it:** install OpenClaw, keep a local Obsidian vault replica on the computer, and contact the agent through a supported messaging app. The agent can also use a dedicated browser profile that the user has logged into for licensed or otherwise authenticated knowledge sources. See [OpenClaw](docs/platforms/openclaw.md).
- **Use it only as a private vault host:** run Obsidian Headless plus a narrow PearlBook MCP server, then access those tools from a supported ChatGPT or Claude conversation. In this pattern the host exposes vault operations; it does not automatically provide an authenticated browser or autonomous agent. See [Deployment options](docs/deployment-options.md#pattern-2-extra-computer-as-a-private-tool-host).

### If your primary computer can stay on

- **Codex:** give local Codex access to the vault and a user-authenticated browser profile, then use [Codex Remote](https://learn.chatgpt.com/docs/remote) from the ChatGPT mobile app. The connected computer performs the work and must remain awake and online. See [Codex and ChatGPT](docs/platforms/codex-chatgpt.md).
- **Claude:** run Claude Code beside the vault, then start or steer work from the Claude mobile app with Remote Control while the connected computer stays awake and online. See [Claude setup](docs/platforms/claude.md).

### If no personal computer can stay on

- **Private tool-host VM:** run Obsidian Headless plus a narrow PearlBook MCP server. ChatGPT or Claude supplies the agent and whatever web tools its conversation surface supports. Authenticated browsing on the VM requires separately designed source tools; it is not provided by MCP itself.
- **Agent-host VM:** run OpenClaw on the VM with the vault and, where practical and permitted, a dedicated browser session authenticated interactively by the user. Contact it through a supported messaging app. This provides more capability but adds more setup, maintenance, and security responsibility.

Read [Deployment options](docs/deployment-options.md) for the decision tree, browser boundaries, and security tradeoffs.

## Start here

1. Read [Architecture](docs/architecture.md).
2. Choose an access pattern in [Deployment options](docs/deployment-options.md).
3. For Codex, run the [guided first-run setup](docs/platforms/codex-chatgpt.md#first-run-setup); for Claude, follow [Claude setup](docs/platforms/claude.md); or create the vault manually with [Obsidian setup](docs/obsidian-setup.md).
4. Configure the [clinical topic workflow](workflows/clinical-topic.md).
5. Add authenticated reference access with [CorePendium browser workflow](workflows/corependium-browser.md).
6. Review [Security and clinical safety](SECURITY.md).
7. If migrating legacy content, see the [Glass Health case study](workflows/glass-migration.md).

You can also tell a compatible agent **“Set up PearlBook”**. The PearlBook skill
will choose between local, phone-to-computer, and always-available ChatGPT access,
then resume from the first incomplete setup stage. Human logins and workspace
authorization always remain interactive.

## Design principles

- **Clinician-owned:** Markdown, media, and metadata remain locally inspectable.
- **Vault first:** search existing notes before drafting or editing.
- **Source before synthesis:** read the primary relevant reference before writing.
- **Human-authenticated:** users log into subscription sites; agents reuse the local session without handling credentials.
- **Reviewable:** every meaningful change has a source trail and a direct note link.
- **Portable:** workflows specify capabilities and invariants, not brittle release-specific commands.
- **Minimal:** notes are concise, useful on shift, and expanded only when the task warrants it.

## Non-goals

PearlBook does not host personal vaults, provide a managed always-on server,
redistribute CorePendium/EM:RAP content, automate credential entry, provide a
prebuilt medical corpus, or replace clinician judgment. It is infrastructure for
personal learning and knowledge management.

## Project status

Early documentation release. Examples are intentionally sanitized. Contributions that improve portability, testing, accessibility, or clinical-review safeguards are welcome.

## License and attribution

The framework and original repository content are available under the [MIT License](LICENSE). Third-party products and content remain the property of their respective owners.
