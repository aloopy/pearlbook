# Codex and ChatGPT setup

Codex and ChatGPT can share the same PearlBook workflow while using different access patterns. The public repository contains the method and adapter; it does not contain the user's vault.

Choose local Codex beside the vault, Codex Remote steering that computer from a phone, ChatGPT calling narrow tools on a private host, or a dot using Headless Sync on its own cloud computer ([Option 4](#option-4-headless-obsidian-on-a-dot-cloud-computer)). Do not assume that ChatGPT can read a local vault merely because Codex can.

This adapter was verified against official OpenAI documentation on 2026-09-22 (first verified 2026-08-26). The dot cloud-computer and cloud-environment guidance below was checked on 2026-09-30. Platform availability depends on rollout and workspace settings; re-verify the linked documentation before relying on account-specific features.

## Option 1: local Codex

Run Codex desktop or CLI on the computer that holds the Obsidian vault. Grant access only to the vault and a dedicated workspace. This provides the simplest file-level search, reviewable edits, and source linking.

An authenticated browser is optional. If the user needs a licensed or institutional source, use a **dedicated browser profile** that is signed into only that source — not the everyday browser that holds EHR, email, or banking sessions — and let the user log in interactively. CorePendium is one emergency-medicine example, not a required integration.

### First-run setup

Use the private Obsidian vault folder as the Codex project folder. The public PearlBook repository and installed skill remain separate.

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

Note links default to native `obsidian://` URIs plus the vault-relative path. Some chat renderers show `obsidian://` links as plain text. If you want clickable HTTPS links instead, opt in with `--link-style https_bridge --link-base <https-url>`. The redirector receives the vault name and note path with every click; `https://obsid.net/` is a third-party service run by Joost de Valk, and a self-hosted redirector lets you control who receives that metadata. See [note delivery](#deliver-a-note-link) for launch limitations.

## Option 2: Codex Remote

[Codex Remote](https://learn.chatgpt.com/docs/remote) lets a user start and steer work from a phone while the connected personal computer performs the work. The computer must remain awake and online. This is a good fit when the synced vault already lives on that computer and the user wants mobile access without creating another vault copy.

## Option 3: ChatGPT Work with a private vault tool

For access when a personal computer is unavailable, keep a synced vault on a persistent private host running Obsidian Headless. Connect ChatGPT to a narrowly scoped PearlBook MCP server that can search, read, and propose reviewable edits. Do not provide a general shell or unrestricted file-system access.

When supported by the product and workspace, a secure outbound tunnel can connect the private MCP server without exposing a public inbound service. See [Deployment options](../deployment-options.md).

In this configuration ChatGPT is the agent and the private host is only a tool server. The host does not automatically gain ChatGPT's web tools, and ChatGPT does not automatically inherit a browser session logged in on the host. Public research remains limited to the tools and connectors available in the ChatGPT conversation. Authenticated sources can use a separately authenticated browser supplied by the conversation surface, a narrowly scoped source tool, or a full agent/browser on the host. None inherits another browser's login.

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

## Option 4: Headless Obsidian on a dot cloud computer

Use this path when you want on-demand note work while your laptop is offline and your account provides a dot cloud computer with terminal and browser access. The dot reads a private Markdown replica there; Obsidian Sync exchanges files with your other devices. A separate cloud-browser login supplies trusted-source access. This path does not require the private MCP server or tunnel from Option 3.

The durable workflow is **capture → retrieve → verify → minimal update → link**. Keep an independent vault backup, authorize the replica and each edit, and require clinician review of clinical content. The cloud replica is decrypted and readable by the agent; end-to-end encrypted transport does not make that working copy inaccessible to its host. Keep PHI out of it.

### 1. Prepare the vault and choose private folders

You need an active Obsidian Sync subscription, an existing remote vault, its account login, and its separate end-to-end encryption password if enabled. Finish syncing and back up the original vault first. Use one Sync client per local replica; do not point desktop Sync and Headless Sync at the same directory.

Ask the dot to use its **own cloud computer**, choose a private workspace outside any public repository, and record the runtime and vault paths for later use. The following Linux adapter example uses generic paths under your cloud home folder; substitute your chosen locations consistently. These commands are for that cloud computer, not your laptop or a Codex repository task.

### 2. Install the official Headless client locally

Use the maintained [Obsidian Headless client](https://github.com/obsidianmd/obsidian-headless), which requires Node.js 22 or later. The tested combination on 2026-09-30 was Node.js 24.19.0 and `obsidian-headless` 0.0.14; this is a reproducible baseline, not a claim that every cloud computer has those versions. Check current release guidance before upgrading.

```bash
node --version
mkdir -p "$HOME/pearlbook-private/runtime" "$HOME/pearlbook-private/vault"
chmod 700 "$HOME/pearlbook-private"
cd "$HOME/pearlbook-private/runtime"
npm init --yes
npm install --save-exact obsidian-headless@0.0.14
./node_modules/.bin/ob --help
```

The workspace-local install needs no global package installation. Stop if the runtime is too old or installation is blocked; use an approved runtime or the private-host option. Keep dependencies outside the vault.

### 3. Sign in privately through desktop takeover

Open **dot profile → Computers → cloud computer → Take over**. In the cloud desktop's native **Terminal**, run:

```bash
cd "$HOME/pearlbook-private/runtime"
./node_modules/.bin/ob login
```

Enter your Obsidian account email, account password, and MFA response at the interactive prompts yourself. Do not paste them into chat, command flags, scripts, or shell history. Then select **Return control**. The takeover controls are documented in [Computers and apps](https://learn.chatgpt.com/docs/dots/computers-and-apps).

Keep subsequent authenticated commands in that same terminal context. A script execution shell may share files with the desktop yet not see its login. If another shell reports that you are signed out, return to the authenticated context; do not copy tokens, dump credential files, or assume shared folders imply shared authentication.

### 4. Connect the remote vault and finish the first sync

In the authenticated terminal, list vaults and select the exact remote name:

```bash
./node_modules/.bin/ob sync-list-remote
./node_modules/.bin/ob sync-setup \
  --vault "REMOTE VAULT NAME" \
  --path "$HOME/pearlbook-private/vault" \
  --device-name "pearlbook-cloud"
```

For an encrypted vault, take over again and enter the **vault encryption password** at the prompt. It is distinct from the Obsidian account password. Omit password flags and JSON mode so the private interactive prompt remains available; return control afterward.

Inspect settings before syncing:

```bash
./node_modules/.bin/ob sync-config --path "$HOME/pearlbook-private/vault"
```

The tested setup used **bidirectional** Sync, **merge** conflict handling, and disabled configuration syncing. Bidirectional means local changes can upload; it is not a read-only mount. Confirm those choices fit your intended workflow. For this read/write example, make them explicit:

```bash
./node_modules/.bin/ob sync-config --path "$HOME/pearlbook-private/vault" \
  --mode bidirectional --conflict-strategy merge --configs ""
./node_modules/.bin/ob sync --path "$HOME/pearlbook-private/vault"
./node_modules/.bin/ob sync-status --path "$HOME/pearlbook-private/vault"
```

Wait for the one-shot sync to finish and report **Fully synced** before editing. Check that a known note and its expected attachment arrived. Inspect file-type and exclusion settings if an image is missing; do not recreate it from memory. For retrieval only, choose `--mode pull-only` before the first sync and leave writes disabled. See the [official command reference](https://github.com/obsidianmd/obsidian-headless#commands).

### 5. Connect a trusted source and optionally save its login

Source access is independent of Obsidian Sync. The dot's cloud browser starts with its own sessions; your laptop's subscription login does not carry over.

1. Ask the dot to open the intended source's actual website and one relevant chapter or page. Use only your own authorized subscription and keep this browser signed into the sources needed for the work.
2. When login is needed, use the built-in **private sign-in form**, checking the destination first. It fills the remote site without putting credentials in the conversation or exposing them to the model. Alternatively, take over the browser and log in directly.
3. Complete MFA, CAPTCHA, and medical or legal terms yourself. The agent must wait for you; a subscription or cloud-browser restriction is not permission to bypass it.
4. If offered, choose **Save to Passwords** to retain the login in the managed password facility. This is optional. Confirm any later request to reuse it. A saved password and a currently signed-in session are different; either may need your attention later.
5. Return control and have the dot verify access to the relevant full page, not merely a title or preview. If access fails, report that the source was not read.

The [official sign-in guidance](https://learn.chatgpt.com/docs/dots/computers-and-apps#sign-in-to-a-website) describes this handoff. Never give the agent a password to type or ask it to inspect the password store, export cookies, or move credentials into a repository/environment secret. Read one relevant chapter at a time, summarize in your own words, and retain its URL and review date. Do not mirror a licensed reference corpus. Verify high-risk claims against current authoritative sources and retain clinician oversight.

### 6. Make and verify one authorized update

Use the [clinical topic workflow](../../workflows/clinical-topic.md) after every fresh sync:

1. Search existing titles, aliases, links, and note bodies; read the canonical note and its cited sources before creating anything new.
2. Preserve any user-provided source image unchanged, provided it is appropriate to retain and contains no PHI. Record its provenance and initial SHA-256; do not confuse it with permission to archive licensed screenshots.
3. Back up the original note outside the synced vault in a private backup folder, and record its SHA-256. Propose the smallest useful change with source links and dates. Apply only the authorized change after reviewing the diff.
4. Recheck the original hash immediately before writing. If another edit changed it, reread and reconcile rather than overwrite. Verify the final diff, frontmatter, internal links, attachment paths, and the unchanged image hash.
5. Run the same one-shot `ob sync --path` command again in the authenticated context. Verify the expected uploads and **Fully synced**. Reopen the note if Sync merged changes; a successful transfer alone does not establish that a clinical merge is correct.
6. Return the exact note path and link, summarize the edit and verification, and ask the user to check arrival on another Obsidian device when available.

A note-and-source-image update completed this cloud-side sequence in testing on 2026-09-30. Arrival on a second device was not independently confirmed. This guide establishes on-demand sync, not an always-running daemon, guaranteed disk durability, or indefinite login persistence. Keep the independent backup and repeat the access/sync checks when resuming work.

### 7. Recover without exposing credentials

| Symptom | Next step |
|---|---|
| Node fetch fails with `ECONNREFUSED` while an approved HTTPS proxy is already configured | Check whether Node is using the existing proxy; use the conditional command below on a supporting runtime. |
| Script shell cannot see the desktop login | Continue in the native terminal that completed login; reauthenticate privately if required. Never move authentication files between contexts. |
| Sync fails, is incomplete, or reports a conflict | Stop edits; keep the backup and local change, resolve connectivity or reconcile the conflict, then sync and inspect again. Do not reset or overwrite the remote vault to force success. |
| Source session expires or the site rejects cloud access | Request private login/verification, or use an authorized local browser with its own login. State when the source remains unavailable. |
| Cloud files or setup are missing after returning | Recreate the private replica from Sync and the independent backup, repeat private authentication, and finish sync before editing. Do not assume old paths or sessions survived. |

In the tested Node 24.19.0 terminal, native fetch initially failed because Node had not opted into the configured proxy. This command used the existing approved route:

```bash
node --use-env-proxy "$HOME/pearlbook-private/runtime/node_modules/.bin/ob" \
  sync --path "$HOME/pearlbook-private/vault"
```

Use the same prefix for `login` or `sync-setup` if those commands encounter the same issue, retaining their private interactive prompts. [Node documents `--use-env-proxy`](https://nodejs.org/download/release/v24.19.0/docs/api/cli.html#--use-env-proxy); it is conditional troubleshooting, not a universal Headless requirement. Do not print proxy secrets, invent a proxy, disable TLS validation, or bypass network policy. If the approved route still fails, stop and report the blocker.

## Deliver a note link

Use the [official Obsidian URI](https://obsidian.md/help/uri), with the vault name and vault-relative path URL-encoded. For a synthetic note:

```text
obsidian://open?vault=PearlBook&file=Topics%2FExample%20topic.md
```

Include `Topics/Example topic.md` as a fallback. The receiving device must have Obsidian and the matching vault/note. An HTTPS bridge such as `obsid.net` can make a link clickable in renderers that suppress custom schemes, but sends vault/path metadata in its URL. Obtain the user's opt-in before using a third-party bridge. A redirect may require a tap or opening the system browser; neither a native URI nor a bridge guarantees launch from a mobile in-app browser. Never include note text, credentials, or a cloud filesystem path in the link.

## Apply the workflow to Notion and other notebooks

The capture → retrieve → verify → minimal update → link loop is portable; the storage adapter changes. Obsidian Headless synchronizes an Obsidian filesystem vault. It does not synchronize Notion automatically.

For Notion, use an available authorized connector or the [official API authorization flow](https://developers.notion.com/guides/get-started/authorization). Grant access only to the needed pages/databases and verify read and write permissions separately. Retrieve the canonical page and its blocks/properties, preserve database structure and relationships, preview a minimal authorized update, then reread it and return its native page link. Use page IDs and native semantics rather than treating pages as Markdown file paths.

The Notion sequence is adaptation guidance, not a tested integration in this walkthrough. For other notebooks, first establish supported retrieval, editing, version/backup, and link capabilities. If the adapter is read-only, return a proposed edit; if a capability is untested, say so. A one-time export into Obsidian is a [migration](../../workflows/migrate-existing-library.md), not ongoing bidirectional synchronization. Browser login to a reference site does not grant notebook API permissions.

## Data and privacy notes

Review the applicable [Work cloud security and retention guidance](https://learn.chatgpt.com/docs/enterprise/chatgpt-work-cloud-security) before placing a replica on a cloud computer. Clearing browser data, removing files, and deleting a conversation are separate actions.

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

Saved [Codex Cloud environments](https://learn.chatgpt.com/docs/environments/cloud-environments) have their own environment variables, network secrets, and **Personal vault** for requested personal values. Network secrets use destination-scoped HTTPS substitution; direct variables are readable by programs. These facilities belong to that environment surface. They are not the dot browser's Passwords store, and their availability does not imply that secrets or authentication carry over to a dot computer. Use only scoped machine credentials appropriate to public-framework development. Never store a human password, MFA secret, browser cookie archive, Obsidian vault, or licensed-content credential in a cloud-task environment.

## Capability map

| Need | Recommended Codex/ChatGPT path |
|---|---|
| Work directly with a local vault | Local Codex |
| Message from a phone while a computer is online | Codex Remote |
| On-demand vault work while the personal computer is offline | Dot cloud computer with Headless Sync and separate source login (Option 4), when available |
| Operate a persistent private vault service | ChatGPT plus private host and narrow MCP (Option 3) |
| Improve the public framework | Codex cloud task |

## Shared skill and future plugin

The PearlBook skill defines the behavioral contract. A future Codex/ChatGPT plugin can bundle that skill with the private MCP connector. Keep transport configuration and credentials out of the skill and out of this repository.

## Recovery behavior

If local Codex, Remote, the private host, the MCP tool, or an optional authenticated source is unavailable, state which component was not consulted. Never imply that ChatGPT inherited a host browser session or that a cloud task accessed the private vault unless that access was explicitly configured and verified.
