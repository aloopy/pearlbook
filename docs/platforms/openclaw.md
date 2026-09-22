# OpenClaw setup

Use this adapter when the user wants a full agent on an always-on computer or private VM and prefers to contact it through a messaging app. This is the highest-control and most setup-intensive PearlBook path.

OpenClaw is the agent host in this pattern. It is not merely a vault MCP server, and it can use only the local files, browser, research tools, and messaging adapters the operator explicitly configures.

```text
Phone / configured messaging app
       |
       v
OpenClaw on a dedicated home computer
       |-- local PearlBook vault
       |-- optional clinician-authenticated browser profile
       `-- optional public research tools
```

## Operating model

- The clinician messages the agent from a phone through a supported messaging adapter chosen and secured by the user. Telegram is one example, not a requirement.
- OpenClaw reads and maintains the local Obsidian vault under the [clinical topic workflow](../../workflows/clinical-topic.md).
- If the user configures an authenticated reference, the clinician logs into it interactively on the host.
- OpenClaw may reuse that authorized browser session but receives no password, MFA seed, recovery code, or exported cookie archive.
- Obsidian Sync can make the same vault available on the phone and other computers. A single-device local vault also works if cross-device access is not needed.

CorePendium is one emergency-medicine example of an optional authenticated reference. OpenClaw and PearlBook do not require it.

## Agent handoff

An agent applying this adapter should first confirm:

1. the host that will remain online;
2. the messaging adapter the user selected;
3. the exact authorized vault path;
4. whether browser-based sources are needed at all; and
5. whether Obsidian Sync or another user-controlled backup/sync path is configured.

Do not infer Telegram, CorePendium, a VM, or multi-device Obsidian Sync from this example.

## Adapter setup (verified against docs.openclaw.ai, 2026-09-22)

### Shared rules: the vault's `AGENTS.md`

OpenClaw loads `AGENTS.md` from the agent's **workspace** at the start of every session ([agent workspace](https://docs.openclaw.ai/concepts/agent-workspace)). The default workspace is `~/.openclaw/workspace`, not your vault. Choose one:

- point the agent's workspace (`agents.defaults.workspace` or a per-agent `workspace`) at the vault so it reads the same root `AGENTS.md` that Codex and Claude Code use. OpenClaw seeds its own bootstrap files (such as `SOUL.md`) into a new workspace; set `agents.defaults.skipBootstrap: true` if you do not want them in the vault; or
- keep the default workspace and put the PearlBook rules, including the exact vault path, in that workspace's `AGENTS.md`.

The workspace is the default working directory, **not a sandbox**: absolute paths can still reach the rest of the host unless OpenClaw sandboxing is enabled ([`agents.defaults.sandbox`](https://docs.openclaw.ai/gateway/sandboxing)).

### Install the PearlBook skill

OpenClaw loads skills from these locations, highest precedence first ([skills](https://docs.openclaw.ai/tools/skills)):

| Location | Scope |
|---|---|
| `<workspace>/skills/pearlbook/` | that agent's workspace |
| `<workspace>/.agents/skills/pearlbook/` | project agent skills |
| `~/.agents/skills/pearlbook/` | personal, shared with Codex |
| `~/.openclaw/skills/pearlbook/` | managed/local skills for the Gateway |

Copy or symlink `skills/codex/pearlbook` from this repository into one of them. Keep `references/local-config.md` local.

### Gateway exposure

On a regular host install the Gateway binds to loopback, unknown DM senders receive a pairing code, and groups are allowlisted ([security](https://docs.openclaw.ai/gateway/security)). Container images default to an exposed bind, so pair them with Gateway auth. Keep these defaults, and run the built-in audit after every configuration change:

```bash
openclaw security audit
openclaw security audit --deep
```

Read the [exposure runbook](https://docs.openclaw.ai/gateway/security/exposure-runbook) before exposing the Gateway beyond loopback.

### Optional: browser sign-in with 1Password

OpenClaw documents [browser sign-in with 1Password for Claude](https://docs.openclaw.ai/gateway/1password#browser-sign-in-with-1password-for-claude): 1Password fills the login directly into the page, and the password never reaches the model, the transcript, or OpenClaw. It is narrow by design:

- a **macOS gateway host** with Chrome, the Claude in Chrome extension connected, the 1Password desktop app, and the 1Password browser extension (8.12.28 or later);
- Claude Code signed in to a direct Anthropic paid plan, with OpenClaw running the `claude-cli` backend through a CLI backend plugin that adds `--chrome`;
- 1Password for Claude connected once through the Claude desktop app; on 1Password Business an admin enables "Allow AI agents to autofill for users," and Claude Team/Enterprise Owners must enable it too; and
- **a person at the Mac to approve every credential use** (for example with Touch ID).

It does not work on headless, Linux, or remote gateways, including the unattended VM pattern. Never relay passwords or one-time codes through the messaging app instead. Use the dedicated browser profile described below for this flow too.

## Host checklist

- Use a dedicated, non-administrator operating-system account.
- Enable full-disk encryption, automatic security updates, screen locking, and device recovery controls.
- Restrict the agent to the vault and a dedicated workspace, not the entire home directory.
- Use a dedicated browser profile signed into only the licensed references PearlBook needs — never the clinician's everyday browser with EHR, email, or banking sessions.
- Enable OpenClaw sandboxing or OS-level permissions so the agent cannot reach files outside the vault and workspace.
- Complete login and MFA manually; stop for reauthentication when the session expires.
- Limit the messaging integration to the intended account or conversation and review its token handling.
- Do not send patient information, passwords, recovery codes, or licensed source text through the messaging service.
- Back up the vault independently of Obsidian Sync and the agent.

## Optional headless variant

The dedicated computer may be replaced with a persistent private host running [Obsidian Headless](https://obsidian.md/help/headless). Keep the messaging adapter and vault tool narrow; do not expose a public shell or general file browser. See [Deployment options](../deployment-options.md).

## Recovery behavior

If the host, vault, messaging adapter, Sync, or an optional authenticated source is unavailable, report exactly which component was not consulted. Do not silently fall back to model memory or claim a note was updated when the host did not apply the change.
