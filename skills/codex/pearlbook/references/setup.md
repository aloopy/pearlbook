# Guided PearlBook setup

Use this workflow when the user asks to install, configure, or connect PearlBook.
Resume from the first incomplete stage instead of restarting a working setup.
Commands below are relative to the installed skill folder (for example
`~/.agents/skills/pearlbook` for Codex or `.claude/skills/pearlbook` for Claude Code).

## 1. Choose the access outcome

Ask one short question if the outcome is not already clear:

1. **Dot cloud computer:** recommend this to ChatGPT users who want to avoid an
   extra always-on computer or a VM they host themselves. The dot uses its own
   cloud computer for an authorized Headless replica and available ChatGPT tools.
2. **Local:** Obsidian and a local agent (Codex, Claude Code, or OpenClaw) use the
   vault on this computer.
3. **Remote to this computer:** the vault stays here and the user reaches the
   computer from a phone. The computer must remain awake and online.
4. **Private tool host:** a persistent host maintained by the user holds a Headless
   replica and exposes bounded PearlBook search, read, preview, and apply tools.
   Determine whether that host is a personal computer or a private VM.

Do not imply that a ChatGPT Project, uploaded skill, GitHub repository, or ephemeral
cloud coding task can directly read a private local vault. A dot supplies a cloud
computer, but access still requires explicit vault setup and authorization.
Obsidian Sync replicates files; it does not supply an agent. The private tool-host
path additionally needs its MCP server and tunnel to remain running.

### Route dot setup directly to the cloud-computer adapter

When dot mode is selected, read the current
[dot setup in the ChatGPT adapter](https://github.com/aloopy/pearlbook/blob/main/docs/platforms/codex-chatgpt.md#option-4-headless-obsidian-on-a-dot-cloud-computer).
Use that sequence instead of the local installer and MCP stages below. This URL
also works when the skill was copied without the rest of the repository. If the
adapter cannot be retrieved, report that blocker rather than inventing commands.

Confirm cloud terminal/browser availability, the authorized remote vault, and
private runtime, replica, backup, and configuration locations. A new vault must
first be created in Obsidian and uploaded through the user's Sync account. Follow
the adapter's pinned configuration-root and wrapper instructions in every terminal
context, and its recovery sequence if prior sync state is missing.

Pause for private account login, MFA, and the separate vault encryption password;
never ask for secrets in chat. Source-browser login is a separate optional step.
Finish the first sync before reading/editing, verify a known note and link, and
apply only an explicitly authorized, reviewed test edit. Confirm its upload and
report cross-device arrival separately. Do not call authentication, persistence,
or recovery verified merely because the runtime or wrapper is installed.

Keep the workflow rules in the private vault's root `AGENTS.md` and have the dot
read them; do not assume automatic local-skill loading in the cloud. Once the core
works, check available image/file tools for optional teaching-artifact workflows.
Then provide the completion report below. No extra computer, MCP server, or tunnel
is needed for this route.

## 2. Choose or create the vault for local and private-host modes

Offer an existing Obsidian vault or a new `Documents/PearlBook` vault. Ask before
creating or modifying folders. Do not search a home directory for a vault.

Agents run the script non-interactively, so always pass an explicit path. Preview
first with `--dry-run`:

```bash
# Existing vault (structure is left unchanged)
python3 scripts/setup_pearlbook.py --existing "/absolute/path/to/vault" --dry-run
python3 scripts/setup_pearlbook.py --existing "/absolute/path/to/vault"

# New starter vault, only after the user confirms the location
python3 scripts/setup_pearlbook.py --create "$HOME/Documents/PearlBook" --dry-run
python3 scripts/setup_pearlbook.py --create "$HOME/Documents/PearlBook" --yes
```

A person in a terminal can run `python3 scripts/setup_pearlbook.py` with no flags
for the interactive prompts.

If the user chooses an existing vault, do not scaffold it unless they explicitly
request the starter structure (`--scaffold-existing`). Open the resulting folder as
both the Obsidian vault and the agent's project folder.

The starter vault includes a root `AGENTS.md` with the shared PearlBook rules. Codex
and OpenClaw read it directly, and Claude Code v2.1.277+ reads it when no
`CLAUDE.md` exists. For an existing vault, offer to add the same file.

Links default to native `obsidian://` URIs. Only if the user wants clickable links in
a chat app that ignores them, offer `--link-style https_bridge --link-base <https-url>`
and explain that the redirector sees the vault name and note path.

For a new private tool-host setup, first create the vault on the user's primary
device and let the user enable Obsidian Sync interactively. The public PearlBook
repository contains the framework, never the private notes.

## 3. Verify the local workflow

Before adding remote infrastructure:

1. read the local configuration;
2. search for a known note or create the welcome note with permission;
3. return its vault-relative path and Obsidian link; and
4. confirm that the native Obsidian app opens it.

If this fails, fix the local path or link behavior before continuing.

## 4. Route the remote modes

- For phone-to-computer access, use the platform's remote feature and state that
  the computer must remain online.
- For the private tool-host mode, read `headless-chatgpt.md` and complete its
  staged verification.

## Completion report

State which mode is configured, where the private vault lives, whether access is
read-only or preview-and-confirm writable, what was actually tested, and what
availability depends on. Distinguish a personal computer or private service that
must stay online from on-demand work on the dot's supplied cloud computer. Do not say setup succeeded based only on installed
files or generated configuration.
