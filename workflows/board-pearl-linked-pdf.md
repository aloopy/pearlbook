# Board pearl → teaching graphic → linked PDF

Use this workflow when a user asks to process a board pearl: a photo of a teaching board, diagram, or similar educational sketch. Produce a faithful teaching graphic with ChatGPT's image-generation tool, then package it in a PDF with real clickable references. This is a per-request workflow, not automatic ingestion of every incoming image. Notebook storage is a separate, optional authorized step.

The content, source, and review rules are portable. This version specifically requires an image-generation tool that accepts the original image as a reference, plus PDF tooling that can add and inspect hyperlink annotations and render pages. Check actual tool availability before starting; a prompt alone does not generate an image or export a PDF. Use existing image and PDF tools rather than building a new ingestion service.

Follow [Security and clinical safety](../SECURITY.md) and the [clinical topic workflow](clinical-topic.md) for source access and any notebook edits. Outputs require clinician review before publication or patient-care use; they support clinical learning, not autonomous clinical decisions. Use no patient data in public examples and do not reproduce or archive bulk licensed source content.

## Run the workflow

### 1. Read the original as the content and design brief

Preserve the original board photo unchanged in the authorized private workspace, provided it is appropriate to retain and contains no patient information. Record its provenance and, when working with files, its SHA-256. Keep original and derived artifacts distinguishable; never overwrite the original with a cleaned-up version.

Before generating, inventory all substantive teaching points, numbers, units, labels, diagrams, arrows, comparisons, table rows (including supplemental data), and relationships. Preserve groupings and the meaning of spatial relationships even when improving the layout. The goal is a clearer version of this board, not a generic infographic about its topic.

Ask a narrow question about unreadable text, ambiguous arrows, or missing context. Do not guess, silently omit unresolved points, or present an incomplete reconstruction as finished. Keep an unresolved item in the review inventory until the user resolves it or explicitly accepts a stated limitation.

### 2. Verify the teaching content

Use the user's preferred trusted sources and consult current primary papers, guidelines, and their supplements or tables for specific numerical claims. Read the relevant source passages before assigning references. Follow the user's authenticated access and source-use rules; summarize and link rather than copying licensed text.

Maintain a compact working map of board item → supporting source and locator → verified value or unresolved discrepancy. Distinguish local protocol, teaching point, and general evidence; a difference from a published guideline is not by itself proof that a local protocol is an error. Preserve populations, time frames, units, denominators, and qualifiers needed to interpret numbers.

Correct confirmed errors in the derived graphic. Explain material corrections with supporting links in the accompanying note, outside the graphic. For conflicts or inaccessible evidence, identify the precise limitation and request only the missing information needed. Never describe an unavailable source as checked.

### 3. Generate and inspect the graphic

Supply the **actual original board image** as an image-generation reference, along with the verified content inventory and specific design instructions. A text description alone is insufficient. If the reference cannot be passed to the tool, report that blocker before generating a purported reconstruction.

Use plain, clean typography, restrained color, and whitespace. No Comic Sans, decorative filler, invented slogans, unnecessary subtitles, generic takeaways, correction banners, or meta-copy such as “source-checked whiteboard pearl” or “keep the source trail.” Make the original teaching structure legible without adding unrelated material.

For quantitative diagrams, preserve verified values, axis scales, direction, labels, and confidence-interval endpoints. A precisely plotted supporting reference can help communicate geometry to the image tool; include it alongside the original board, and still use the actual image-generation tool for the final teaching graphic. Do not substitute a hand-built PDF or plot for the requested image-generated graphic.

Inspect the high-resolution output against both the board inventory and the verified sources, label by label, number by number, row by row, and diagram by diagram. Check arrows, associations, axes, and interval endpoints as carefully as text. Repair errors or omissions through image editing/regeneration, then inspect the entire result again for regressions. If fidelity cannot be achieved, state what remains wrong and do not label the graphic verified.

### 4. Add real PDF links

Place the final high-resolution image in a PDF without stretching, cropping, or downsampling it into illegibility. Choose page dimensions and orientation that keep the teaching content readable. Reserve a small reference area outside the graphic, or use clearly mapped reference labels without obscuring teaching content.

Add compact, readable labels with a visible **↗** icon, such as `Guideline ↗`, `Study, Table 2 ↗`, or `Supplement, Table S1 ↗`. These are formatting examples, not citations. Map each label to the actual relevant claim, diagram, or table and use a direct, verified paper, guideline, supplement, or table URL. Avoid substituting a search-results page or journal homepage for a precise reference. Keep visual clutter low and remove account/session parameters from links.

Use PDF tooling to create a real hyperlink annotation covering **both the reference label and its icon**. Rasterized text, a drawn URL, or a drawn ↗ is not clickable by itself. If a source table has no stable direct anchor, link to its verified parent paper or supplement and name the exact table in the label; do not invent a fragment identifier.

### 5. Verify and deliver

Render every PDF page and inspect legibility at normal reading size, clipping, alignment, and the reference area. Inspect the PDF's link annotations: verify the destination URI and that each clickable rectangle covers the intended visible label/icon after page scaling, stays within the page, and does not cover an unrelated item. Open each reference from the PDF in a link-capable viewer and confirm the intended destination; a paywall may still require the reader's own access. If a viewer or target is unavailable, report which check remains incomplete.

