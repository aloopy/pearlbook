---
name: pearlbook
description: Search, answer from, and maintain a user-owned PearlBook clinical learning vault. Use for clinical learning questions, vault retrieval, source-linked synthesis, and explicitly authorized note updates. Do not use it as autonomous clinical decision support or to store patient information.
---

# PearlBook

Use the narrowest authorized path to the user's private knowledge:

1. an explicitly authorized local vault directory;
2. a configured PearlBook MCP tool; or
3. neither, in which case state that the private vault was not consulted.

Do not search an entire home directory to discover a vault. The public PearlBook repository contains no personal notes.

Before accessing a local vault, read `references/local-config.md` when it exists. Treat that file as private machine configuration and never copy it into a repository, response, or cloud task.

## First-run onboarding

When local configuration is absent—or the user asks to set up PearlBook—read
`references/setup.md` and guide the user from the first incomplete stage. First ask
which access outcome they want:

1. local Obsidian plus Codex, recommended for a first setup;
2. phone access through a computer that remains online; or
3. always-available ChatGPT access through a private headless host.

For the vault itself, offer two choices:

1. use an existing Obsidian vault; or
2. create a new `PearlBook` vault, recommended for beginners, at a user-approved location such as `Documents/PearlBook`.

Ask before creating or modifying any folder. Do not discover a vault by searching a home directory. After the user chooses, prefer `scripts/setup_pearlbook.py` to validate the path, optionally scaffold the starter vault, and write the ignored local configuration. Never pass `--yes` until the user has explicitly confirmed creation.

Explain that the private Obsidian vault folder and the Codex project should normally be the same folder. The public PearlBook repository and installed skill remain separate from the private vault.

For headless ChatGPT access, read `references/headless-chatgpt.md`. Treat setup as
complete only after Headless Sync is healthy, the MCP tools pass direct tests, the
preview-and-apply write flow passes with a disposable note, ChatGPT discovers the
tools, and a new chat successfully searches, reads, and—with explicit approval—
updates a known note. Pause for the user to enter Obsidian credentials, encryption
passwords, MFA, OpenAI API keys, and workspace authorization directly in the
relevant terminal or website. Never ask the user to paste those secrets into chat.

## Workflow

1. Classify the request as answer-only, note lookup, note update, new note, or visual.
2. Search titles, aliases, tags, and note bodies before creating anything.
3. Inspect the canonical note and its linked sources.
4. Use licensed references only through a session the user authenticated. Stop for login or MFA.
5. For high-risk or time-sensitive claims, verify current primary or authoritative sources.
6. Answer concisely with uncertainty, local-protocol caveats, and source links where relevant.
7. Edit only when the user explicitly requests it or a configured workflow clearly authorizes it. For MCP-backed edits, read the current note, present the proposed diff, obtain explicit approval, then apply the exact previewed change. Never treat approval of one preview as approval for a later or broader edit.
8. Validate links, attachments, and unrelated-content preservation after an edit.
9. Return a clickable Obsidian link, the vault-relative note path, and the sources materially used.

## Present vault notes in chat

When `link_style` is `obsid_net`, end every vault-backed answer with a normal Markdown link that uses the configured HTTPS bridge:

```text
[Open “Note title” in Obsidian](https://obsid.net/?vault=<encoded-vault>&file=<encoded-vault-relative-path>)
```

Use the vault name and vault-relative path, not an absolute local path. Percent-encode every query value, including `/` as `%2F` and spaces as `%20`. Do not emit `obsidian://` directly in ChatGPT or Codex because chat renderers may leave custom URI schemes as unclickable text. Include the plain vault-relative path after the link as a fallback.

Prefer `scripts/build_obsidian_link.py` when it is available. The HTTPS URL contains the vault name and note path, but not the note contents; do not generate it for a path that itself contains sensitive information.

## Safety boundaries

- Do not store PHI, reconstructable patient cases, credentials, cookies, or browser profiles.
- Do not reproduce licensed or paywalled source content; summarize only what is needed.
- Never request or accept a human password, MFA seed, or recovery code for agent storage.
- Never say the vault or a source was checked when access failed.
- Treat outputs as clinician-reviewed educational knowledge management, not autonomous patient-care decisions.
- Ask before destructive, broad, or externally visible changes.
