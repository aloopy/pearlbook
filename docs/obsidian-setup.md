# Obsidian setup

## 1. Create a local-first vault

Create the vault in a normal user-owned directory. Give the agent access only to the vault and any dedicated workspace it needs. A symlink can provide a stable short path while the real vault remains in a synced or backed-up location.

After installing the PearlBook skill for your agent, you can run the guided `setup_pearlbook.py` script from the installed skill. It can configure an existing vault or, with confirmation, create a generic starter vault named `PearlBook`. The vault folder should normally be opened as the agent's project or working folder as well.

Keep one `AGENTS.md` at the vault root as the shared rules for every agent (Codex, Claude Code, OpenClaw). The starter vault includes one; see the platform pages for how each agent loads it.

Do not place credentials, browser profiles, or raw patient data in the vault.

For an always-available private host, Obsidian documents [Obsidian Headless](https://obsidian.md/help/headless) as its automation-oriented Sync client. Review [Deployment options](deployment-options.md) before creating another vault replica.

## 2. Recommended structure

The guided starter uses a specialty-neutral structure:

```text
Vault/
├── Topics/
├── Cases/
├── Pearls/
├── Sources/
├── Templates/
├── attachments/
└── Inbox/
```

Adapt taxonomy to the clinician's field and mental model. An emergency-medicine user might organize `Topics/` into cardiovascular, neurologic, pediatrics, procedures, and toxicology; another specialty should use its own natural categories. Folder names are less important than consistency, searchable titles, aliases, and cross-links.

## 3. Note types

### Topic notes

Long-lived clinical subjects. Keep them specialty-focused and easy to scan:

- recognition and phenotype
- immediate actions
- diagnostic pivots
- doses, targets, and thresholds
- disposition
- dangerous pitfalls
- source links

### Pearls

One question or teaching point per note. Use these when a comprehensive review would bury the useful answer.

### Cases

De-identified learning records. Never commit PHI. Capture the diagnostic pivot, management lesson, and links to durable topic notes.

### Specialty or language collections

Optional collections can hold institutional pathways, procedural checklists, teaching material, or practical language resources. These folders are user choices, not required PearlBook structure.

### Canvas

Use Obsidian Canvas for algorithms, chalk talks, anatomy, and multi-branch decisions when the visual relationship adds value.

## 4. Frontmatter

A minimal topic template:

```markdown
---
title: "Topic"
aliases: []
tags:
  - clinical-knowledge
status: active
updated: YYYY-MM-DD
---

> [!source] Primary reference
> [Source title](https://example.org/source)

# Topic

## Recognition

## Actions

## Pitfalls

## Disposition

## Sources
```

Imported notes may also retain provenance fields such as `source`, `source_id`, and original creation/update dates.

Emergency-medicine users may add a CorePendium callout or EM-specific headings. Those are optional conventions rather than requirements of the base template.

## 5. Attachments and links

- Store media inside the vault under predictable subfolders.
- Prefer relative Obsidian embeds such as `![[attachments/topic/image.png]]`.
- Preserve originals when performing crops or annotations.
- Use `[[wikilinks]]` for internal concepts.
- Validate renamed notes for broken links.

PearlBook's default note link is a native Obsidian URI plus the plain vault-relative path:

```text
obsidian://open?vault=<vault-name>&file=<percent-encoded-vault-relative-path>
```

Some chat surfaces show `obsidian://` links as plain text. If you want a clickable link there, you can opt into an HTTPS bridge (`link_style: https_bridge` with a `link_base`). A bridge receives the vault name and note path with every click, so never use it for paths that could identify a patient. `https://obsid.net/` is one such bridge, run by a third party (Joost de Valk), not by Obsidian; the original LangostaMD setup used it. A self-hosted static redirector keeps the metadata private.

Treat the bridge as optional adapter behavior, not a core requirement.

## 6. Search-before-create rule

Before creating a note:

1. Search file names, aliases, tags, and bodies.
2. Inspect likely matches.
3. Prefer updating the canonical note or adding a pearl linked to it.
4. Create a new topic only when the concept is genuinely distinct.
5. Add reciprocal links where they improve retrieval.

This avoids duplicate pages such as “DKA,” “Diabetic Ketoacidosis,” and “Adult DKA” silently diverging.

## 7. Backups and version control

Back up the vault independently of the agent. Git is useful for Markdown history but may be awkward for large media; a private remote or encrypted backup is usually appropriate. Public repositories should contain only deliberately sanitized examples.

## 8. Validation checklist

- YAML parses
- internal links resolve
- attachment paths exist
- no PHI or secrets
- main source link is present
- note density matches its purpose
- chat response links to the exact note