Deliver the high-resolution image and the linked PDF with clear file links, and preserve the original photo. Keep accompanying prose brief: material corrections and any unresolved limitations. Do not claim generation, export, rendering, link verification, or source review that did not actually succeed. If a required tool is unavailable, name the exact blocked step and retain completed work so it can resume.

## Optional notebook capture

Only store or update notebook content when the user requests it or standing rules explicitly authorize it. Permission to process an image does not authorize notebook writes, public sharing, or a background job.

1. Read the destination's existing rules and verify authorized access. Follow its existing sync procedure **before** reading and editing; stop on incomplete sync or conflicts. Search for and read the canonical note before creating a duplicate.
2. Preview the smallest useful update and follow the destination's approval requirements. Link the sources, original board, derived image, and linked PDF from that note. Record provenance and material corrections without copying licensed reference text. Preserve unrelated note content and retain an independent backup according to existing rules.
3. Verify the original image remains unchanged, the note diff is correct, and all attachment and source links resolve. Follow the existing sync procedure **after** writing, inspect any merged content, and report the observed sync result. Do not infer arrival on another device without checking it.
4. Return a clickable link to the exact note plus a notebook-relative path or native identifier fallback. For Obsidian, respect the configured [note-link policy](../skills/codex/pearlbook/SKILL.md#present-vault-notes-in-chat); do not silently enable a third-party HTTPS bridge. If the configured link cannot be clicked in this chat surface, say so and give the path rather than claim it works.

For an already configured Obsidian cloud replica, reuse the adapter's [authorized update and sync sequence](../docs/platforms/codex-chatgpt.md#6-make-and-verify-one-authorized-update). Other notebooks can apply the same provenance and review rules only after their retrieval, attachment, edit, backup/version, and link capabilities are established; see [notebook adaptation guidance](../docs/platforms/codex-chatgpt.md#apply-the-workflow-to-notion-and-other-notebooks). This workflow does not establish or test those integrations, install sync, or guarantee durable background synchronization. With missing or read-only access, deliver the artifacts and a proposed note update instead of claiming storage succeeded.

## Paste-ready prompt

Attach the board image and replace the bracketed source preference. Notebook capture is off unless separately requested or explicitly authorized by standing rules.

```text
Process this board pearl into a faithful teaching graphic and a linked PDF.
Preferred trusted sources: [my configured sources, or specify sources here].

Treat the original board as the content and design brief. Preserve ALL substantive
teaching points, numbers, units, labels, diagrams, arrows, comparisons, table rows
(including supplemental data), and relationships. Improve legibility and layout
without replacing it with a generic infographic. Preserve the original photo.

Check clinical content against my preferred trusted sources and primary papers,
guidelines, supplements, and tables for specific claims. Distinguish local protocol,
teaching points, and general evidence. Correct confirmed errors; explain material
corrections outside the graphic with sources. Ask narrowly about unreadable or
unresolved content; do not guess or silently omit it. Do not reproduce bulk licensed
content or include patient data. The output needs clinician review.

Use ChatGPT's actual image-generation tool and pass the original board image as an
actual reference. Use plain clean typography, restrained color, and whitespace.
No Comic Sans, decorative filler, invented slogans, unnecessary subtitles, generic
takeaways, correction banners, or meta-copy such as "source-checked whiteboard
pearl" or "keep the source trail." Preserve verified quantitative diagram values,
scales, direction, labels, and confidence-interval endpoints. An accurate supporting
reference plot may help, but use image generation for the final teaching graphic.
Inspect every label, number, table row, arrow, relationship, and diagram against the
original and sources; repair omissions/errors and recheck the whole image.

Place the high-resolution final image in a PDF. Add compact readable reference
labels with visible ↗ icons and REAL PDF hyperlink annotations covering each label
and icon. Use verified direct paper/guideline/supplement/table URLs and exact table
labels when no stable table anchor exists. Drawn URLs are not clickable. Keep links
and references unobtrusive without shrinking teaching content into illegibility.
Render and inspect all PDF pages for legibility/clipping. Inspect annotation targets
and clickable areas, and open each link to verify its intended destination.

Deliver the image and linked PDF, preserve the original, and keep the accompanying
note to material corrections and unresolved limitations. State exact blockers if
any source or tool is unavailable; never claim work or verification that did not run.

Only if notebook capture is separately requested or explicitly authorized: follow
the destination's rules and sync checks before/after editing; search/read the
canonical note, follow its preview/approval requirements, preserve unrelated text,
and link sources plus original/derived artifacts. Verify attachments, return the
exact clickable note link with a path/identifier fallback, and report any link or
sync limitations. Do not imply automatic ingestion, tested notebook integrations,
or guaranteed durable background sync.
```

## Run/review checklist

- [ ] Original retained; complete content/relationship inventory; ambiguities resolved or explicitly accepted and disclosed.
- [ ] Sources read; numbers checked against relevant primary material and supplements; material corrections documented outside the graphic.
- [ ] Actual board supplied to image generation; final graphic inspected and repaired, including every row, arrow, scale, and interval endpoint.
- [ ] High-resolution image and PDF legible; all pages rendered; no clipped content or decorative/meta-copy additions.
- [ ] Every reference has a visible ↗ and real annotation over its label/icon; targets and clickable areas verified; incomplete checks disclosed.
- [ ] Image and PDF delivered; original preserved; clinician review required; optional notebook writes authorized, verified, and linked with observed sync status.
