# Architecture

PearlBook is a pattern, not a dependency graph tied to one agent release.

## Core components

```text
Clinician
   |
   v
Conversation surface
   |
   v
Medical knowledge agent
   |-- local files or narrow tool ---> private Obsidian vault replica
   |-- authenticated browser --------> CorePendium / licensed references
   |-- public research --------------> primary and reputable sources
   `-- version control -------------> workflow docs and non-private tooling
```

The **vault is the durable clinical memory**. The agent's chat history, model context, and platform memory can improve continuity, but none should be the only copy of a clinical note. The public PearlBook repository contains the framework; the private vault remains outside it.

## Vault access patterns

1. **Direct local files:** the agent runs on a machine holding an authorized vault replica and receives access only to the vault and a dedicated workspace.
2. **Narrow private tool:** a persistent private host holds a synchronized vault replica and exposes only PearlBook search, read, and reviewable-edit operations to the conversation surface.

Do not use an ephemeral cloud coding task as the durable vault host. See [Deployment options](deployment-options.md).

## Capability contract

An implementation needs these capabilities:

| Capability | Required behavior |
|---|---|
| File discovery | Recursively find Markdown, Canvas, templates, and attachments |
| Content search | Search titles, aliases, tags, and note bodies quickly |
| Safe editing | Preserve unrelated content and produce inspectable diffs |
| Browser profiles | Reuse a clinician-authenticated local profile |
| Page inspection | Read rendered pages and links, including JavaScript applications |
| Narrow browser actions | Navigate, search, and open sources without scripting credentials |
| Public research | Find current primary/authoritative sources when licensed material is insufficient |
| Link generation | Return a clickable link to the exact vault note |
| Auditability | Record sources, note paths, and material changes |
| Human handoff | Stop for login, MFA, CAPTCHA, uncertainty, or unsafe external action |

Map these capabilities to the current platform's tools. Avoid making the workflow depend on command names, tab indices, generated element IDs, or one model provider.

## Information boundaries

### Safe to version publicly

- Folder conventions and templates
- Sanitized example notes
- Workflow pseudocode
- Validation scripts
- Source-linking conventions
- Browser recovery logic without credentials

### Keep local or private

- The actual personal vault unless intentionally published
- Patient information
- Cookies, browser profiles, tokens, passwords, MFA recovery codes
- Full text, screenshots, or derived bulk copies of licensed references
- Private chat/session exports

## Main clinical flow

1. Classify the request: answer only, update an existing note, create a note, or build a visual.
2. Search the vault and inspect the closest relevant note.
3. Open the relevant CorePendium chapter in the authenticated browser and read it before drafting.
4. Supplement with current primary or authoritative public sources when needed.
5. Produce an ED-focused answer.
6. Edit the vault only when requested or when the configured workflow explicitly permits it.
7. Validate links and attachments.
8. Return the answer plus a clickable link to the exact note.

## Portability strategy

Keep two layers separate:

- **Workflow layer:** invariants such as “vault before web,” “human login,” and “confirm sources before editing.”
- **Adapter layer:** current commands or APIs that implement search, browser snapshots, file edits, and messaging.

When a platform changes, update only the adapter notes. The clinical workflow and vault remain stable.
