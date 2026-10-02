# Codex and ChatGPT setup

Codex and ChatGPT can share the same PearlBook workflow while using different access patterns. The public repository contains the method and adapter; it does not contain the user's vault.

Choose local Codex beside the vault, Codex Remote steering that computer from a phone, ChatGPT calling narrow tools on a private host, or a dot using Headless Sync on its own cloud computer ([Option 4](#option-4-headless-obsidian-on-a-dot-cloud-computer)). Do not assume that ChatGPT can read a local vault merely because Codex can.

This adapter was verified against official OpenAI documentation on 2026-09-22 (first verified 2026-08-26). The dot cloud-computer persistence guidance was rechecked on 2026-10-02; cloud-environment guidance was checked on 2026-09-30. Platform availability depends on rollout and workspace settings; re-verify the linked documentation before relying on account-specific features.

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

Ask the dot to use its **own cloud computer** and choose a private, non-temporary workspace outside any repository, synced notebook, or public backup. Record separate runtime, vault, backup, and configuration paths locally. The Linux examples below use a **placeholder** workspace path: replace it consistently, including inside the wrapper. These commands are for that cloud computer, not your laptop or a Codex repository task.

On Linux, Headless 0.0.14 puts its account token, vault configuration, device identity, and sync database under `XDG_CONFIG_HOME/obsidian-headless` (falling back to `~/.config/obsidian-headless`). The vault directory alone is insufficient. In the observed failure, the desktop terminal inherited a runtime-specific configuration path under `/dev/shm`, while the execution shell used a different location. After the host changed, account and vault state were missing even though workspace files survived. A local “no account” error is not evidence of server-side token expiry. This storage behavior is visible in the [official client source](https://github.com/obsidianmd/obsidian-headless/blob/0.0.14/cli.js); recheck it when upgrading.

Pin one private `XDG_CONFIG_HOME` in every login, setup, status, and sync entry point. `--config-dir` names the vault's `.obsidian` folder; it does **not** relocate global authentication or sync state. Do not copy tokens or use `OBSIDIAN_AUTH_TOKEN` to conceal a path mismatch. Reauthenticate interactively in the chosen location.

The [dot computer documentation](https://learn.chatgpt.com/docs/dots/computers-and-apps#use-the-cloud-computer) says state can remain between uses; it specifies neither a durable credential path nor a VM-replacement guarantee. Workspace survival in one observed replacement is not such a guarantee. Keep independent private vault backups and distinguish process tests from host-restart or replacement tests.

### 2. Install the official Headless client locally

Use the maintained [Obsidian Headless client](https://github.com/obsidianmd/obsidian-headless), which requires Node.js 22 or later. The tested combination on 2026-09-30 was Node.js 24.19.0 and `obsidian-headless` 0.0.14; this is a reproducible baseline, not a claim that every cloud computer has those versions. Check current release guidance before upgrading.

```bash
node --version
# Replace this placeholder; set PB_ROOT again in each new terminal.
PB_ROOT="/path/to/private-workspace/pearlbook-private"
umask 077
mkdir -p "$PB_ROOT/runtime" "$PB_ROOT/vault" "$PB_ROOT/bin" "$PB_ROOT/config"
chmod 700 "$PB_ROOT" "$PB_ROOT/runtime" "$PB_ROOT/vault" "$PB_ROOT/bin" "$PB_ROOT/config"
cd "$PB_ROOT/runtime"
npm init --yes
npm install --save-exact obsidian-headless@0.0.14
./node_modules/.bin/ob --help
```

The workspace-local install needs no global package installation. Stop if the runtime is too old or installation is blocked; use an approved runtime or the private-host option. Keep dependencies outside the vault. Create `$PB_ROOT/bin/pb-ob` with the following contents, replacing its placeholder with the **same absolute path**, and run `chmod 700 "$PB_ROOT/bin/pb-ob"`:

```sh
#!/bin/sh
set -eu
umask 077
PB_ROOT="/path/to/private-workspace/pearlbook-private"
export XDG_CONFIG_HOME="$PB_ROOT/config"
unset OBSIDIAN_AUTH_TOKEN
exec "$PB_ROOT/runtime/node_modules/.bin/ob" "$@"
```

Use this wrapper for every authenticated command, including inside any `pb-sync.sh` helper or service. It deliberately overrides a runtime-provided XDG path on each invocation. Keep its config directory private (0700); the tested client creates token/key files with 0600 permissions. Do not print their contents, place secrets in the wrapper, or back up authentication state into a notebook or public archive. Copying it can expose credentials and duplicate device/sync identity.

### 3. Sign in privately through desktop takeover

Open **dot profile → Computers → cloud computer → Take over**. In the cloud desktop's native **Terminal**, set `PB_ROOT` to the chosen absolute workspace path from step 2, then run:

```bash
"$PB_ROOT/bin/pb-ob" login
```

Enter your Obsidian account email, account password, and MFA response at the interactive prompts yourself. Do not paste them into chat, command flags, scripts, or shell history. Then select **Return control**. The takeover controls are documented in [Computers and apps](https://learn.chatgpt.com/docs/dots/computers-and-apps).

Use the same wrapper from the desktop terminal and execution shell. Before authentication, check only paths, ownership, permissions, and a non-secret marker in the chosen config root; never dump the environment or credential files. If either context cannot access that root, stop and resolve the storage or permission mismatch before asking the user to log in.

### 4. Connect the remote vault and finish the first sync

Start with an empty local vault directory. If an earlier replica exists but its sync state is missing, follow [recovery](#7-recover-without-exposing-credentials) first. In the terminal, list vaults and select the exact remote name:

```bash
"$PB_ROOT/bin/pb-ob" sync-list-remote
"$PB_ROOT/bin/pb-ob" sync-setup \
  --vault "REMOTE VAULT NAME" \
  --path "$PB_ROOT/vault" \
  --device-name "pearlbook-cloud"
```

For an encrypted vault, take over again and enter the **vault encryption password** at the prompt. It is distinct from the Obsidian account password. Omit password flags and JSON mode so the private interactive prompt remains available; return control afterward.

Inspect settings before syncing:

```bash
"$PB_ROOT/bin/pb-ob" sync-config --path "$PB_ROOT/vault"
```

Set **pull-only** before the first sync, with configuration syncing disabled. Setup defaults to bidirectional mode, so do not run sync between setup and this configuration step:

```bash
"$PB_ROOT/bin/pb-ob" sync-config --path "$PB_ROOT/vault" \
  --mode pull-only --conflict-strategy merge --configs ""
"$PB_ROOT/bin/pb-ob" sync --path "$PB_ROOT/vault"
"$PB_ROOT/bin/pb-ob" sync-status --path "$PB_ROOT/vault"
```

Wait for the one-shot sync to finish and report **Fully synced** before editing. Check that a known note and its expected attachment arrived. Inspect file-type and exclusion settings if an image is missing; do not recreate it from memory. Confirm that notes previously deleted on the remote remain absent locally. For retrieval only, keep `pull-only` and leave writes disabled. After these checks and the user's authorization to upload changes, enable bidirectional mode explicitly:

```bash
"$PB_ROOT/bin/pb-ob" sync-config --path "$PB_ROOT/vault" --mode bidirectional
```

Bidirectional Sync uploads local changes; it is not a read-only mount. See the [official command reference](https://github.com/obsidianmd/obsidian-headless#commands).

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
5. Run the same wrapper for one-shot sync again: `"$PB_ROOT/bin/pb-ob" sync --path "$PB_ROOT/vault"`. Verify the expected uploads and **Fully synced**. Reopen the note if Sync merged changes; a successful transfer alone does not establish that a clinical merge is correct.
6. Return the exact note path and link, summarize the edit and verification, and ask the user to check arrival on another Obsidian device when available.

A note-and-source-image update completed this cloud-side sequence in testing on 2026-09-30. Arrival on a second device was not independently confirmed. This guide establishes on-demand sync, not an always-running daemon, guaranteed disk durability, or indefinite login persistence. Keep the independent backup and repeat the access/sync checks when resuming work.

### 7. Recover without exposing credentials

| Symptom | Next step |
|---|---|
| Node fetch fails with `ECONNREFUSED` while an approved HTTPS proxy is already configured | Check whether Node is using the existing proxy; use the conditional command below on a supporting runtime. |
| Script shell cannot see the desktop login, or reports “no account” | Check that both use the same wrapper, config root, and OS user. Missing local state can cause this before any server call; do not diagnose token expiry from it. If state is lost, authenticate privately in the pinned root. Never move authentication files between contexts. |
| Sync fails, is incomplete, or reports a conflict | Stop edits; keep the backup and local change, resolve connectivity or reconcile the conflict, then sync and inspect again. Do not reset or overwrite the remote vault to force success. |
| Source session expires or the site rejects cloud access | Request private login/verification, or use an authorized local browser with its own login. State when the source remains unavailable. |
| Vault files remain but account, device, or sync database state is missing | Stop sync and edits; follow the fresh-replica recovery below. Reattaching a stale directory with default bidirectional sync can upload old files and resurrect remote deletions. |
| Cloud files or setup are missing after returning | Check the recorded paths and permissions, then restore the client and use fresh-replica recovery. Do not assume paths, state, or sessions survived. |

**Fresh-replica recovery after lost sync state:** stop active sync processes; preserve the old vault as a dated private backup **outside** the active sync path. Create a new empty vault directory, use the pinned wrapper for private login and `sync-setup`, then set `pull-only` before the first sync. Verify expected notes and attachments, **Fully synced**, and that known remote deletions remain absent. Review any unsynced local changes from the backup individually; never copy the stale tree wholesale into the fresh replica. Enable bidirectional mode only after review and authorization. `mirror-remote` also downloads only but reverts local changes; do not use it to skip preserving the old replica.

**Resume and persistence checklist:**

- [ ] Desktop Terminal, execution shell, new processes, and sync helpers use the same explicit config root and wrapper.
- [ ] A non-secret marker created there is visible from each context; ownership and 0700 directory permissions are correct. Check only marker contents, never token/key contents.
- [ ] Private user login and encryption setup are complete; local vault association and settings are visible through the wrapper.
- [ ] First/recovery sync is pull-only; expected files arrived, known deletions stayed deleted, and status is fully synced.
- [ ] For authorized writes, bidirectional mode and arrival on a second device are checked separately.
- [ ] Record exactly which survival checks passed: new shell/process, later session, actual host restart, or host replacement. A new shell is **not** a VM restart test. Recheck state and sync before each resumed edit; never promise indefinite authentication or an always-on service.

In the tested Node 24.19.0 terminal, native fetch initially failed because Node had not opted into the configured proxy. When the same problem occurs, adapt the wrapper to use that existing approved route:

```bash
# Replace the wrapper's final exec line only when this proxy fix is needed:
exec node --use-env-proxy "$PB_ROOT/runtime/node_modules/.bin/ob" "$@"
```

Keep the wrapper's XDG export and restrictive umask in place so `login`, `sync-setup`, and sync all use the same state, retaining private interactive prompts. [Node documents `--use-env-proxy`](https://nodejs.org/download/release/v24.19.0/docs/api/cli.html#--use-env-proxy); it is conditional troubleshooting, not a universal Headless requirement. Do not print proxy secrets, invent a proxy, disable TLS validation, or bypass network policy. If the approved route still fails, stop and report the blocker.

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
