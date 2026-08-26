# Clinical topic workflow

This workflow separates **answering** from **editing**. A question authorizes inspection and an evidence-backed reply; it does not automatically authorize broad vault rewrites.

## Default sequence

### 1. Search the vault

- Search titles and full text.
- Open the closest relevant note.
- Identify whether the requested point is already present, missing, or contradicted.
- Tell the clinician what exists when that context matters.

### 2. Select and read the relevant sources

Use the user's configured source policy. Depending on the question, that may include:

- an institutional pathway or local protocol;
- a society guideline, regulatory source, or primary study;
- a licensed specialty reference through a user-authenticated browser; or
- no external source when the task is only to retrieve or reorganize existing vault content.

Read material sources before drafting rather than adding citations to an answer written from model memory. CorePendium is one optional licensed-reference example for emergency-medicine users; it is not required by PearlBook.

Capture:

- the direct source URL or stable identifier
- relevant dose/threshold/procedure details
- links to useful associated media or institutional material
- uncertainty or gaps that require another source

Do not copy or publish licensed source text.

### 3. Supplement appropriately

Use current public sources when:

- the topic has changed since the reference was published
- the configured reference lacks the needed detail
- primary literature or a society guideline is necessary
- the question is high-stakes or controversial

Prefer primary studies, society guidelines, regulatory information, and authoritative clinical references. Distinguish source statements from the agent's inference.

### 4. Answer at the intended altitude

Default clinical style:

- matched to the clinician's specialty and level of training
- concise and useful at the point of learning or care
- action, dose, threshold, and pitfall oriented
- explicit about high-risk exceptions
- clear when local protocols or device labeling control

Emergency-medicine users may choose an ED-focused, senior-resident style. Avoid turning a narrow pearl into a textbook chapter unless the user asks for a comprehensive review.

### 5. Decide whether to edit

Edit when the clinician asks, when a standing local policy explicitly requests capture, or when confirming a small in-scope update is clearly part of the workflow. Otherwise, suggest the change.

When editing:

- preserve unrelated user content
- use the canonical note when one exists
- add the most relevant source link where it is easy to find
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

sources = select_configured_sources(request, note, user_policy)
if freshness_or_detail_gap(request, sources):
    sources += current_authoritative_research(request)

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
| Optional licensed-source search weak | Navigate by specialty/index, then supplement with current authoritative sources |
| Conflicting guidance | Name the conflict, dates, population, and local-policy implications |
| No direct chapter | Link the most relevant search/index page and avoid claiming a direct match |
| High-risk uncertainty | Slow down, verify, and state the uncertainty |
| User asks for copyrighted text | Summarize and link; do not reproduce paywalled content |

## Optional emergency-medicine example

An emergency-medicine user may configure CorePendium as a preferred specialty reference and follow the [CorePendium browser workflow](corependium-browser.md). Another clinician might instead configure a different licensed reference, institutional guideline library, or no authenticated browser source at all. The search, synthesis, review, and edit invariants stay the same.
