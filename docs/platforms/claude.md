# Claude setup

This adapter is intentionally reserved for a Claude agent to draft and verify against current official Claude Code and Cowork documentation.

It should preserve the same PearlBook contract:

- local vault access when the vault is on the current machine
- a phone-to-computer path when a personal machine is online
- a persistent private host and narrow tool for always-available access
- human-entered login and MFA for licensed references
- no personal vault, browser state, or credentials in the public repository
- explicit disclosure when the vault or a source could not be consulted

Do not infer Claude credential or remote-access behavior from the Codex adapter. Verify those platform details independently before replacing this handoff.
