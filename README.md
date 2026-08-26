# PearlBook

An open framework for building a private, agent-compatible clinical learning system around an Obsidian vault and a vault-first workflow. Public research, institutional resources, and authenticated references are optional integrations chosen by the user.

PearlBook documents the architecture and operating habits behind **LangostaMD** without depending on a particular agent release, model vendor, or exact command syntax. LangostaMD is the original emergency-medicine implementation; its taxonomy and sources are examples, not defaults.

> [!IMPORTANT]
> This repository contains the **method, adapters, and sanitized examples**. It does not contain anyone's personal notes, vault, credentials, browser state, patient information, or licensed reference content.

## Start here

### For people

1. **Create or choose the private vault.** Use an existing Obsidian vault or create a new `PearlBook` vault with [Obsidian setup](docs/obsidian-setup.md). Keep it separate from this public repository.
2. **Choose where PearlBook will run.** Use your primary computer, an extra always-on computer, or a private VM. [Deployment options](docs/deployment-options.md) explains what remains available when a computer is offline.
3. **Configure one primary agent.** Follow [OpenClaw](docs/platforms/openclaw.md), [Codex/ChatGPT](docs/platforms/codex-chatgpt.md), or [Claude](docs/platforms/claude.md). Do not install all three by default.
4. **Verify the core workflow.** Confirm that the agent can search a known note, read it, return an exact clickable link, and preview an authorized edit before applying it.
5. **Review the boundaries.** Before enabling remote access or adding private sources, read [Architecture](docs/architecture.md), the [clinical topic workflow](workflows/clinical-topic.md), and [Security and clinical safety](SECURITY.md).
6. **Add phone or always-available access only after the core works.** Remote control, messaging, Headless Sync, MCP, and VMs are deployment layers; none replaces the vault or supplies an agent by itself.
7. **Add optional content last.** Migrate an [existing library](workflows/migrate-existing-library.md) if needed, then add institutional or licensed sources useful to your field. [CorePendium](workflows/corependium-browser.md) and the [Glass Health migration](workflows/glass-migration.md) are examples, not requirements.

If you use Codex, you can tell the agent **“Set up PearlBook.”** The guided skill resumes from the first incomplete stage and pauses for every folder choice, login, credential, and workspace authorization that requires you.

### For agents

1. Read [`AGENTS.md`](AGENTS.md), [Architecture](docs/architecture.md), and [Security](SECURITY.md).
2. Identify the user's chosen platform and host pattern before changing configuration. If neither is chosen, use [Deployment options](docs/deployment-options.md) to help the user choose before applying adapter-specific steps.
3. Read only the matching platform adapter and the workflow relevant to the task.
4. Treat CorePendium, Glass Health, emergency-medicine folders, and LangostaMD conventions as examples unless the user explicitly selects them.
5. Keep the public framework, private vault, credentials, browser state, and licensed content in their documented boundaries.

## What this repository covers

- Setting up an Obsidian vault as the agent's durable knowledge base
- A safe, reviewable workflow for answering clinical questions and maintaining notes
- Distinct setup paths for OpenClaw, Codex/ChatGPT, and Claude
- Optional authenticated-reference access, with EM:RAP CorePendium as an emergency-medicine example
- A reusable migration method for existing libraries, with Glass Health as one historical case study
- Portable capability contracts for adapting the design to other agents and specialties
- Sanitized templates and checks that keep the system predictable

## Compare the agent options

The three adapters implement the same PearlBook contract but are not interchangeable deployment instructions.

| Adapter | Where the agent runs | Phone access | Authenticated browser on the host | Best fit |
|---|---|---|---|---|
| [OpenClaw](docs/platforms/openclaw.md) | An always-on personal computer or private VM | A configured messaging app | Yes, after the user logs into a dedicated browser profile | Maximum control; most setup and maintenance |
| [Codex and ChatGPT](docs/platforms/codex-chatgpt.md) | Local Codex, or ChatGPT using a narrow tool on a persistent host | Codex Remote for a connected computer; ChatGPT mobile for a private tool host | Yes with local Codex; no automatic access through a tool-only host | Direct local work, reviewable edits, and an OpenAI-native remote path |
| [Claude](docs/platforms/claude.md) | Local Claude Code, or claude.ai using a narrow tool on a persistent host | Remote Control for a connected computer; Claude mobile for a private tool host | Yes with local Claude Code and an approved browser integration; no automatic access through a tool-only host | Direct local work and a Claude-native remote path |

Read the [platform adapter index](docs/platforms/README.md) before combining components. A hybrid setup can be useful, but each additional agent, vault replica, browser profile, or write path adds conflict and security risk.

## Choose by computer availability

### Primary computer stays on

- **Codex:** work locally beside the vault and use [Codex Remote](https://learn.chatgpt.com/docs/remote) from the ChatGPT mobile app.
- **Claude:** work locally beside the vault and use Remote Control from the Claude mobile app.

The connected computer performs the work and must remain awake and online. An authenticated browser is optional.

### Extra computer stays on

- **Full agent host:** run OpenClaw with a local vault replica and contact it through a supported messaging app.
- **Private tool host:** run Obsidian Headless plus narrow PearlBook MCP tools, then call them from ChatGPT or Claude. The host exposes vault operations; it does not automatically provide an agent or authenticated browser.

### No personal computer stays on

- **Private tool-host VM:** run Obsidian Headless plus PearlBook MCP; ChatGPT or Claude remains the agent.
- **Agent-host VM:** run OpenClaw with the vault and any explicitly configured browser or research tools.

A VM improves availability but adds cost, maintenance, and responsibility for a decrypted vault replica. Read [Deployment options](docs/deployment-options.md) before choosing this route.

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
