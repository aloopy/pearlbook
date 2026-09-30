# Security and clinical safety

## Never commit

- patient identifiers or reconstructable clinical narratives
- credentials, tokens, cookies, browser storage, or browser-profile archives
- MFA seeds or recovery codes
- raw private chat/session exports
- a personal vault unless each file is intentionally approved for publication
- copied chapters, screenshots, transcripts, or bulk-derived content from licensed references
- private source exports, including raw Notion, Evernote, Apple Notes, or Glass migration data

Use synthetic or thoroughly de-identified examples. “Removing the name” is not sufficient de-identification when dates, locations, images, or rare events remain identifying.

## Authenticated browser rules

1. Use a dedicated browser profile signed into only the reference sites PearlBook needs, never the everyday browser that holds EHR, email, or banking sessions.
2. The user enters credentials and completes MFA. A user-approved password-manager fill or platform private sign-in form is acceptable only when credentials go directly to the intended service without reaching the agent or chat. The user handles verification and medical/legal terms acceptance.
3. The agent may reuse that session to open the specific pages the user's question needs.
4. The agent must not export or serialize authentication state into the repository.
5. A login blocker causes a human handoff, not credential-guessing or bypass.
6. Collect only the minimum page information needed for the current task. No crawling, bulk download, or mirroring.
7. Respect subscriptions, licenses, terms, and robots/access controls.

## Credential boundaries

| Runtime | Allowed | Never provide |
|---|---|---|
| Local computer | User-authenticated browser profile; local OS protections | Password text, MFA seed, recovery code, exported cookies |
| Private headless host | Scoped machine tokens required by the sync or narrow tool | Human website passwords or unrestricted home-directory access |
| Dot cloud computer | Authorized private vault replica; user-authenticated source session; optional user-approved managed login | Passwords exposed to the agent/chat, copied authentication state, PHI |
| Cloud coding environment | Minimum scoped machine credential for public-repository development | Personal vault, licensed-site credentials, browser state, human passwords |
| Private PearlBook tool | Tool-specific authentication and least-privilege vault path | General shell, arbitrary filesystem root, secret-store browsing |

Human credentials belong in the user's password manager and should be entered by the user into the intended service. A platform secret feature does not make a human password appropriate for agent use.

A managed browser login is separate from an active session, which can expire. Saved-login reuse may require user confirmation. Keep the dot cloud computer, the native terminal's Sync login, and Codex Cloud environment secrets separate; never repair access by dumping credentials or moving tokens between them. See the [ChatGPT setup](docs/platforms/codex-chatgpt.md#option-4-headless-obsidian-on-a-dot-cloud-computer).

## Private-host hardening

- Use a dedicated non-administrator account and full-disk encryption.
- Restrict file permissions to the approved vault and tool workspace.
- Keep the operating system, runtime, and dependencies patched.
- Prefer an outbound-only private connection; do not expose a public shell or file browser.
- Keep synchronization state on persistent storage and maintain an independent vault backup.
- Avoid logging note bodies, browser data, queries containing sensitive details, or tool responses by default.
- Test restore, session-expiry, tool-unavailable, and sync-conflict behavior.

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
- [ ] verify `.gitignore` covers vaults, browser state, local data, and secrets
- [ ] enable GitHub secret scanning and push protection when available
- [ ] require pull-request review for changes to security-sensitive adapters
- [ ] confirm the repository license still matches the intended use
- [ ] document vulnerability/contact handling

If sensitive data is committed, rotate affected credentials immediately and remove it from the full Git history; deleting the current file is not enough.

## Reporting

Report vulnerabilities privately through GitHub's private vulnerability reporting: open the repository's **Security** tab and choose **Report a vulnerability**. (The repository owner must first enable it in the repository's **Settings** security section (**Private vulnerability reporting > Enable**); if the button is missing, it has not been enabled yet.)

Use public GitHub issues only for non-sensitive concerns. Do not place secrets, PHI, or exploit details in a public issue.
