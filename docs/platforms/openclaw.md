# OpenClaw setup

Use this adapter when the user wants a full agent on an always-on computer or private VM and prefers to contact it through a messaging app. This is the highest-control and most setup-intensive PearlBook path.

OpenClaw is the agent host in this pattern. It is not merely a vault MCP server, and it can use only the local files, browser, research tools, and messaging adapters the operator explicitly configures.

```text
Phone / configured messaging app
       |
       v
OpenClaw on a dedicated home computer
       |-- local PearlBook vault
       |-- optional clinician-authenticated browser profile
       `-- optional public research tools
```

## Operating model

- The clinician messages the agent from a phone through a supported messaging adapter chosen and secured by the user. Telegram is one example, not a requirement.
- OpenClaw reads and maintains the local Obsidian vault under the [clinical topic workflow](../../workflows/clinical-topic.md).
- If the user configures an authenticated reference, the clinician logs into it interactively on the host.
- OpenClaw may reuse that authorized browser session but receives no password, MFA seed, recovery code, or exported cookie archive.
- Obsidian Sync can make the same vault available on the phone and other computers. A single-device local vault also works if cross-device access is not needed.

CorePendium is one emergency-medicine example of an optional authenticated reference. OpenClaw and PearlBook do not require it.

## Agent handoff

An agent applying this adapter should first confirm:

1. the host that will remain online;
2. the messaging adapter the user selected;
3. the exact authorized vault path;
4. whether browser-based sources are needed at all; and
5. whether Obsidian Sync or another user-controlled backup/sync path is configured.

Do not infer Telegram, CorePendium, a VM, or multi-device Obsidian Sync from this example.

## Host checklist

- Use a dedicated, non-administrator operating-system account.
- Enable full-disk encryption, automatic security updates, screen locking, and device recovery controls.
- Restrict the agent to the vault and a dedicated workspace, not the entire home directory.
- Use a dedicated browser profile for licensed references.
- Complete login and MFA manually; stop for reauthentication when the session expires.
- Limit the messaging integration to the intended account or conversation and review its token handling.
- Do not send patient information, passwords, recovery codes, or licensed source text through the messaging service.
- Back up the vault independently of Obsidian Sync and the agent.

## Optional headless variant

The dedicated computer may be replaced with a persistent private host running [Obsidian Headless](https://obsidian.md/help/headless). Keep the messaging adapter and vault tool narrow; do not expose a public shell or general file browser. See [Deployment options](../deployment-options.md).

## Recovery behavior

If the host, vault, messaging adapter, Sync, or an optional authenticated source is unavailable, report exactly which component was not consulted. Do not silently fall back to model memory or claim a note was updated when the host did not apply the change.
