# Codex and ChatGPT setup

Codex and ChatGPT can share the same PearlBook workflow while using different access patterns. The public repository contains the method and adapter; it does not contain the user's vault.

## Option 1: local Codex

Run Codex desktop or CLI on the computer that holds the Obsidian vault. Grant access only to the vault and a dedicated workspace. This provides the simplest file-level search, reviewable edits, and source linking.

Install or reference the [`pearlbook` skill](../../skills/codex/pearlbook/SKILL.md) so the agent applies vault-first retrieval, clinical safety, and editing boundaries consistently.

After installation, copy `references/local-config.example.md` to `references/local-config.md` inside the installed skill and set the absolute authorized vault path. The real `local-config.md` is ignored by this repository and must remain local. Start a new Codex task after installing or updating the skill so it appears in the available-skills catalog.

Chat renderers may suppress direct `obsidian://` links. Set `link_style: obsid_net` to present a normal clickable HTTPS link that redirects into the native Obsidian app on desktop or mobile. The URL includes the vault name and vault-relative note path, but not the note contents. Users who do not want that metadata in an external URL can self-host the static redirector or use plain relative paths instead.

## Option 2: Codex Remote

[Codex Remote](https://learn.chatgpt.com/docs/remote) lets a user start and steer work from a phone while the connected personal computer performs the work. The computer must remain awake and online. This is a good fit when the synced vault already lives on that computer and the user wants mobile access without creating another vault copy.

## Option 3: ChatGPT Work with a private vault tool

For access when a personal computer is unavailable, keep a synced vault on a persistent private host running Obsidian Headless. Connect ChatGPT to a narrowly scoped PearlBook MCP server that can search, read, and propose reviewable edits. Do not provide a general shell or unrestricted file-system access.

When supported by the product and workspace, a secure outbound tunnel can connect the private MCP server without exposing a public inbound service. See [Deployment options](../deployment-options.md).

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
