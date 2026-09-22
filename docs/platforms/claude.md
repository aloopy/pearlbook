# Claude setup

Claude Code and claude.ai can implement the PearlBook workflow with the same separation used elsewhere in this repository: the public framework stays in this repo, and the private vault stays on machines the clinician controls.

Use this adapter for one of three distinct paths: local Claude Code beside the vault, Remote Control steering that computer from a phone, or claude.ai calling narrow vault tools on a persistent private host. Do not assume that claude.ai can read a local vault merely because Claude Code can.

This adapter was verified against official Claude documentation on 2026-09-22 (first drafted 2026-08-24). Platform capabilities, plans, and defaults change; re-verify the linked documentation before relying on plan- or version-specific details.

## Option 1: local Claude Code

Run Claude Code — [CLI, desktop app, IDE extension, or web-connected local session](https://code.claude.com/docs/en/how-claude-code-works.md) — on the computer that holds the Obsidian vault. As with Codex, the simplest mental model is that the private vault folder and the Claude Code working directory are the same folder. The public PearlBook repository remains separate.

Scoping behavior to rely on:

- Claude Code operates within the working directory and its subdirectories by default; parent directories require explicit permission ([permissions](https://code.claude.com/docs/en/permissions.md)).
- A dedicated workspace outside the vault can be added with `--add-dir` rather than widening access to the home directory.
- Keep the default ask-before-acting permission mode for vault edits until the preview-and-review habit is established. Broad auto-approval modes trade review for speed and are not recommended for a clinical vault.
- On macOS, Linux, and WSL2, the optional [bash sandbox](https://code.claude.com/docs/en/sandboxing.md) can further restrict filesystem and network reach. Native Windows is not supported; run Claude Code inside WSL2 there.

### Shared instructions: one `AGENTS.md`

Keep the PearlBook rules in **one `AGENTS.md` at the vault root**, shared by Claude Code, Codex, and OpenClaw. The guided setup script creates a starter version; it carries vault-first retrieval, search-before-create, source-before-synthesis, explicit-approval edits, and the [safety boundaries](../../skills/codex/pearlbook/SKILL.md#safety-boundaries) from the shared skill.

How Claude Code loads it ([AGENTS.md in the memory docs](https://code.claude.com/docs/en/memory#agents-md)):

- Claude Code v2.1.277 and later reads `AGENTS.md` directly, **but only when there is no `CLAUDE.md`, `.claude/CLAUDE.md`, or `CLAUDE.local.md`** in the working directory or above it. Your personal `~/.claude/CLAUDE.md` does not count and still loads alongside it.
- In sessions that cannot read `AGENTS.md` directly — Amazon Bedrock or other third-party providers, telemetry disabled, versions before v2.1.277, or the first session after an upgrade — add an optional `CLAUDE.md` next to it that contains only:

  ```markdown
  @AGENTS.md
  ```

  The import never loads the file twice, so it is safe to keep everywhere.
- A `CLAUDE.local.md` counts as a `CLAUDE.md` and stops `AGENTS.md` from loading. If you keep one, either add `@AGENTS.md` to it or set **Project instructions** to `claude-md-and-agents-md` in `/config`.

Do not maintain separate, diverging rule files for each agent.

### Install the PearlBook skill

Claude Code does **not** read Codex's `.agents/skills` folders. Copy or symlink the skill folder into a Claude Code skills location ([skills](https://code.claude.com/docs/en/skills.md)):

```bash
# Personal: available in every Claude Code project on this computer
mkdir -p ~/.claude/skills
ln -s "/path/to/pearlbook-repo/skills/codex/pearlbook" ~/.claude/skills/pearlbook

# Or project-only: inside the vault
mkdir -p "/path/to/vault/.claude/skills"
cp -R "/path/to/pearlbook-repo/skills/codex/pearlbook" "/path/to/vault/.claude/skills/pearlbook"
```

The skill's `name` and `description` frontmatter works unchanged. The Codex-only `agents/openai.yaml` is ignored. Run `setup_pearlbook.py` from the installed copy so its `references/local-config.md` stays local and out of the public repository.

**claude.ai, Claude Desktop, and Cowork** use skills uploaded to your claude.ai account rather than local folders. Create a ZIP whose top level is the `pearlbook` folder — leaving out any `references/local-config.md`, which holds your private vault path — upload it, and enable it in **Customize > Skills**. Uploaded skills accept only these frontmatter fields: `name`, `description`, `license`, `compatibility`, `metadata`, and `allowed-tools`. An uploaded skill cannot reach a vault on your computer; pair it with a private MCP connector (Option 3) or use Claude Code locally.

### Optional: PearlBook MCP tools in Claude Code

Claude Code can read local vault files directly, so MCP is optional locally. To test or use the same bounded tools the headless host exposes, register the bundled stdio server with a Python environment that has `mcp` installed ([MCP](https://code.claude.com/docs/en/mcp)):

```bash
python3 -m venv ~/.pearlbook-runtime
~/.pearlbook-runtime/bin/pip install -r /path/to/pearlbook/scripts/requirements-mcp.txt
claude mcp add pearlbook -- ~/.pearlbook-runtime/bin/python \
  /path/to/pearlbook/scripts/pearlbook_mcp.py --vault "/path/to/vault" --vault-name "PearlBook"
```

The server also accepts `--link-style {obsidian,https_bridge,path}` and `--link-base`. Run `claude mcp get pearlbook` to confirm the connection.

Chat renderers may not make `obsidian://` links clickable. The default is still a native Obsidian link plus the vault-relative path; an HTTPS bridge is an opt-in described in [Obsidian setup](../obsidian-setup.md#5-attachments-and-links).

## Option 2: steer the computer from a phone (Remote Control)

[Remote Control](https://code.claude.com/docs/en/remote-control.md) lets the user start and steer a local Claude Code session from the Claude mobile app or claude.ai/code in a browser. Execution stays on the connected computer: the vault, permissions, MCP servers, and any authenticated browser remain local, and the phone is only a steering surface. The computer must remain awake and online.

Two properties matter for PearlBook:

- While Remote Control is connected, the session transcript — your messages, Claude's responses, and tool activity, which can include note text — is stored on Anthropic servers and retained under the [data usage](https://code.claude.com/docs/en/data-usage.md) policy. It is not deleted when the session ends. Avoid pasting patient details or secrets into the conversation regardless of surface.
- Remote Control is distinct from **cloud sessions** on claude.ai/code, which run in Anthropic-managed VMs. Treat a cloud session like any ephemeral cloud coding task: useful for developing this public framework, never a home for the private vault, licensed-site credentials, or browser state.

## Option 3: claude.ai with a private vault tool

For access when no personal computer is online, keep the synced vault on a persistent private host running Obsidian Headless, and expose only narrow PearlBook operations as an MCP server, as described in [Deployment options](../deployment-options.md#pattern-2-extra-computer-as-a-private-tool-host).

Claude-specific adapter details:

- claude.ai supports [custom connectors](https://claude.com/docs/connectors/custom/remote-mcp.md) that call a **remote** MCP server by URL, with OAuth (preferred) or beta request-header authentication. Plan availability differs between consumer and Team/Enterprise workspaces; check current documentation. Never choose **No sign-in** for a vault server.
- Anthropic offers [MCP tunnels](https://claude.com/docs/connectors/mcp-tunnels/overview.md) (outbound-only, no public endpoint), but as of September 2026 only as a research preview for Claude Enterprise organizations, on request. Individual Pro and Max users must still provide their own authenticated ingress (reverse proxy with OAuth, tunnel service, or network-level access) and must not expose an unauthenticated public endpoint in front of the vault.
- The [bundled PearlBook MCP server](../../skills/codex/pearlbook/scripts/pearlbook_mcp.py) speaks stdio. Reuse its tool contract — bounded search, exact-note read, hash-checked preview-and-apply writes, no delete/rename/shell/hidden folders — behind a streamable HTTP transport before presenting it as a custom connector.
- The server cannot tell whether a person approved a write. `pearlbook_apply_write` is annotated as destructive so Claude asks before each call; keep that prompt and do not choose "Always allow" for the write tool.

The tool-host boundaries are identical to the ChatGPT pattern: claude.ai is the agent, the host is only a tool server, the host's browser logins are not inherited, and public research is limited to what the claude.ai conversation surface provides.

## Optional authenticated reference browsing

When a user's field requires a licensed or institutional source, the [Claude in Chrome](https://code.claude.com/docs/en/chrome.md) extension can connect Claude Code to a Chrome (or other Chromium-based) browser and satisfy the shared authenticated-browser trust boundary.

**Use a dedicated browser profile, not your everyday browser.** Claude in Chrome shares the login state of the browser it is connected to, so it can reach any site that profile is signed into. A clinician's main browser is often signed into the EHR, hospital email, or banking. Create a separate Chrome profile, install the extension only there, and sign that profile into only the reference sites PearlBook needs.

- It reuses the sessions in that dedicated profile; the clinician signs in to the selected source normally.
- It navigates, reads rendered pages (including JavaScript applications), and reports what is visible.
- It pauses at login pages and CAPTCHAs and asks the human to handle them.
- Site-level permissions in the extension control which sites Claude may act on; grant only the reference sites the workflow needs.
- Optionally, [1Password for Claude](https://support.1password.com/1password-claude/) can fill a login without the password reaching Claude: each fill needs the user's approval on the Mac (for example Touch ID). It currently requires macOS, the Claude desktop app, and a paid plan.

Availability is plan- and platform-dependent (direct Anthropic paid plans, desktop Chromium browsers, no WSL or mobile). For public research, Claude Code's built-in web search and fetch tools work without a browser, but a generic fetch of a licensed JavaScript application may return only a shell — that indicates the browser path is needed, not that access failed.

CorePendium is one emergency-medicine example of this optional pattern; follow the [CorePendium workflow](../../workflows/corependium-browser.md) and the source's own terms. Claude and PearlBook do not require it.

## Data and privacy notes

- Consumer Claude accounts (Free, Pro, Max) let you choose whether your chats are used for model training; with it on, data is retained for up to 5 years, otherwise 30 days. Review [data usage](https://code.claude.com/docs/en/data-usage.md) and the account's privacy settings before routing clinical learning conversations through it. Commercial plans do not train on user content by default.
- Feedback commands (`/feedback`, `/bug`, `/share`) can upload the session transcript to Anthropic. Do not submit feedback from sessions containing sensitive material.
- Local session transcripts are stored in plaintext under `~/.claude/projects/` (30 days by default); the host checklist in [SECURITY.md](../../SECURITY.md) (dedicated account, full-disk encryption) covers them.

## Capability map

| Need | Recommended Claude path |
|---|---|
| Work directly with a local vault | Claude Code with the vault as the working directory and a root `AGENTS.md` |
| Message from a phone while a computer is online | Remote Control steering the local session |
| Access when the personal computer is offline | claude.ai plus persistent private host and a narrow, authenticated remote-MCP connector |
| Read licensed references | Claude in Chrome over a dedicated, clinician-authenticated browser profile |
| Improve the public framework | Cloud session or local checkout of this repository |

## Recovery behavior

Unchanged from the core contract: if the vault, the private tool, or an authenticated reference session is unavailable on any of these surfaces, the agent must say the vault or source was not consulted and must never silently substitute model memory for private knowledge.
