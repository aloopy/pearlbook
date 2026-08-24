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

When local configuration is absent, offer two choices:

1. use an existing Obsidian vault; or
2. create a new `PearlBook` vault, recommended for beginners, at a user-approved location such as `Documents/PearlBook`.

Ask before creating or modifying any folder. Do not discover a vault by searching a home directory. After the user chooses, prefer `scripts/setup_pearlbook.py` to validate the path, optionally scaffold the starter vault, and write the ignored local configuration. Never pass `--yes` until the user has explicitly confirmed creation.

Explain that the private Obsidian vault folder and the Codex project should normally be the same folder. The public PearlBook repository and installed skill remain separate from the private vault.

## Workflow

1. Classify the request as answer-only, note lookup, note update, new note, or visual.
2. Search titles, aliases, tags, and note bodies before creating anything.
3. Inspect the canonical note and its linked sources.
4. Use licensed references only through a session the user authenticated. Stop for login or MFA.
5. For high-risk or time-sensitive claims, verify current primary or authoritative sources.
6. Answer concisely with uncertainty, local-protocol caveats, and source links where relevant.
7. Edit only when the user explicitly requests it or a configured workflow clearly authorizes it.
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
