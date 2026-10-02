---
name: pearlbook
description: Set up, search, answer from, and maintain a user-owned PearlBook clinical learning vault. Use for clinical learning questions, vault retrieval, source-linked synthesis, and explicitly authorized note updates. Do not use it as autonomous clinical decision support or to store patient information.
---

# PearlBook

This skill works in any agent that supports `SKILL.md` skills (Codex, Claude Code,
claude.ai, OpenClaw). A ChatGPT dot can also read these public instructions and
follow the linked cloud-computer adapter; do not assume a locally installed skill
is available to the dot. Platform-specific steps are labeled.

Use the narrowest authorized path to the user's private knowledge:

1. an explicitly authorized vault directory on the selected local or cloud computer;
2. a configured PearlBook MCP tool; or
3. neither, in which case state that the private vault was not consulted.

Do not search an entire home directory to discover a vault. The public PearlBook repository contains no personal notes.

Before accessing a local vault, read `references/local-config.md` when it exists. Treat that file as private machine configuration and never copy it into a repository, response, or cloud task. If the vault root has an `AGENTS.md`, follow it as the user's standing rules.

## First-run onboarding

When local configuration is absent—or the user asks to set up PearlBook—read
`references/setup.md` and guide the user from the first incomplete stage. Confirm the access outcome only if the user has not already selected it:

1. a ChatGPT dot using its own cloud computer, for users who want ChatGPT integration without an extra computer or self-hosted VM;
2. a local agent (Codex, Claude Code, or OpenClaw) beside the Obsidian vault;
3. phone access through a personal computer that remains online; or
4. a private headless host exposing narrow tools (the bundled MCP runbook covers ChatGPT).

For dot mode, use the cloud-computer route in `references/setup.md` instead of
the local setup script and private MCP stages below. It links to the canonical adapter and its sync,
configuration-storage, authentication, and recovery checks; no MCP host is required.

For the vault itself, offer two choices:

1. use an existing Obsidian vault; or
2. create a new `PearlBook` vault, recommended for beginners, at a user-approved location such as `Documents/PearlBook`.

For local setup, ask before creating or modifying any folder. Do not discover a vault by searching a home directory. After the user chooses, prefer `scripts/setup_pearlbook.py` with explicit flags (`--existing PATH`, or `--create PATH --yes`) to validate the path, optionally scaffold the starter vault (including a shared `AGENTS.md`), and write the ignored local configuration. Never pass `--yes` until the user has explicitly confirmed creation.

For local agents, explain that the private Obsidian vault folder and the agent's project or working folder should normally be the same folder. The public PearlBook repository and installed skill remain separate from the private vault.

For the private MCP host path, read `references/headless-chatgpt.md`. Treat setup as
complete only after Headless Sync is healthy, the MCP tools pass direct tests, the
preview-and-apply write flow passes with a disposable note, ChatGPT discovers the
tools, and a new chat successfully searches, reads, and—with explicit approval—
updates a known note. Pause for the user to enter Obsidian credentials, encryption
passwords, MFA, API keys, and workspace authorization directly in the
relevant terminal or website. Never ask the user to paste those secrets into chat.

## Workflow

1. Classify the request as answer-only, note lookup, note update, new note, or visual.
2. Search titles, aliases, tags, and note bodies before creating anything.
3. Inspect the canonical note and its linked sources.
4. Use a licensed reference only through the user's own logged-in account, opening the specific page the question needs, the way the user would read it. Stop for login or MFA. Never crawl, bulk-download, or copy the source into the vault.
5. For high-risk or time-sensitive claims, verify current primary or authoritative sources.
6. Answer concisely with uncertainty, local-protocol caveats, and source links where relevant.
7. Edit only when the user explicitly requests it or a configured workflow clearly authorizes it. For MCP-backed edits, read the current note, present the proposed diff, obtain explicit approval, then apply the exact previewed change. Never treat approval of one preview as approval for a later or broader edit. The MCP server cannot see the user; you and the chat client's confirmation prompt are the approval gate.
8. Validate links, attachments, and unrelated-content preservation after an edit.
9. Return the vault-relative note path, an Obsidian link when configured, and the sources materially used.

## Present vault notes in chat

Read `link_style` from the local configuration:

- `obsidian` (default): end vault-backed answers with a native link, then the plain vault-relative path as a fallback. Some chat renderers show `obsidian://` links as plain text; the path still lets the user find the note.

  ```text
  [Open “Note title” in Obsidian](obsidian://open?vault=<encoded-vault>&file=<encoded-vault-relative-path>)
  ```

- `https_bridge` (opt-in): use the configured `link_base` HTTPS redirector so the link is clickable in chat. The redirector receives the vault name and note path with every click. `obsid.net` is one third-party option run by Joost de Valk; a self-hosted redirector keeps that metadata private.
- `path`: return only the vault-relative path.

Use the vault name and vault-relative path, not an absolute local path. Percent-encode every query value, including `/` as `%2F` and spaces as `%20`. Prefer `scripts/build_obsidian_link.py` when it is available (add `--base` only for `https_bridge`). Never put a path that itself contains sensitive information into an external URL.

## Safety boundaries

- Do not store PHI, reconstructable patient cases, credentials, cookies, or browser profiles.
- Do not reproduce licensed or paywalled source content; store your own summary and a link back to the source.
- Never request, handle, or store a human password, MFA seed, or recovery code. A user-approved password-manager fill or platform private sign-in is acceptable when the secret goes directly to the intended service without reaching the agent or chat.
- Never say the vault or a source was checked when access failed.
- Treat outputs as clinician-reviewed educational knowledge management, not autonomous patient-care decisions.
- Ask before destructive, broad, or externally visible changes.
