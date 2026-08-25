# Deployment options

PearlBook separates the **public framework** from the **private knowledge store**. Personal notes remain in a user-controlled Obsidian vault. Start by deciding which computer can remain available, then decide whether that computer will run a full agent or only expose narrow vault tools.

## Agent host versus tool host

These are different architectures even when they use the same computer or VM.

| Capability | Agent host | Tool host |
|---|---|---|
| Example | OpenClaw with messaging | Obsidian Headless plus PearlBook MCP |
| Where reasoning runs | On the host agent | In ChatGPT or Claude |
| Vault search and reviewable edits | Local | Through narrow MCP tools |
| Public web research | Host agent's configured tools | Conversation surface's available tools |
| Reuse a browser logged into a licensed source | Yes, when a browser is installed and the user authenticated it | No, not unless explicit source/browser tools are added to the server |
| General autonomous work on the host | Yes, within configured permissions | No; MCP only exposes the tools that were implemented |

An MCP server is a tool provider, not an agent. A VM running only Obsidian Headless and PearlBook MCP can search and update the vault, but it does not independently browse, plan, or reuse an authenticated browser profile. ChatGPT or Claude remains the agent and can use only the tools available on that conversation surface plus the narrow MCP tools the host exposes.

## Choose by the computer you can keep available

### Pattern 1: extra computer as an agent host

Run OpenClaw on a dedicated home computer and contact it through a supported messaging app such as Telegram.

```text
Phone / messaging app
         |
         v
OpenClaw on always-on computer
   |-- local Obsidian vault replica
   |-- dedicated authenticated browser profile
   `-- public research tools
```

This is the most open and controllable option. It can combine the local vault with sources that are impractical or impermissible to copy into the vault, because the agent can navigate a browser session that the user authenticated interactively. It is also the most setup-intensive home configuration. See [OpenClaw setup](platforms/openclaw.md).

### Pattern 2: extra computer as a private tool host

Run Obsidian Headless plus a narrow PearlBook MCP server. ChatGPT or Claude performs the reasoning and calls the private vault tools.

```text
ChatGPT or Claude on phone
         |
         v
Secure private MCP connection
         |
         v
Always-on tool host
   |-- PearlBook MCP
   `-- Obsidian Headless --> Obsidian Sync
```

This is simpler and narrower than running a full agent. It is well suited to vault search, reading, source-linked synthesis, and preview-before-apply edits. Browsing is limited to the public web, connectors, and browser capabilities available to the ChatGPT or Claude conversation unless the MCP server deliberately exposes additional source-specific tools. It cannot automatically reuse a browser login stored on the host.

### Pattern 3: primary computer as an agent host

If a user's normal Mac or Windows PC can remain awake and online, run the agent locally beside the vault.

