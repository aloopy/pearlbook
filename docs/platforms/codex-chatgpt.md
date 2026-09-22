# Codex and ChatGPT setup

Codex and ChatGPT can share the same PearlBook workflow while using different access patterns. The public repository contains the method and adapter; it does not contain the user's vault.

Use this adapter for one of three distinct paths: local Codex beside the vault, Codex Remote steering that computer from a phone, or ChatGPT calling narrow vault tools on a persistent private host. Do not assume that ChatGPT can read a local vault merely because Codex can.

This adapter was verified against official OpenAI documentation on 2026-09-22 (first verified 2026-08-26). Platform availability depends on rollout and workspace settings; re-verify the linked documentation before relying on account-specific features.

## Option 1: local Codex

Run Codex desktop or CLI on the computer that holds the Obsidian vault. Grant access only to the vault and a dedicated workspace. This provides the simplest file-level search, reviewable edits, and source linking.

An authenticated browser is optional. If the user needs a licensed or institutional source, use a **dedicated browser profile** that is signed into only that source — not the everyday browser that holds EHR, email, or banking sessions — and let the user log in interactively. CorePendium is one emergency-medicine example, not a required integration.

### First-run setup

The simplest mental model is that the private Obsidian vault folder and the Codex project are the same folder. The public PearlBook repository and installed skill remain separate.

**1. Install the skill.** Codex loads personal skills from `~/.agents/skills` and repository skills from `.agents/skills` in the project and its parent folders up to the repository root ([Codex skills](https://developers.openai.com/codex/skills)). Either:

```bash
# Personal install from a local checkout (symlink keeps it updated with git pull)
mkdir -p ~/.agents/skills
ln -s "/path/to/pearlbook-repo/skills/codex/pearlbook" ~/.agents/skills/pearlbook
# or copy instead of linking:
# cp -R "/path/to/pearlbook-repo/skills/codex/pearlbook" ~/.agents/skills/pearlbook
```

or, in Codex, ask `$skill-installer` to install the skill folder from `https://github.com/aloopy/pearlbook/tree/main/skills/codex/pearlbook`. Codex detects new skills automatically; restart Codex if it does not appear.

**2. Run the guided setup** from the installed skill. A person in a terminal can run it with no flags for interactive prompts; an agent should pass an explicit path:

```bash
# Existing vault
python3 ~/.agents/skills/pearlbook/scripts/setup_pearlbook.py --existing "/absolute/path/to/vault"
# New starter vault after the user confirms the location
python3 ~/.agents/skills/pearlbook/scripts/setup_pearlbook.py --create "$HOME/Documents/PearlBook" --yes
```

Add `--dry-run` to preview. The setup offers two paths:

1. select an existing Obsidian vault without changing its structure; or
2. create a new `Documents/PearlBook` vault with `Inbox`, `Topics`, `Pearls`, `Cases`, `Sources`, `Templates`, `attachments`, and a root `AGENTS.md`.

The script refuses system, root, and broad home locations, avoids overwriting a non-empty folder, and writes the authorized absolute path to `references/local-config.md` inside the installed skill. That file is ignored by this repository and must remain local; you do not need to copy `local-config.example.md` yourself unless you skip the script. After setup, open that same folder as a vault in Obsidian and as the project in Codex.

**3. Keep one `AGENTS.md` at the vault root.** Codex reads it automatically ([AGENTS.md guide](https://developers.openai.com/codex/guides/agents-md)); the same file serves Claude Code and OpenClaw. For an existing vault, add it with `--scaffold-existing` or copy the rules from the starter vault.

**4. Start a new Codex task** so the [`pearlbook` skill](../../skills/codex/pearlbook/SKILL.md) is available, and verify that it finds a known note and returns its path and link.

Note links default to native `obsidian://` URIs plus the vault-relative path. Some chat renderers show `obsidian://` links as plain text. If you want clickable HTTPS links instead, opt in with `--link-style https_bridge --link-base <https-url>`. The redirector receives the vault name and note path with every click; `https://obsid.net/` is a third-party service run by Joost de Valk, and a self-hosted redirector keeps that metadata private.

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

The MCP server cannot tell whether a person approved a write. `pearlbook_apply_write`
is annotated as destructive so ChatGPT asks for confirmation before each call; keep
that confirmation and review the preview diff every time.

## Data and privacy notes

- Individual ChatGPT plans use conversations for model training by default. Turn
  off **Settings > Data controls > Improve the model for everyone** before routing
  clinical learning conversations through ChatGPT or Codex. ChatGPT Business,
  Enterprise, Edu, and the API are not used for training by default
  ([how your data is used](https://help.openai.com/en/articles/5722486-how-your-data-is-used-to-improve-model-performance)).
- Even with training off, thumbs-up/down feedback can make that whole conversation
  available for training. Do not rate conversations that contain sensitive material.
- Codex has a separate **Include environments** training setting in Codex settings.
- Avoid pasting patient details or secrets into any conversation, local or remote.

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

## Recovery behavior

If local Codex, Remote, the private host, the MCP tool, or an optional authenticated source is unavailable, state which component was not consulted. Never imply that ChatGPT inherited a host browser session or that a cloud task accessed the private vault unless that access was explicitly configured and verified.
