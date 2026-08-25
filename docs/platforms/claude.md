# Claude setup

Claude Code and claude.ai can implement the PearlBook workflow with the same separation used elsewhere in this repository: the public framework stays in this repo, and the private vault stays on machines the clinician controls.

This adapter was drafted and verified by a Claude agent against official Claude documentation on 2026-08-24. Platform capabilities, plans, and defaults change; re-verify the linked documentation before relying on plan- or version-specific details.

## Option 1: local Claude Code

Run Claude Code — [CLI, desktop app, IDE extension, or web-connected local session](https://code.claude.com/docs/en/how-claude-code-works.md) — on the computer that holds the Obsidian vault. As with Codex, the simplest mental model is that the private vault folder and the Claude Code working directory are the same folder. The public PearlBook repository remains separate.

Scoping behavior to rely on:

- Claude Code operates within the working directory and its subdirectories by default; parent directories require explicit permission ([permissions](https://code.claude.com/docs/en/permissions.md)).
- A dedicated workspace outside the vault can be added with `--add-dir` rather than widening access to the home directory.
- Keep the default ask-before-acting permission mode for vault edits until the preview-and-review habit is established. Broad auto-approval modes trade review for speed and are not recommended for a clinical vault.
- On macOS and Linux, the optional [bash sandbox](https://code.claude.com/docs/en/sandboxing.md) can further restrict filesystem and network reach.

### Behavioral contract

Encode the PearlBook contract where Claude Code loads it automatically:

- A `CLAUDE.md` at the vault root carries the standing rules: vault-first retrieval, search-before-create, source-before-synthesis, explicit-approval edits, and the [safety boundaries](../../skills/codex/pearlbook/SKILL.md#safety-boundaries) from the shared skill ([memory](https://code.claude.com/docs/en/memory.md)).
- Claude Code [Agent Skills](https://code.claude.com/docs/en/skills.md) live in `.claude/skills/` (project) or `~/.claude/skills/` (user) and use the same `SKILL.md` name-plus-description frontmatter as the Codex skill, so the [pearlbook skill](../../skills/codex/pearlbook/SKILL.md) contract ports with minimal adaptation. Keep any local configuration (authorized vault path, link style) out of the public repository, exactly as the Codex adapter does.

Chat renderers may suppress `obsidian://` links here too; the `obsid_net` HTTPS-bridge convention from [Obsidian setup](../obsidian-setup.md#5-attachments-and-links) applies unchanged.

## Option 2: steer the computer from a phone (Remote Control)

[Remote Control](https://code.claude.com/docs/en/remote-control.md) lets the user start and steer a local Claude Code session from the Claude mobile app or claude.ai/code in a browser. Execution stays on the connected computer: the vault, permissions, MCP servers, and any authenticated browser remain local, and the phone is only a steering surface. The computer must remain awake and online.

Two properties matter for PearlBook:

- While a session is connected, its transcript syncs through Anthropic servers so devices stay consistent, and is removed when the session ends. Avoid pasting patient details or secrets into the conversation regardless of surface.
- Remote Control is distinct from **cloud sessions** on claude.ai/code, which run in Anthropic-managed VMs. Treat a cloud session like any ephemeral cloud coding task: useful for developing this public framework, never a home for the private vault, licensed-site credentials, or browser state ([data usage](https://code.claude.com/docs/en/data-usage.md)).

## Option 3: claude.ai with a private vault tool

For access when no personal computer is online, keep the synced vault on a persistent private host running Obsidian Headless, and expose only narrow PearlBook operations as an MCP server, as described in [Deployment options](../deployment-options.md#pattern-2-extra-computer-as-a-private-tool-host).

Claude-specific adapter details:

- claude.ai supports [custom connectors](https://claude.com/docs/connectors/custom/remote-mcp.md) that call a **remote** MCP server by URL, on web and mobile, with OAuth 2.0 (preferred) or beta header-based authentication. Plan availability differs between consumer and Team/Enterprise workspaces; check current documentation.
- Anthropic does not provide an outbound tunnel comparable to OpenAI's Secure MCP Tunnel. The private host's MCP endpoint must be reachable from claude.ai, so the operator supplies their own authenticated ingress (reverse proxy, tunnel service, or network-level access) and must not expose an unauthenticated public endpoint in front of the vault.
- The [bundled PearlBook MCP server](../../skills/codex/pearlbook/scripts/pearlbook_mcp.py) speaks stdio. Reuse its tool contract — bounded search, exact-note read, hash-checked preview-and-confirm writes, no delete/rename/shell — behind a streamable HTTP transport before presenting it as a custom connector.

The tool-host boundaries are identical to the ChatGPT pattern: claude.ai is the agent, the host is only a tool server, the host's browser logins are not inherited, and public research is limited to what the claude.ai conversation surface provides.

## Authenticated reference browsing

The [Claude in Chrome](https://code.claude.com/docs/en/chrome.md) extension connects Claude Code to the clinician's real Chrome (or Chromium-based) browser, satisfying the [CorePendium browser workflow](../../workflows/corependium-browser.md) trust boundary directly:

- It reuses existing logged-in sessions; the clinician authenticates CorePendium normally in the browser.
- It navigates, reads rendered pages (including JavaScript applications), and reports what is visible.
- It will not enter credentials and pauses for the human at login pages and CAPTCHAs — the required handoff behavior, enforced by the platform.
- Site-level permissions control which sites Claude may act on; grant only the reference sites the workflow needs.

Availability is plan- and platform-dependent (paid plans, desktop Chrome, no WSL or mobile). For public research, Claude Code's built-in web search and fetch tools work without a browser, but a generic fetch of a licensed JavaScript application may return only a shell — that indicates the browser path is needed, not that access failed.

## Data and privacy notes

- Consumer claude.ai accounts have a training opt-in with longer retention when enabled; review [data usage](https://code.claude.com/docs/en/data-usage.md) and the account's privacy settings before routing clinical learning conversations through it. Commercial plans do not train on user content by default.
- Feedback commands can upload the session transcript to Anthropic. Do not submit feedback from sessions containing sensitive material.
- Local session transcripts are stored in plaintext under `~/.claude/`; the host checklist in [SECURITY.md](../../SECURITY.md) (dedicated account, full-disk encryption) covers them.

## Capability map

| Need | Recommended Claude path |
|---|---|
| Work directly with a local vault | Claude Code with the vault as the working directory |
| Message from a phone while a computer is online | Remote Control steering the local session |
| Access when the personal computer is offline | claude.ai plus persistent private host and a narrow remote-MCP connector |
| Read licensed references | Claude in Chrome over a clinician-authenticated browser |
| Improve the public framework | Cloud session or local checkout of this repository |

## Recovery behavior

Unchanged from the core contract: if the vault, the private tool, or an authenticated reference session is unavailable on any of these surfaces, the agent must say the vault or source was not consulted and must never silently substitute model memory for private knowledge.
