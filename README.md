# PearlBook

An open framework for building a private, agent-compatible clinical learning system around an Obsidian vault and a vault-first workflow. Public research, institutional resources, and authenticated references are optional integrations chosen by the user.

PearlBook documents the architecture and operating habits behind **LangostaMD** without depending on a particular agent release, model vendor, or exact command syntax. LangostaMD is the original emergency-medicine implementation; its taxonomy and sources are examples, not defaults.

> [!IMPORTANT]
> This repository contains the **method, adapters, and sanitized examples**. It does not contain anyone's personal notes, vault, credentials, browser state, patient information, or licensed reference content.

## Start here

### Use a ChatGPT dot without an extra computer

**Choose a dot if you want PearlBook in ChatGPT without keeping an extra laptop running or setting up and hosting your own VM.** A dot has its own cloud computer and browser. You can take over that computer to authenticate privately, then return control so it can work with an authorized Obsidian Headless replica while your personal devices are offline. See [OpenAI's computer and login guide](https://learn.chatgpt.com/docs/dots/computers-and-apps).

This also brings the notebook workflow together with ChatGPT's available research, [image generation](https://learn.chatgpt.com/docs/image-generation), and [file tools](https://learn.chatgpt.com/docs/artifacts-viewer). For example, give your dot a teaching-board photo: it can verify the content against sources, flag a correction for your review, create a clearer teaching graphic and PDF with clickable references, and file the result in your notebook when authorized. Follow the [board-pearl workflow](workflows/board-pearl-linked-pdf.md); check which tools your account provides and review the clinical content.

To start, send your dot:

> Read https://github.com/aloopy/pearlbook and help me set up PearlBook on your own cloud computer. Follow the dot setup in the ChatGPT adapter, use Obsidian Headless for my notebook, and guide me through private login. I want to capture teaching material, retrieve my notes, and make source-linked updates. Confirm the private vault location and access before making changes.

The [step-by-step dot setup](docs/platforms/codex-chatgpt.md#option-4-headless-obsidian-on-a-dot-cloud-computer) covers Obsidian Sync, private authentication, optional saved source logins, and recovery. You still need a Sync subscription, a backup, and permission to place a decrypted replica on the cloud computer. Reading the repository starts the guided setup; it does not install a local skill in the cloud or grant vault access automatically. No separate MCP host is required for this path.

Spaced-repetition questions drawn from your notes are a future direction to explore, not a configured PearlBook feature or a promise of improved retention.

### For people

1. **Create or choose the private vault.** Use an existing Obsidian vault or create a new `PearlBook` vault with [Obsidian setup](docs/obsidian-setup.md). Keep it separate from this public repository.
2. **Choose where PearlBook will run.** Choose a dot's cloud computer, your primary computer, an extra always-on computer, or a private VM you manage. [Deployment options](docs/deployment-options.md) explains what remains available when a computer is offline.
3. **Configure one primary agent.** Follow [OpenClaw](docs/platforms/openclaw.md), [Codex/ChatGPT](docs/platforms/codex-chatgpt.md), or [Claude](docs/platforms/claude.md). Do not install all three by default. Keep one `AGENTS.md` at the vault root as the shared rules file; have the selected agent read it before working on the vault.
4. **Verify the core workflow.** Confirm that the agent can search a known note, read it, return an exact clickable link, and preview an authorized edit before applying it.
5. **Review the boundaries.** Before enabling remote access or adding private sources, read [Architecture](docs/architecture.md), the [clinical topic workflow](workflows/clinical-topic.md), and [Security and clinical safety](SECURITY.md).
6. **Verify access from your phone after the core works.** A dot can use its own cloud computer; remote access to a personal computer requires that computer to stay online. Headless Sync and MCP are optional deployment components, not agents by themselves.
7. **Add optional content last.** Migrate an [existing library](workflows/migrate-existing-library.md) if needed, then add institutional or licensed sources useful to your field. [CorePendium](workflows/corependium-browser.md) and the [Glass Health migration](workflows/glass-migration.md) are examples, not requirements.

For agents with local skill support, after installing the [`pearlbook` skill](skills/codex/pearlbook/SKILL.md) for your agent (see its platform page), you can tell the agent **“Set up PearlBook.”** The guided skill resumes from the first incomplete stage and pauses for every folder choice, login, credential, and workspace authorization that requires you.

### For agents

1. Read [`AGENTS.md`](AGENTS.md), [Architecture](docs/architecture.md), and [Security](SECURITY.md).
2. Identify the user's chosen platform and host pattern before changing configuration. If neither is chosen, use [Deployment options](docs/deployment-options.md) to help the user choose before applying adapter-specific steps.
3. Read only the matching platform adapter and the workflow relevant to the task.
4. Treat CorePendium, Glass Health, emergency-medicine folders, and LangostaMD conventions as examples unless the user explicitly selects them.
5. Keep the public framework, private vault, credentials, browser state, and licensed content in their documented boundaries.

## What this repository covers

- Setting up an Obsidian vault as the agent's durable knowledge base
- A safe, reviewable workflow for answering clinical questions and maintaining notes
- A [board-pearl graphic and linked-PDF workflow](workflows/board-pearl-linked-pdf.md), with a reusable prompt and optional notebook capture
- Distinct setup paths for ChatGPT dots, local Codex, OpenClaw, Claude, and private tool hosts
- Optional authenticated-reference access, with EM:RAP CorePendium as an emergency-medicine example
- A reusable migration method for existing libraries, with Glass Health as one historical case study
- Portable capability contracts for adapting the design to other agents and specialties
- Sanitized templates and checks that keep the system predictable

## Compare the agent options

The platform adapters implement the same PearlBook contract. Choose both the agent and the computer it will use.

| Adapter | Where the agent runs | Phone access | Authenticated browser on the host | Best fit |
|---|---|---|---|---|
| [OpenClaw](docs/platforms/openclaw.md) | An always-on personal computer or private VM | A configured messaging app | Yes, after the user logs into a dedicated browser profile | Maximum control; most setup and maintenance |
| [ChatGPT dot](docs/platforms/codex-chatgpt.md#option-4-headless-obsidian-on-a-dot-cloud-computer) | Its own cloud computer; no extra computer or self-hosted VM needed | ChatGPT on your phone | Its own browser, with private user login | Notebook work alongside ChatGPT research, image, and file tools |
| [Codex / ChatGPT private tools](docs/platforms/codex-chatgpt.md) | Local Codex, or a narrow tool on a host you maintain | Codex Remote or ChatGPT with private tools | Local Codex browser; no inherited login through a tool-only host | Direct local work or a narrowly scoped private service |
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

- **Dot cloud computer:** use on-demand Obsidian Headless Sync and a separately authenticated cloud browser. Follow the [step-by-step ChatGPT setup](docs/platforms/codex-chatgpt.md#option-4-headless-obsidian-on-a-dot-cloud-computer), including private login, optional saved passwords, and recovery. Keep an independent vault backup; this path does not promise a continuously running sync service.
- **Private tool-host VM:** run Obsidian Headless plus PearlBook MCP; ChatGPT or Claude remains the agent.
- **Agent-host VM:** run OpenClaw with the vault and any explicitly configured browser or research tools.

A VM you manage adds hosting cost and maintenance. A dot supplies the cloud computer; both cloud paths still require care for the decrypted vault replica and its backup. Read [Deployment options](docs/deployment-options.md) before choosing this route.

## Design principles

- **Clinician-owned:** Markdown, media, and metadata remain locally inspectable.
- **Vault first:** search existing notes before drafting or editing.
- **Source before synthesis:** read the primary relevant reference before writing.
- **Human-authenticated when needed:** users log into selected subscription sites in a dedicated browser profile; the authorized local or cloud agent may reuse that session, one page at a time for the user's question, without handling credentials.
- **Reviewable:** every meaningful change has a source trail and a direct note link.
- **Portable:** workflows specify capabilities and invariants, not brittle release-specific commands.
- **Minimal:** notes are concise, useful on shift, and expanded only when the task warrants it.

## Non-goals

PearlBook does not host personal vaults, provide a managed always-on server,
redistribute or mirror licensed content, let an agent handle or store credentials,
provide a prebuilt medical corpus, or replace clinician judgment. (A password-manager
fill or platform private sign-in that the user approves is allowed when the secret
goes directly to the intended service and never reaches the agent.) It is infrastructure for personal
learning and knowledge management.

## Project status

Early documentation release. Examples are intentionally sanitized. Contributions that improve portability, testing, accessibility, or clinical-review safeguards are welcome.

## License and attribution

The framework and original repository content are available under the [MIT License](LICENSE). Third-party products and content remain the property of their respective owners.