- **Codex:** use local vault access and a dedicated user-authenticated browser profile, then start or steer work from a phone with [Codex Remote](https://learn.chatgpt.com/docs/remote). The connected computer performs the task.
- **Claude:** use the corresponding local and remote path only after a Claude agent verifies the current official capabilities and security model. See the [Claude handoff](platforms/claude.md).

This is usually the easiest capable setup because there is no separate server or second vault replica. Its availability depends on the user's everyday computer remaining powered, connected, patched, and unlocked as required by the chosen platform.

### Pattern 4: private VM when no personal computer can stay on

A private VM replaces the always-on physical computer. It can be configured in either role:

1. **Tool-host VM:** Obsidian Headless plus PearlBook MCP. ChatGPT or Claude is the agent. This gives stable vault availability but no authenticated VM browsing by default.
2. **Agent-host VM:** OpenClaw plus the vault and optional browser automation. This can support authenticated sources after the user logs into a dedicated browser session, but it requires more operating-system, browser, credential, update, backup, and monitoring work.

The VM is usually the most reliable option for users willing to pay and maintain it. Treat it as a sensitive endpoint: the synchronized vault exists in decrypted form while the host is running.

Obsidian Sync replicates vault files between authorized devices. It is not a general-purpose hosted REST API for agents. Obsidian's supported automation path is [Obsidian Headless](https://obsidian.md/help/headless), currently documented as open beta, which can sync a vault on a persistent machine without the desktop application.

Headless does not eliminate the machine; it eliminates the desktop UI. Obsidian
Sync does not run PearlBook code. If all personal computers may be offline, an
always-on private VM/VPS must run Headless Sync, the PearlBook MCP server, and the
outbound tunnel. PearlBook does not currently provide a managed hosted service.

## Recommended tiers

### 1. Local first

Give the agent access only to the vault directory and its dedicated workspace. This is the simplest and most inspectable configuration.

### 2. Phone to a personal computer

Use a platform's remote-control surface or a narrowly configured messaging adapter. The personal computer holds the synced vault and performs retrieval locally. It must remain awake, online, patched, and encrypted.

### 3. Always-available private host

Run Obsidian Headless on a persistent private host with an active Obsidian Sync subscription:

```bash
npm install -g obsidian-headless
ob login
ob sync-setup
ob sync --continuous
```

Obsidian currently documents Node.js 22 or later. Back up the vault before initial setup, and do not run desktop Sync and Headless Sync against the same local vault on one device.

Expose only narrow PearlBook operations to the conversation surface, for example:

- search note titles, aliases, tags, and bodies
- read one selected note
- propose or apply one reviewable note change
- return a source link and exact note path

Do not expose unrestricted shell access, the host home directory, browser storage, or a general file-system root.

```text
Phone
  |
  v
Agent conversation surface
  |
  v
Narrow PearlBook tool
  |
  v
Persistent private host
  |-- Obsidian Headless --> Obsidian Sync
  `-- approved vault directory
```

A private MCP server is one portable way to implement the narrow tool. When supported by the chosen OpenAI product and workspace, OpenAI's [Secure MCP Tunnel](https://developers.openai.com/api/docs/guides/secure-mcp-tunnels) provides an outbound-only connection from the private network rather than requiring a public inbound endpoint. The tunnel transports MCP calls; it does not run the agent, sync the vault, or add browser capabilities.

## Browsing boundary

Keep three different browser paths explicit:

1. **Browser beside a local agent:** Codex, Claude, or OpenClaw may use a local browser profile that the user authenticated, subject to platform permissions and the source's terms.
2. **Browser supplied by the conversation surface:** ChatGPT or Claude may provide public web search, browser use, or connectors. Those capabilities run outside the private host and do not inherit the host's logged-in browser session.
3. **Source tools exposed through MCP:** a private host may expose narrowly designed tools for approved sources. This is additional implementation work and should not become an unrestricted browser proxy.

For licensed references, do not automate passwords, MFA, CAPTCHA, or session export. Prefer interactive user login, narrow retrieval, and source linking without copying a paywalled corpus into the vault.

The Codex/ChatGPT skill includes a bounded stdio MCP implementation and a guided
[headless setup runbook](../skills/codex/pearlbook/references/headless-chatgpt.md).
It exposes bounded Markdown search, exact-note reads, and hash-checked
preview-and-confirm writes from one explicit vault root. It intentionally provides
no delete, rename, shell, or arbitrary filesystem operations. Treat this as a
private developer-mode deployment; public plugin distribution has different
hosting and authentication requirements.

## Why not sync inside every cloud task?

Ephemeral coding tasks are designed to check out a repository, run setup, make changes, and end. They are a poor home for a personal vault because they require repeated synchronization, expand the number of copies, complicate conflict handling, and increase the chance of sensitive files entering logs or patches.

Use cloud coding tasks to develop and test the public PearlBook framework. Use a persistent private host for private-vault access.

## Recovery behavior

If the private host, Sync, authenticated reference session, or narrow tool is unavailable, the agent must say that the vault or source was not consulted. It should never silently substitute model memory for private knowledge.
