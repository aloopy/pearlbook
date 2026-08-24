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

## Workflow

1. Classify the request as answer-only, note lookup, note update, new note, or visual.
2. Search titles, aliases, tags, and note bodies before creating anything.
3. Inspect the canonical note and its linked sources.
4. Use licensed references only through a session the user authenticated. Stop for login or MFA.
5. For high-risk or time-sensitive claims, verify current primary or authoritative sources.
6. Answer concisely with uncertainty, local-protocol caveats, and source links where relevant.
7. Edit only when the user explicitly requests it or a configured workflow clearly authorizes it.
8. Validate links, attachments, and unrelated-content preservation after an edit.
9. Return the exact note path or configured Obsidian link plus the sources materially used.

## Safety boundaries

- Do not store PHI, reconstructable patient cases, credentials, cookies, or browser profiles.
- Do not reproduce licensed or paywalled source content; summarize only what is needed.
- Never request or accept a human password, MFA seed, or recovery code for agent storage.
- Never say the vault or a source was checked when access failed.
- Treat outputs as clinician-reviewed educational knowledge management, not autonomous patient-care decisions.
- Ask before destructive, broad, or externally visible changes.
