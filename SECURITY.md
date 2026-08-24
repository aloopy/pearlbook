# Security and clinical safety

## Never commit

- patient identifiers or reconstructable clinical narratives
- credentials, tokens, cookies, browser storage, or browser-profile archives
- MFA seeds or recovery codes
- raw private chat/session exports
- a personal vault unless each file is intentionally approved for publication
- copied chapters, screenshots, transcripts, or bulk-derived content from licensed references
- private source exports such as the raw Glass notebook JSON

Use synthetic or thoroughly de-identified examples. “Removing the name” is not sufficient de-identification when dates, locations, images, or rare events remain identifying.

## Authenticated browser rules

1. The user enters credentials and completes MFA.
2. The agent may reuse that local session for authorized research.
3. The agent must not export or serialize authentication state into the repository.
4. A login blocker causes a human handoff, not credential-guessing or bypass.
5. Collect only the minimum page information needed for the current task.
6. Respect subscriptions, licenses, terms, and robots/access controls.

## Medical content rules

- Treat the system as educational knowledge management, not autonomous clinical decision-making.
- Identify local protocols, device labeling, and institutional policy where they control.
- Verify time-sensitive or high-risk claims with current authoritative sources.
- Include enough context to prevent a dose, threshold, or contraindication from being dangerously detached.
- Preserve uncertainty and disagreement between sources.
- Require clinician review before publication or patient-care use.

## Repository review before public release

- [ ] scan git history, not just the current tree
- [ ] run a secret scanner
- [ ] search for names, MRNs, dates of birth, addresses, phone numbers, and emails
- [ ] inspect images and document metadata
- [ ] confirm examples are synthetic or approved
- [ ] verify licensed text is summarized rather than reproduced
- [ ] confirm external links do not contain account or session parameters
- [ ] choose a license
- [ ] document vulnerability/contact handling

If sensitive data is committed, rotate affected credentials immediately and remove it from the full Git history; deleting the current file is not enough.

## Reporting

Until a private reporting channel is listed, open a GitHub issue only for non-sensitive concerns. Do not place secrets, PHI, or exploit details in a public issue.
