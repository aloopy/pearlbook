# Guided PearlBook setup

Use this workflow when the user asks to install, configure, or connect PearlBook.
Resume from the first incomplete stage instead of restarting a working setup.

## 1. Choose the access outcome

Ask one short question if the outcome is not already clear:

1. **Local:** Obsidian and Codex use the vault on this computer. Recommend this to
   beginners.
2. **Remote to this computer:** the vault stays here and the user reaches the
   computer from a phone. The computer must remain awake and online.
3. **Always-available ChatGPT:** a persistent private host holds a Headless Sync
   replica and exposes bounded PearlBook search, read, preview, and apply tools.
   Ask whether that host is an always-on personal computer or a cloud VM. If every
   personal computer may be offline, a cloud VM or future managed service is
   required.

Do not imply that a ChatGPT Project, uploaded skill, GitHub repository, or ephemeral
cloud coding task can directly read a private local vault.
Do not imply that Obsidian Sync or the PearlBook repository supplies compute. A
Headless client, MCP server, and tunnel must remain running on a real host.

## 2. Choose or create the vault

Offer an existing Obsidian vault or a new `Documents/PearlBook` vault. Ask before
creating or modifying folders. Do not search a home directory for a vault.

For local setup, prefer:

```bash
python3 scripts/setup_pearlbook.py --access local
```

The script location is relative to this skill. If the user chooses an existing
vault, do not scaffold it unless they explicitly request the starter structure.
Open the resulting folder as both the Obsidian vault and Codex project.

For a new always-available setup, first create the vault on the user's primary
device and let the user enable Obsidian Sync interactively. The public PearlBook
repository contains the framework, never the private notes.

## 3. Verify the local workflow

Before adding remote infrastructure:

1. read the local configuration;
2. search for a known note or create the welcome note with permission;
3. return its vault-relative path and clickable Obsidian link; and
4. confirm that the native Obsidian app opens it.

If this fails, fix the local path or link behavior before continuing.

## 4. Route the remote modes

- For phone-to-computer access, use the platform's remote feature and state that
  the computer must remain online.
- For always-available ChatGPT access, read `headless-chatgpt.md` and complete its
  staged verification.

## Completion report

State which mode is configured, where the private vault lives, whether access is
read-only or preview-and-confirm writable, what was actually tested, and which
component must remain running. Do not say setup succeeded based only on installed
files or generated configuration.
