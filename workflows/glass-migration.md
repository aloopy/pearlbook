# Glass Health to Obsidian: migration case study

This is an optional historical case study, not a standard PearlBook setup step. Most users will migrate from another application or begin with an empty vault; start with the generic [migration workflow](migrate-existing-library.md).

The account below describes one personal notebook migration performed in February 2026. The private source data and conversion scripts are not assumed to be available, and the described internal endpoints may change or disappear.

Before attempting a similar export, confirm that you own or may export the material and that the method complies with current terms and law. Prefer an official export when available.

## Outcome

The migration converted approximately:

- 256 notebook pages
- 273 remote images
- scripts, schemas, general pages, journal-club notes, and cases
- internal page connections and external references

The resulting vault contained 256 migrated notes plus 16 deliberately created topic stubs. Counts are historical, not a guarantee for other exports.

## Discovery

While the user was logged into Glass Health, the browser session exposed an internal JSON endpoint:

```text
/api/pages/?with_connections=true
```

A second endpoint provided collection/list mappings:

```text
/api/page_lists/
```

The authenticated page returned the notebook data as TinyMCE-style HTML with page UUIDs, collection metadata, connections, and remote image URLs. Data was retrieved through the existing authenticated browser context; credentials and cookies were not extracted.

**Do not treat internal endpoints as a stable public API.** Inspect the current application and use an official export if one exists.

## Conversion pipeline

```text
authenticated export
       |
       v
raw JSON archive (private)
       |
       +--> page inventory and UUID/title map
       |
       v
HTML normalization with a DOM parser
       |
       +--> table placeholders
       +--> image URL inventory
       +--> internal-link resolution
       |
       v
HTML-to-Markdown conversion
       |
       +--> restore GFM tables
       +--> rewrite images to local paths
       +--> add provenance frontmatter
       |
       v
pilot vault --> visual review --> batch conversion --> validation
```

The implementation used Node.js with:

- `jsdom` for DOM parsing
- `turndown` for HTML-to-Markdown conversion
- `turndown-plugin-gfm` for tables and other GFM features

Use maintained equivalents if these are no longer suitable.

## Hard parts

### Complex tables

Tables contained lists, emphasis, links, and images inside cells. Converting the full document in one pass flattened or escaped content.

The converter therefore:

1. parsed the document with a DOM implementation
2. converted each table cell independently
3. normalized internal newlines to `<br>`
4. replaced each table with a placeholder
5. converted the surrounding document
6. restored the generated Markdown tables

### Internal links

Glass links included page UUIDs. A complete UUID-to-title mapping was built before conversion, then resolvable links were rewritten as Obsidian `[[wikilinks]]`. Unresolved targets were logged for review rather than silently discarded.

### Remote images

Remote images were downloaded into `attachments/glass-images/`. Filenames were derived from stable URL hashes to avoid collisions. Markdown references were then rewritten to local vault-relative paths.

Keep the raw URL manifest until migration validation is complete. Remote assets can disappear before text pages do.

### Folder inference

Collections mapped naturally to most specialty folders. Unclassified pages used explicit keyword rules as a fallback. Inference was logged and reviewed because automated taxonomy is error-prone.

## Provenance template

```markdown
---
title: "Page title"
source: glass-health
source_type: script
source_id: UUID
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags:
  - glass-import
---

[Converted content]
```

The original vault used `glass_type` and `glass_id`; generic `source_type` and `source_id` are more portable.

## Test strategy

1. Save an untouched raw export privately.
2. Inventory page types, collections, links, tables, and images.
3. Convert five deliberately diverse pages.
4. Review them inside Obsidian.
5. Fix link, table, image, and folder rules.
6. Test a second, larger sample.
7. Run the batch conversion with resumable checkpoints.
8. Validate counts, attachments, internal links, and Markdown rendering.
9. Keep a migration report with unresolved items.

The original batch processed groups of 25 and saved progress after each batch.

## Validation results from this migration

- all 256 pages converted
- 273 images stored locally
- no conversion errors reported
- 24 broken wikilinks found, representing 20 unique targets
- 4 case/separator mismatches repaired
- 16 missing but useful topic targets represented by new stubs

“Zero conversion errors” does not mean perfect semantic conversion; visual and link review remained necessary.

## Reusable lessons

- Export early and preserve the raw data privately.
- Separate extraction from conversion so either half can be repeated.
- Build the full identifier map before rewriting links.
- Treat tables as structured subdocuments.
- Download media locally.
- Pilot on pathological examples, not easy ones.
- Make batches resumable and idempotent.
- Preserve provenance.
- Never add PHI or private notebook content to a public repository.
