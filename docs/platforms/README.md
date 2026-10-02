# Platform adapters

PearlBook has one workflow contract and three primary agent adapters. Choose the adapter that matches where the agent will run. Do not configure all three by default.

**People:** choose the simplest adapter that meets your availability and phone-access needs, then follow only that setup page.

**Agents:** first establish whether the user wants a dot's cloud computer or a host they maintain, and how they want to reach PearlBook. If the user has not chosen a platform, help them choose from [Deployment options](../deployment-options.md) before creating files, installing software, or requesting credentials.

## Shared contract

Every adapter must:

- operate only on an explicitly authorized vault, following the shared rules in the vault-root `AGENTS.md`;
- search before creating a note;
- distinguish answering from editing;
- make writes reviewable and preserve unrelated content;
- identify the sources materially used;
- return the exact note path and a clickable note link when configured;
- stop for authentication, uncertainty, or unsafe external action; and
- say when the vault or a requested source was not consulted.

Authenticated reference browsing is optional. It can use a local or cloud agent's dedicated, user-authenticated browser profile (signed into only the needed sources) or a separately designed, narrow source tool. A tool-only MCP host does not inherit browser sessions.

## Adapter boundaries

### OpenClaw

- **Agent host:** an always-on personal computer or private VM
- **Phone surface:** a messaging adapter chosen and secured by the user
- **Vault access:** direct local files
- **Browser access:** a dedicated local profile, signed into only the needed reference sites, authenticated interactively by the user
- **Tradeoff:** most control and extensibility; most setup, patching, and monitoring

Read [OpenClaw setup](openclaw.md).

### Codex and ChatGPT

**Choose a dot for ChatGPT integration without bringing an extra computer or hosting a VM.** Its cloud computer holds the authorized replica and its browser supports private user login. Available ChatGPT tools can turn retrieved learning material into images and files; the [board-pearl workflow](../../workflows/board-pearl-linked-pdf.md) is one example. Local Codex and a private MCP host remain separate choices.

- **Local agent:** Codex on the computer that holds the vault
- **Phone surface:** Codex Remote steers that connected computer
- **Cloud computer:** a dot can use on-demand Headless Sync and a separately authenticated browser; see the adapter for private login and recovery
- **Private-host alternative:** ChatGPT calls a narrow PearlBook MCP tool on a persistent private host
- **Browser boundary:** local Codex may use an approved local browser; ChatGPT through a tool-only host does not inherit the host's browser login
- **Tradeoff:** simplest guided PearlBook setup and an OpenAI-native remote path; a persistent private service requires a maintained host, while dot cloud work depends on available platform capabilities and verified sync

Read [Codex and ChatGPT setup](codex-chatgpt.md).

### Claude

- **Local agent:** Claude Code on the computer that holds the vault
- **Phone surface:** Remote Control steers that connected computer
- **Always-available alternative:** claude.ai calls a narrow remote MCP tool on a persistent private host
- **Browser boundary:** local Claude Code may use an approved browser integration; claude.ai through a tool-only host does not inherit the host's browser login
- **Tradeoff:** a Claude-native local and remote-control path; the operator must provide secure ingress for an always-available remote MCP service

Read [Claude setup](claude.md).

## Hybrid setups

A user may intentionally run more than one adapter against the same synchronized vault. If so:

1. designate one canonical vault and synchronization mechanism;
2. avoid concurrent writes to the same note;
3. use the same search-before-create and preview-before-apply rules;
4. keep platform-specific configuration outside the public vault content; and
5. test conflict recovery before relying on the hybrid setup.

Redundant read paths can improve availability. Redundant unsynchronized write paths usually increase ambiguity and conflict risk.
