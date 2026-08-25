# Headless Obsidian and ChatGPT

Use this only for a user who wants ChatGPT to reach PearlBook without depending on
their primary computer. The first synchronization test is read-only. The finished
workflow supports reviewable writes after the user explicitly enables
bidirectional Sync.

## Architecture

```text
ChatGPT
  -> OpenAI Secure MCP Tunnel
  -> bounded PearlBook MCP server
  -> dedicated Headless Sync directory
  -> Obsidian Sync
  -> the user's primary Obsidian vault
```

Headless Sync is the replication layer, not a ChatGPT API. The MCP server is the
narrow access layer. The tunnel is the private transport.

"Headless" means that Obsidian runs without the desktop application; it does not
mean that no computer is required. PearlBook and Obsidian do not currently provide
a managed server for this workflow. One host must remain powered on and connected:

- an always-on personal computer, which makes access unavailable whenever that
  computer is offline; or
- a persistent cloud VM/private server, which remains available when the user's
  personal devices are offline.

If the user selects a cloud VM, explain that the synchronized working copy is
decrypted on that VM so the MCP server can read it. Use an encrypted persistent
volume, a dedicated account, restrictive file permissions, backups, and a provider
the user is willing to trust with that private replica.

## Safety invariants

- Use a persistent, patched, encrypted host and a dedicated non-administrator
  account.
- Back up the vault before enabling another replica.
- Do not run Obsidian desktop Sync and Headless Sync on the same device. Use one
  sync method per device.
- Start with Headless Sync in `pull-only` mode. Enable bidirectional Sync only
  after search/read tests pass and before testing previewed writes.
- Never expose a home directory, shell, general filesystem root, credentials,
  cookies, or browser profile.
- The user enters Obsidian login, MFA, encryption passwords, OpenAI API keys, and
  workspace authorization directly. Do not request them in chat or place them in
  the repository.
- Do not store PHI in the vault or send patient information through this workflow.

## Stage 1: prepare the vault and host

Confirm that the user has:

- an active Obsidian Sync subscription;
- a remote vault containing the PearlBook vault;
- a persistent macOS, Linux, or Windows host; and
- Node.js 22 or later for Obsidian Headless; and
- Python 3.10 or later for the bundled MCP server.

Explicitly record which host will run the three persistent components: Headless
Sync, PearlBook MCP, and `tunnel-client`. If no host will remain online, stop: the
always-available mode cannot work.

If the host already uses Obsidian desktop Sync, stop and have the user choose a
different host or disable desktop Sync on that device before proceeding.

Run the bundled readiness check when available:

```bash
python3 scripts/check_headless_readiness.py --vault ~/PearlBookHeadless
```

Ask before installing global software or creating the directory. Then guide the
user through the official Headless commands:

```bash
npm install -g obsidian-headless
mkdir -p ~/PearlBookHeadless
ob login
ob sync-list-remote
ob sync-setup --vault "REMOTE VAULT NAME" --path ~/PearlBookHeadless --device-name pearlbook-headless
ob sync-config --path ~/PearlBookHeadless --mode pull-only
ob sync --path ~/PearlBookHeadless
ob sync-status --path ~/PearlBookHeadless
```

Pause while the user completes authentication. Do not put password or MFA flags in
shell history. Inspect `ob sync-status` and a known Markdown filename before
continuing. Run `ob sync --continuous --path ~/PearlBookHeadless` under an
OS-appropriate user service only after the one-time sync succeeds.

Official references:

- https://obsidian.md/help/headless
- https://obsidian.md/help/sync/headless

## Stage 2: install and test the MCP server

Create an isolated Python environment outside the vault. From the installed skill
or a trusted PearlBook checkout:

```bash
python3 -m venv .pearlbook-runtime
.pearlbook-runtime/bin/pip install -r skills/codex/pearlbook/scripts/requirements-mcp.txt
.pearlbook-runtime/bin/python skills/codex/pearlbook/scripts/pearlbook_mcp.py \
  --vault ~/PearlBookHeadless \
  --vault-name "PearlBook"
```

The last command runs a stdio MCP server and waits for requests. Do not type note
content into that terminal. Test it with MCP Inspector before adding the tunnel:

```bash
npx @modelcontextprotocol/inspector@latest
```

Verify the read tools first:

- `pearlbook_search` finds a known note and returns only bounded snippets;
- `pearlbook_read` reads that exact Markdown note and rejects absolute paths,
  traversal, non-Markdown files, and symlink escapes.

Then ask the user whether to enable writing. If approved, switch Headless Sync to
bidirectional mode:

```bash
ob sync-config --path ~/PearlBookHeadless --mode bidirectional
```

Use a disposable Markdown note to verify the two-step write tools:

1. `pearlbook_preview_write` requires either the SHA-256 returned by
   `pearlbook_read` or the literal `new` for a new note. It returns a unified diff
   and expiring `change_id` without changing the vault.
2. Show that diff to the user and obtain explicit approval.
3. `pearlbook_apply_write` accepts only that `change_id`, rechecks the source hash,
   and applies the exact preview atomically.
4. Confirm the new content reaches the user's primary Obsidian device through
   Sync, then remove the disposable note manually if desired.

The service intentionally provides no delete, rename, arbitrary filesystem, or
shell tool. A changed source hash invalidates the proposal so concurrent edits are
not silently overwritten.

## Stage 3: connect the private tunnel

Developer-mode tunnel availability depends on the user's OpenAI account, Platform
organization permissions, and ChatGPT workspace policy. Do not silently replace it
with an unauthenticated public forwarding URL.

1. Have the user enable ChatGPT Developer mode in **Settings -> Security and
   login**, if available.
2. Have the user create a tunnel in OpenAI Platform tunnel settings and associate
   it with the intended ChatGPT workspace.
3. Download the current `tunnel-client` from the Platform page or its official
   latest release. Do not hard-code a release URL.
4. Have the user place the runtime API key in the host's protected environment or
   secret store without pasting it into chat.
5. Initialize the tunnel with the `tunnel_id` and the full stdio command for
   `pearlbook_mcp.py`.
6. Run `tunnel-client doctor --profile <profile> --explain`, then keep
   `tunnel-client run --profile <profile>` healthy under an OS user service.

Official reference:

- https://developers.openai.com/api/docs/guides/secure-mcp-tunnels

## Stage 4: add and verify in ChatGPT

In ChatGPT Plugins, create a developer-mode app, choose **Tunnel**, select the
tunnel or enter its `tunnel_id`, and review the discovered tool metadata. Start a
new chat with the app enabled and test:

> Search PearlBook for a known topic. Read only. Cite the note path and return a
> clickable Obsidian link.

Setup is complete only if the new chat invokes `pearlbook_search`, reads the
selected note with `pearlbook_read`, returns the expected source path, previews an
authorized disposable edit, waits for approval, applies it, and the edit syncs to
the primary device. If tool discovery fails, check tunnel workspace association
and `tunnel-client` health. If retrieval or editing fails, check Headless Sync
status, sync mode, and the authorized vault path.

The one-time host setup requires terminal or remote-desktop access to the
persistent host. It is not safely mobile-only. Once the services are installed and
healthy, normal search and reviewed note updates can be performed from ChatGPT on
a phone.
