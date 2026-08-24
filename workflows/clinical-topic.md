# Clinical topic workflow

This workflow separates **answering** from **editing**. A question authorizes inspection and an evidence-backed reply; it does not automatically authorize broad vault rewrites.

## Default sequence

### 1. Search the vault

- Search titles and full text.
- Open the closest relevant note.
- Identify whether the requested point is already present, missing, or contradicted.
- Tell the clinician what exists when that context matters.

### 2. Read CorePendium before drafting

Open the most relevant main chapter in the authenticated browser. Do not add CorePendium as an after-the-fact citation; use it to shape the answer from the start.

Capture:

- the direct chapter URL
- relevant dose/threshold/procedure details
- links to useful associated EM:RAP media
- uncertainty or gaps that require another source

Do not copy or publish the chapter text.

### 3. Supplement appropriately

Use current public sources when:

- the topic has changed since the reference was published
- CorePendium lacks the needed detail
- primary literature or a society guideline is necessary
- the question is high-stakes or controversial

Prefer primary studies, society guidelines, regulatory information, and authoritative clinical references. Distinguish source statements from the agent's inference.

### 4. Answer at the intended altitude

Default clinical style:

- ED-focused
- concise and senior-resident useful
- action, dose, threshold, and pitfall oriented
- explicit about high-risk exceptions
- clear when local protocols or device labeling control

Avoid turning a narrow pearl into a textbook chapter.

### 5. Decide whether to edit

Edit when the clinician asks, when a standing local policy explicitly requests capture, or when confirming a small in-scope update is clearly part of the workflow. Otherwise, suggest the change.

When editing:

- preserve unrelated user content
- use the canonical note when one exists
- add the main CorePendium link near the top
- include relevant media links
- keep attachments local
- validate frontmatter, internal links, and note density

### 6. Return a direct note link

Every clinical-topic response should include the relevant exact note link, even when no edit occurred. Generate it from the vault-relative path; never expose the filesystem path in a public link.

## Pseudocode

```text
request = classify(user_message)
matches = vault.search(request.topic)
note = choose_canonical(matches)

core = browser.open_authenticated_reference(request.topic)
sources = [core]
if freshness_or_detail_gap(request, core):
    sources += public_research(request)

answer = synthesize(note, sources, clinical_context)

if request.authorizes_edit:
    changed_note = minimally_update(note, answer, sources)
    validate(changed_note)

return answer + exact_note_link(note)
```

## Failure modes

| Failure | Response |
|---|---|
| No matching note | Answer from sources and propose or create a focused page according to policy |
| Login expired | Ask the clinician to log in manually; resume afterward |
| CorePendium search weak | Navigate by specialty/index, then supplement with public sources |
| Conflicting guidance | Name the conflict, dates, population, and local-policy implications |
| No direct chapter | Link the most relevant search/index page and avoid claiming a direct match |
| High-risk uncertainty | Slow down, verify, and state the uncertainty |
| User asks for copyrighted text | Summarize and link; do not reproduce paywalled content |
