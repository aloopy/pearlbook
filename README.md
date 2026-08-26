# PearlBook

An open framework for building a private, agent-compatible clinical learning system around an Obsidian vault and a vault-first workflow. Public research, institutional resources, and authenticated references are optional integrations chosen by the user.

PearlBook documents the architecture and operating habits behind **LangostaMD** without depending on a particular agent release, model vendor, or exact command syntax. LangostaMD is the original emergency-medicine implementation; its taxonomy and sources are examples, not defaults.

> [!IMPORTANT]
> This repository contains the **method, adapters, and sanitized examples**. It does not contain anyone's personal notes, vault, credentials, browser state, patient information, or licensed reference content.

## What this repository covers

- Setting up an Obsidian vault as the agent's durable knowledge base
- A safe, reviewable workflow for answering clinical questions and maintaining notes
- Distinct setup paths for OpenClaw, Codex/ChatGPT, and Claude
- Optional authenticated-reference access, with EM:RAP CorePendium as an emergency-medicine example
- A reusable migration method for existing libraries, with Glass Health as one historical case study
- Portable capability contracts for adapting the design to other agents and specialties
- Sanitized templates and checks that keep the system predictable

## Choose an agent surface

The three adapters implement the same PearlBook contract but are not interchangeable deployment instructions.

| Adapter | Where the agent runs | Phone access | Authenticated browser on the host | Best fit |
|---|---|---|---|---|
| [OpenClaw](docs/platforms/openclaw.md) | An always-on personal computer or private VM | A configured messaging app | Yes, after the user logs into a dedicated browser profile | Maximum control; most setup and maintenance |
| [Codex and ChatGPT](docs/platforms/codex-chatgpt.md) | Local Codex, or ChatGPT using a narrow tool on a persistent host | Codex Remote for a connected computer; ChatGPT mobile for a private tool host | Yes with local Codex; no automatic access through a tool-only host | Direct local work, reviewable edits, and an OpenAI-native remote path |
| [Claude](docs/platforms/claude.md) | Local Claude Code, or claude.ai using a narrow tool on a persistent host | Remote Control for a connected computer; Claude mobile for a private tool host | Yes with local Claude Code and an approved browser integration; no automatic access through a tool-only host | Direct local work and a Claude-native remote path |

Read the [platform adapter index](docs/platforms/README.md) before combining components. A hybrid setup can be useful, but each additional agent, vault replica, browser profile, or write path adds conflict and security risk.

## Choose a setup

Start with the computer you can keep available, then choose the agent surface.

### 1. If you have an extra computer that can stay on

- **Run an agent on it:** install OpenClaw, keep a local Obsidian vault replica on the computer, and contact the agent through a supported messaging app. If needed, the agent can also use a dedicated browser profile that the user has logged into for selected licensed or institutional sources. See [OpenClaw](docs/platforms/openclaw.md).
- **Use it only as a private vault host:** run Obsidian Headless plus a narrow PearlBook MCP server, then access those tools from a supported ChatGPT or Claude conversation. In this pattern the host exposes vault operations; it does not automatically provide an authenticated browser or autonomous agent. See [Deployment options](docs/deployment-options.md#pattern-2-extra-computer-as-a-private-tool-host).

### 2. If your primary computer can stay on

- **Codex:** give local Codex access to the vault and, if needed, an approved user-authenticated browser profile. Use [Codex Remote](https://learn.chatgpt.com/docs/remote) from the ChatGPT mobile app. The connected computer performs the work and must remain awake and online. See [Codex and ChatGPT](docs/platforms/codex-chatgpt.md).
- **Claude:** run Claude Code beside the vault and optionally connect an approved browser integration. Start or steer work from the Claude mobile app with Remote Control while the connected computer stays awake and online. See [Claude setup](docs/platforms/claude.md).

### 3. If no personal computer can stay on

- **Private tool-host VM:** run Obsidian Headless plus a narrow PearlBook MCP server. ChatGPT or Claude supplies the agent and whatever web tools its conversation surface supports. Authenticated browsing on the VM requires separately designed source tools; it is not provided by MCP itself.
- **Agent-host VM:** run OpenClaw on the VM with the vault and, where practical and permitted, a dedicated browser session authenticated interactively by the user. Contact it through a supported messaging app. This provides more capability but adds more setup, maintenance, and security responsibility.

Read [Deployment options](docs/deployment-options.md) for the decision tree, browser boundaries, and security tradeoffs.

## Start here

### For people

1. Read [Architecture](docs/architecture.md).
2. Choose an access pattern in [Deployment options](docs/deployment-options.md).
3. Choose exactly one primary adapter from [OpenClaw](docs/platforms/openclaw.md), [Codex/ChatGPT](docs/platforms/codex-chatgpt.md), or [Claude](docs/platforms/claude.md).
4. Create or connect the vault with [Obsidian setup](docs/obsidian-setup.md).
5. Configure the [clinical topic workflow](workflows/clinical-topic.md).
6. Review [Security and clinical safety](SECURITY.md).
7. Add an authenticated reference only if useful to your field. [CorePendium](workflows/corependium-browser.md) is an optional emergency-medicine example.
8. If you already have a knowledge library, follow [Migrate an existing library](workflows/migrate-existing-library.md). The [Glass Health migration](workflows/glass-migration.md) is one case study, not a prerequisite.

### For agents

1. Read [`AGENTS.md`](AGENTS.md), [Architecture](docs/architecture.md), and [Security](SECURITY.md).
2. Identify the user's chosen platform and host pattern before changing configuration. If neither is chosen, use [Deployment options](docs/deployment-options.md) to help the user choose before applying adapter-specific steps.
3. Read only the matching platform adapter and the workflow relevant to the task.
4. Treat CorePendium, Glass Health, emergency-medicine folders, and LangostaMD conventions as examples unless the user explicitly selects them.
5. Keep the public framework, private vault, credentials, browser state, and licensed content in their documented boundaries.

For Codex, the guided skill can also be invoked by telling a compatible agent **“Set up PearlBook.”** It will choose between local, phone-to-computer, and always-available ChatGPT access, then resume from the first incomplete setup stage. Human logins and workspace authorization always remain interactive.

## Design principles

- **Clinician-owned:** Markdown, media, and metadata remain locally inspectable.
- **Vault first:** search existing notes before drafting or editing.
- **Source before synthesis:** read the primary relevant reference before writing.
- **Human-authenticated when needed:** users log into selected subscription sites; local agents may reuse the approved session without handling credentials.
- **Reviewable:** every meaningful change has a source trail and a direct note link.
- **Portable:** workflows specify capabilities and invariants, not brittle release-specific commands.
- **Minimal:** notes are concise, useful on shift, and expanded only when the task warrants it.

## Non-goals

PearlBook does not host personal vaults, provide a managed always-on server,
redistribute licensed content, automate credential entry, provide a prebuilt
medical corpus, or replace clinician judgment. It is infrastructure for personal
learning and knowledge management.

## Project status

Early documentation release. Examples are intentionally sanitized. Contributions that improve portability, testing, accessibility, or clinical-review safeguards are welcome.

## License and attribution

The framework and original repository content are available under the [MIT License](LICENSE). Third-party products and content remain the property of their respective owners.
