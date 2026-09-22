# CorePendium browser workflow

This is an **optional emergency-medicine example**, not a PearlBook dependency. [CorePendium](https://www.emrap.org/corependium/) is EM:RAP's subscription reference, and a paid account is the way to read it. The same pattern works for any other licensed or institutional source.

## The idea in one sentence

The agent reads CorePendium the way you would — with your own logged-in account, one page at a time, when you ask a question — so you get to the answer faster at the point of care, with a link back to the page.

It is a faster way for a subscriber to look something up. It is not a way to copy, collect, or redistribute EM:RAP's work.

## What this looks like

- **Your account.** You use your own paid CorePendium subscription and log in yourself, in a dedicated browser profile that is signed into only the reference sites you use with PearlBook (not your everyday browser with EHR or email sessions).
- **One question, one page.** The agent opens the specific chapter or section your question needs, reads it, and answers — just as you would if you clicked through yourself.
- **Personal, point-of-care use.** The answer is for you. It includes a direct link back to the CorePendium page so you can read the source and EM:RAP gets the visit.
- **Your own notes.** In your vault, save your own short summary, the key pearl in your words, and the link. Do not paste CorePendium text into notes, especially notes you share or publish.

## What this is not

- No crawling, spidering, or following links through the site to gather content.
- No bulk downloading, mirroring, exporting, or building a copied database or corpus.
- No sharing your login or letting the agent serve anyone but you.
- No getting around logins, paywalls, CAPTCHAs, or other access controls.

Please read and follow [EM:RAP's Terms of Use](https://www.emrap.org/terms). They set the rules for your subscription, and they take precedence over anything in this guide. If you are unsure whether a use fits, ask EM:RAP.

## Roles

You:

- open the dedicated browser profile and log in (a password-manager fill that you approve on your own device is fine);
- complete MFA, CAPTCHA, or account confirmation;
- ask the question that decides which page is opened.

The agent:

- reuses your logged-in session in that profile;
- opens and reads the page that answers your question;
- records the URL and writes a short answer in its own words;
- stops and asks you when login or confirmation is needed.

Never place credentials, cookies, storage state, browser-profile archives, screenshots of account data, or copied subscription content in Git or in the vault.

## Browser capabilities the adapter needs

- status and profile discovery
- tab listing, opening, and closing
- stable tab handles or labels
- accessibility or DOM snapshots of the rendered page the user is reading
- narrow click, type, and navigation actions
- visible blocker reporting

## Operating loop

### 1. Inspect state

Check that the browser is available and that the dedicated profile is in use. Reuse an existing CorePendium tab when possible. Use a stable label or handle rather than a numeric tab position.

### 2. Confirm you are signed in

Look at the rendered page. A chapter index, account-aware navigation, or readable chapter content means the session is signed in. A JavaScript shell returned by a generic web fetch does **not** mean browser access failed; it only means the page needs the browser.

If a login, MFA, CAPTCHA, or permission prompt is visible, stop and ask the user to complete that step.

### 3. Find the page for this question

Prefer, in order:

1. a direct chapter URL already linked from the user's vault note;
2. CorePendium's own search;
3. the specialty or index navigation;
4. a public web search to find the right chapter URL.

Open only what the question needs. Read the page before acting. Prefer accessible labels and URLs over coordinates or brittle CSS selectors.

### 4. Answer and link back

Capture the page URL and title, and answer the question in your own words with the clinically relevant points. Include the link so the user can read the full section. Summaries, not transcripts.

### 5. Recover safely

After navigation, a modal, or a search, inspect the page again before the next action.

If a control reference becomes stale:

1. inspect the same tab again;
2. locate the current visible control;
3. retry once;
4. report a blocker rather than looping.

If retries opened duplicate tabs, close the extras.

## Capability-oriented example

```text
browser.status()
profile = browser.choose_profile(dedicated_reference_profile=true, requires_existing_login=true)
tab = browser.reuse_or_open(label="corependium", profile=profile)
page = browser.inspect(tab)

if page.requires_manual_auth:
    handoff_to_user(page.blocker)
    stop

browser.open_page_for_question(tab, user_question)   # one page, not a crawl
chapter = browser.inspect(tab)
return answer_in_own_words(chapter, user_question) + chapter.canonical_url
```

Concrete adapters may call these operations `status`, `profiles`, `tabs`, `open`, `snapshot`, or `act`; names will change while the pattern stays the same.

## Verification checklist

- dedicated browser profile, signed into only the needed sources
- correct tab after navigation
- signed-in rendered chapter, not a public shell
- only the page(s) needed for this question were opened
- chapter link included in the answer
- answer and vault note are in the user's own words
- no session material or CorePendium text saved to the vault or Git
- manual authentication blockers reported precisely
