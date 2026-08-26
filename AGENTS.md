# AGENTS.md

## Purpose

Help maintain a release-agnostic, clinician-owned blueprint for a medical knowledge agent. Optimize for portability, safety, inspectability, and practical clinical learning.

## Read first

1. `README.md`
2. `docs/architecture.md`
3. `SECURITY.md`
4. `docs/deployment-options.md` when changing access or hosting behavior
5. `docs/platforms/README.md` when selecting or comparing agent surfaces
6. only the platform adapter and workflow file relevant to the task

## Contribution rules

- Describe durable capabilities and invariants before platform-specific commands.
- Confirm the user's chosen platform and host pattern before applying adapter-specific setup.
- Treat CorePendium, Glass Health, LangostaMD, and emergency-medicine taxonomy as optional examples unless the user explicitly selects them.
- Put exact OpenClaw or vendor commands in clearly labeled adapter examples.
- Do not commit PHI, secrets, authentication state, private vault content, or paywalled reference text.
- Use synthetic or sanitized examples.
- Preserve attribution and provenance.
- Prefer concise Markdown that renders well in GitHub and Obsidian.
- When documenting clinical workflows, require authoritative source review and clinician oversight.
- Do not imply that an agent replaces medical judgment.
- Never automate credential entry, MFA bypass, CAPTCHA bypass, or subscription circumvention.
- Keep browser extraction narrow and task-specific.
- Treat historical internal APIs as unstable observations, not supported integrations.
- Do not put a personal vault, human account password, MFA secret, cookie archive, or licensed content in a repository secret or cloud-task environment.
- Do not treat an ephemeral coding task as the durable vault host.
- `docs/platforms/claude.md` was verified against official Claude documentation on 2026-08-24; re-verify platform claims against current official documentation before materially changing them.
- `docs/platforms/codex-chatgpt.md` was verified against official OpenAI documentation on 2026-08-26; re-verify platform claims before materially changing them.

## Change workflow

1. Inspect existing documentation before creating a new page.
2. Search briefly for an existing maintained solution before proposing custom tooling.
3. Make focused changes on a branch.
4. Check internal links and examples.
5. Review the diff for secrets, PHI, and licensed content.
6. Summarize assumptions and portability tradeoffs in the pull request.

## Definition of done

- works conceptually across agent-platform releases
- distinguishes core workflow from adapter details
- has no sensitive or licensed copied content
- provides an actionable clinician/user handoff
- includes failure and recovery behavior
- links from the README or an appropriate index
