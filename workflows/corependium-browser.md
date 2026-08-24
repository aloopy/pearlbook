# CorePendium browser workflow

CorePendium is a licensed, JavaScript-rendered reference. Public web fetches may see only an application shell. Pearlbook therefore uses a browser profile that the clinician authenticates manually.

This guide describes behavior, not a fixed OpenClaw release or command syntax.

## Trust boundary

The clinician:

- opens the browser profile
- enters credentials
- completes MFA, CAPTCHA, or account confirmation
- decides which subscription account may be used

The agent:

- reuses the authenticated local session
- navigates and reads rendered pages
- records URLs and concise clinical synthesis
- stops when manual authentication is required

Never place credentials, cookies, storage state, browser-profile archives, screenshots of account data, or copied subscription content in Git.

## Required browser capabilities

The platform adapter should provide:

- status and profile discovery
- tab listing/opening/closing
- stable tab handles or labels
- accessibility/DOM snapshots of rendered content
- narrow click/type/navigation actions
- optional page evaluation for data already available to the authenticated page
- visible blocker reporting

## Operating loop

### 1. Inspect state

Check browser availability, then list profiles and tabs. Reuse an existing CorePendium tab when possible. Use a stable label or handle rather than a numeric tab position.

### 2. Confirm authentication visibly

Inspect the rendered page. A chapter index, account-aware navigation, or readable chapter content supports that the session is authenticated. A JavaScript shell returned by a generic fetch does **not** prove that browser access failed.

If login, MFA, CAPTCHA, or permission is visible, stop and ask the clinician to complete that exact step.

### 3. Search and navigate

Prefer:

1. direct known chapter URL
2. CorePendium's own search
3. specialty/index navigation
4. public search to locate the canonical chapter URL

Read the page before acting. Prefer durable accessible labels and URLs over coordinates or brittle CSS selectors.

### 4. Extract only what the workflow needs

Capture the direct URL, title, clinically relevant facts, and associated media links needed for the task. Summarize in original language. Do not bulk-export the reference or persist its full text.

### 5. Recover safely

After navigation, modal changes, or search submission, inspect the page again before the next action.

If a control reference becomes stale:

1. inspect the same tab again
2. locate the current visible control
3. retry once
4. report a blocker rather than looping

If retries created duplicate tabs, close the extras.

## Capability-oriented example

```text
browser.status()
profile = browser.choose_profile(requires_existing_login=true)
tab = browser.reuse_or_open(label="corependium", profile=profile)
page = browser.inspect(tab)

if page.requires_manual_auth:
    handoff_to_clinician(page.blocker)
    stop

result = browser.navigate_or_search(tab, clinical_topic)
chapter = browser.inspect(tab)
return summarize(chapter) + chapter.canonical_url
```

Concrete adapters may call these operations `status`, `profiles`, `tabs`, `open`, `snapshot`, or `act`; names will change while the invariants remain stable.

## Verification checklist

- correct browser profile
- correct tab after navigation
- logged-in rendered chapter, not a public shell
- main chapter link captured
- relevant media links captured
- no copied session material
- no paywalled text committed
- manual authentication blockers reported precisely
