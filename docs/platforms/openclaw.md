# OpenClaw setup

This adapter describes the current high-control PearlBook pattern: a dedicated home computer, an Obsidian vault synced to that computer, and a Telegram conversation surface.

```text
Phone / Telegram
       |
       v
OpenClaw on a dedicated home computer
       |-- local PearlBook vault
       |-- clinician-authenticated browser profile
       `-- public research tools
```

## Operating model

- The clinician messages the agent from a phone through Telegram.
- OpenClaw reads and maintains the local Obsidian vault under the [clinical topic workflow](../../workflows/clinical-topic.md).
- The clinician logs into licensed references interactively on the home computer.
- OpenClaw may reuse the authorized browser session but receives no password, MFA seed, recovery code, or exported cookie archive.
- Obsidian Sync can make the same vault available on the phone and other computers. A single-device local vault also works if cross-device access is not needed.

## Host checklist

- Use a dedicated, non-administrator operating-system account.
- Enable full-disk encryption, automatic security updates, screen locking, and device recovery controls.
- Restrict the agent to the vault and a dedicated workspace, not the entire home directory.
- Use a dedicated browser profile for licensed references.
- Complete login and MFA manually; stop for reauthentication when the session expires.
- Limit the Telegram bot to the intended account or chat and review the bot's token handling.
- Do not send patient information, passwords, recovery codes, or licensed source text through Telegram.
- Back up the vault independently of Obsidian Sync and the agent.

## Optional headless variant

The dedicated computer may be replaced with a persistent private host running [Obsidian Headless](https://obsidian.md/help/headless). Keep the messaging adapter and vault tool narrow; do not expose a public shell or general file browser. See [Deployment options](../deployment-options.md).
