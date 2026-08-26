# Migrate an existing knowledge library

Migration is optional. New PearlBook users can begin with an empty vault, while existing users can import selected material from another notes system. Prefer an official export and treat each source application as an adapter to the same conversion pipeline.

## Choose the source adapter

Verify current export options in the source application's official documentation before beginning.

| Source | Useful official export | Likely conversion work |
|---|---|---|
| Notion | Markdown and CSV or HTML, including exported assets | Restore page hierarchy, database properties, links, and attachment paths |
| Evernote | ENEX or HTML from the desktop app | Convert ENML/HTML, preserve tags and dates, and extract attachments |
| Apple Notes | Markdown or PDF for individual notes on current macOS | Inventory notes and folders; prefer Markdown where available; plan a reviewable batch method for large libraries |
| Glass Health | No universal PearlBook path; see the historical [Glass case study](glass-migration.md) | Treat any observed internal endpoint as unstable and prefer an official export |
| Another system | Its most structured, portable official export | Map source identifiers, hierarchy, links, metadata, and media into Markdown |

Official export references:

- [Notion: export your content](https://www.notion.com/help/export-your-content)
- [Evernote: export notes and notebooks as ENEX or HTML](https://help.evernote.com/hc/en-us/articles/209005557-Export-Notes-and-Notebooks-as-ENEX-or-HTML)
- [Apple Notes: import, export, and print notes on Mac](https://support.apple.com/guide/notes/import-export-and-print-notes-not201900c07/mac)

## Reusable migration pipeline

```text
official export
      |
      v
private untouched archive
      |
      +--> inventory notes, folders, metadata, links, and attachments
      |
      v
source-specific parser
      |
      v
normalized intermediate records
      |
      +--> stable source identifier
      +--> title and source path
      +--> created / updated dates
      +--> body content
      +--> outbound links
      `--> attachment manifest
      |
      v
Markdown conversion
      |
      +--> frontmatter and provenance
      +--> internal-link rewriting
      +--> local attachment paths
      `--> unresolved-item report
      |
      v
small pilot --> human review --> resumable batch --> validation
```

Keep the raw export private and outside the public PearlBook repository. Do not migrate patient information, credentials, private browser data, or licensed reference corpora.

## Source mapping worksheet

Before writing a converter, record:

- source application and export date;
- official export format and version;
- number of notes, folders/notebooks, tags, and attachments;
- stable identifiers available for rewriting links;
- body format such as Markdown, HTML, ENML, rich text, or PDF;
- fields that must become frontmatter;
- embedded media and attachment locations;
- unsupported blocks, tables, drawings, or database views; and
- the destination taxonomy chosen by the user.

Do not infer a specialty folder structure from PearlBook examples. Preserve the user's existing organization during the pilot unless they explicitly request a new taxonomy.

## Pilot before batching

Choose a deliberately difficult sample containing:

1. a simple text note;
2. a note with headings and lists;
3. a note with tables or structured blocks;
4. a note with internal and external links;
5. a note with attachments or images; and
6. a note with tags, dates, or other important metadata.

Review the converted sample inside Obsidian. Fix the converter before running the full batch. A migration should be resumable and idempotent so a failed run does not require manual cleanup or duplicate notes.

## Validation

Compare the source inventory with the destination:

- notes converted, skipped, duplicated, and failed;
- attachments downloaded and missing;
- internal links resolved and unresolved;
- metadata preserved and dropped;
- folders or notebooks mapped;
- Markdown rendering checked on representative notes; and
- any synthetic topic stubs or inferred classifications clearly reported.

Keep a private migration report and preserve provenance in each migrated note. “No conversion errors” is not the same as semantic fidelity; human review remains necessary.
