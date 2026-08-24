# Deployment options

PearlBook separates the **public framework** from the **private knowledge store**. The agent may run locally, on an always-on computer, or through a cloud conversation surface, but personal notes remain in a user-controlled Obsidian vault.

## Choose an access pattern

| Pattern | Phone access | Vault location | Best fit | Main limitation |
|---|---|---|---|---|
| Local agent app | Indirect | Current computer | Editing and setup | Computer must be in use |
| Remote control of a personal computer | Yes | Current computer | Low-friction mobile access | Computer must remain awake and online |
| Always-on home computer | Yes | Dedicated computer | Open-source, user-controlled operation | Most setup and maintenance |
| Private headless host | Yes | Persistent private host | Cloud availability without a desktop session | Requires secure host and tool configuration |

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

A private MCP server is one portable way to implement the narrow tool. When supported by the chosen OpenAI product and workspace, OpenAI's [Secure MCP Tunnel](https://learn.chatgpt.com/blog/connect-private-mcp-servers-to-openai-products) provides an outbound-only connection from the private network rather than requiring a public inbound endpoint.

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
