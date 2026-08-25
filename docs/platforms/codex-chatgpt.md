# Codex and ChatGPT setup

Codex and ChatGPT can share the same PearlBook workflow while using different access patterns. The public repository contains the method and adapter; it does not contain the user's vault.

## Option 1: local Codex

Run Codex desktop or CLI on the computer that holds the Obsidian vault. Grant access only to the vault and a dedicated workspace. This provides the simplest file-level search, reviewable edits, and source linking.

### First-run setup

The simplest mental model is that the private Obsidian vault folder and the Codex project are the same folder. The public PearlBook repository and installed skill remain separate.

Run the guided setup from the installed skill:

```bash
python3 ~/.codex/skills/pearlbook/scripts/setup_pearlbook.py
```

The setup offers two paths:

1. select an existing Obsidian vault without changing its structure; or
2. create a new `Documents/PearlBook` vault with `Inbox`, `Topics`, `Pearls`, `Cases`, `Sources`, `Templates`, and `attachments`.

The script asks before creating a new folder, refuses broad root/home locations, avoids overwriting a non-empty folder, and stores the authorized absolute path only in the ignored local skill configuration. After setup, open that same folder as a vault in Obsidian and as the project in Codex.

Install or reference the [`pearlbook` skill](../../skills/codex/pearlbook/SKILL.md) so the agent applies vault-first retrieval, clinical safety, and editing boundaries consistently.

After installation, copy `references/local-config.example.md` to `references/local-config.md` inside the installed skill and set the absolute authorized vault path. The real `local-config.md` is ignored by this repository and must remain local. Start a new Codex task after installing or updating the skill so it appears in the available-skills catalog.

Chat renderers may suppress direct `obsidian://` links. Set `link_style: obsid_net` to present a normal clickable HTTPS link that redirects into the native Obsidian app on desktop or mobile. The URL includes the vault name and vault-relative note path, but not the note contents. Users who do not want that metadata in an external URL can self-host the static redirector or use plain relative paths instead.

## Option 2: Codex Remote

[Codex Remote](https://learn.chatgpt.com/docs/remote) lets a user start and steer work from a phone while the connected personal computer performs the work. The computer must remain awake and online. This is a good fit when the synced vault already lives on that computer and the user wants mobile access without creating another vault copy.

## Option 3: ChatGPT Work with a private vault tool

For access when a personal computer is unavailable, keep a synced vault on a persistent private host running Obsidian Headless. Connect ChatGPT to a narrowly scoped PearlBook MCP server that can search, read, and propose reviewable edits. Do not provide a general shell or unrestricted file-system access.

When supported by the product and workspace, a secure outbound tunnel can connect the private MCP server without exposing a public inbound service. See [Deployment options](../deployment-options.md).

In this configuration ChatGPT is the agent and the private host is only a tool server. The host does not automatically gain ChatGPT's web tools, and ChatGPT does not automatically inherit a browser session logged in on the host. Public research remains limited to the tools and connectors available in the ChatGPT conversation. Authenticated sources require a separately designed, narrowly scoped source tool or a full agent/browser running on the host.

### Guided headless setup

The PearlBook skill now contains a staged agent runbook and a bundled stdio MCP
server with bounded search/read plus preview-and-confirm writes. Ask the agent:

> Set up PearlBook for always-available ChatGPT access.

The agent should read
[`references/headless-chatgpt.md`](../../skills/codex/pearlbook/references/headless-chatgpt.md),
resume from the first incomplete stage, and pause while the user enters every
credential directly. The workflow verifies Headless Sync, tests the MCP tools with
MCP Inspector, connects an outbound Secure MCP Tunnel, and finally tests search,
read, preview, approval, apply, and Sync from a new ChatGPT conversation.

Initial host provisioning requires terminal or remote-desktop access. Once the
host is configured and its services remain online, ordinary PearlBook use can be
performed from ChatGPT on a mobile device.

This path is currently a developer-mode, single-user setup. It is not a public
hosted PearlBook service, and availability depends on OpenAI Platform tunnel and
ChatGPT workspace permissions.

## Codex cloud tasks

[Codex cloud](https://learn.chatgpt.com/docs/cloud) is useful for developing, testing, and reviewing the public PearlBook repository in an isolated environment. It should not be the default runtime for a private vault.

OpenAI documents in [Cloud environments](https://learn.chatgpt.com/docs/environments/cloud-environment) that secrets are available to the setup script and removed before the agent phase. They are appropriate only for scoped machine credentials that are intentionally needed during setup. Never store a human password, MFA secret, browser cookie archive, Obsidian vault, or licensed-content credential in a cloud-task environment.

## Capability map

| Need | Recommended Codex/ChatGPT path |
|---|---|
| Work directly with a local vault | Local Codex |
| Message from a phone while a computer is online | Codex Remote |
| Access when the personal computer is offline | ChatGPT plus persistent private host and narrow MCP |
| Improve the public framework | Codex cloud task |

## Shared skill and future plugin

The PearlBook skill defines the behavioral contract. A future Codex/ChatGPT plugin can bundle that skill with the private MCP connector. Keep transport configuration and credentials out of the skill and out of this repository.
