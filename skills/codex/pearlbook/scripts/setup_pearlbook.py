#!/usr/bin/env python3
"""Configure an existing vault or create a private PearlBook starter vault."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from pearlbook_vault import (  # noqa: E402
    LINK_STYLES,
    VaultError,
    broad_path_reason,
    normalize_link_settings,
)


STARTER_FOLDERS = (
    "Inbox",
    "Topics",
    "Pearls",
    "Cases",
    "Sources",
    "Templates",
    "attachments",
)

WELCOME_NOTE = """# Welcome to PearlBook

PearlBook is your private, clinician-owned learning vault.

- Capture unprocessed material in `Inbox`.
- Keep durable clinical subjects in `Topics`.
- Store one focused teaching point per note in `Pearls`.
- Use `Cases` only for de-identified learning records. Never store PHI.
- Link claims to their sources and verify time-sensitive clinical information.

Ask your agent to search before creating a new note and to return the note path and an Obsidian link with each vault-backed answer.
"""

# Shared instructions for every agent that opens this vault. Codex and OpenClaw
# read AGENTS.md; Claude Code v2.1.277+ reads it when no CLAUDE.md exists.
VAULT_AGENTS = """# AGENTS.md — PearlBook vault

This folder is a private, clinician-owned Obsidian learning vault. These rules
apply to every agent (Codex, Claude Code, OpenClaw, or another tool).

## Scope

- Work only inside this vault and any workspace the user explicitly adds.
- Do not read or change `.obsidian/`, `.trash/`, `.git/`, or other hidden folders.
- Never store patient information (PHI), credentials, cookies, or browser data here.

## Workflow

1. Search titles, aliases, tags, and note bodies before creating anything.
2. Read the closest existing note and the sources it links.
3. Read the relevant source before drafting; verify time-sensitive or high-risk claims.
4. Answer concisely, with uncertainty and local-protocol caveats where relevant.
5. Edit only when the user asks. Show the proposed change first and apply only
   the change the user approved. Preserve unrelated content.
6. Return the vault-relative note path (and an Obsidian link when configured)
   plus the sources materially used.

## Licensed sources

Use a licensed reference only through the user's own logged-in account, one
page at a time in response to the user's question. Store your own summary and a
link back to the source; do not paste the source's text into notes, crawl the
site, or build a copy of it.

## Failure behavior

If the vault or a source could not be consulted, say so. Never substitute
model memory for the user's notes without saying so.
"""

TOPIC_TEMPLATE = """---
title: ""
aliases: []
tags: []
status: active
updated: YYYY-MM-DD
---

# Topic

## Recognition

## Immediate actions

## Diagnostic pivots

## Management

## Pitfalls

## Disposition

## Sources
"""


def default_vault_path() -> Path:
    return Path.home() / "Documents" / "PearlBook"


def default_config_path() -> Path:
    return Path(__file__).resolve().parent.parent / "references" / "local-config.md"


def safe_path(raw_path: str) -> Path:
    if not raw_path.strip():
        raise ValueError("vault path must not be empty")
    path = Path(raw_path).expanduser().resolve(strict=False)
    reason = broad_path_reason(path)
    if reason:
        raise ValueError(f"choose a dedicated vault folder: {reason}")
    return path


def markdown_config(
    vault_name: str,
    vault_path: Path,
    access_mode: str,
    link_style: str = "obsidian",
    link_base: str | None = None,
) -> str:
    lines = [
        "# Local PearlBook configuration",
        "",
        "```yaml",
        f"vault_name: {json.dumps(vault_name)}",
        f"vault_path: {json.dumps(str(vault_path))}",
        f"access_mode: {access_mode}",
        "default_access: read_only",
        "note_changes: explicit_request_only",
        f"link_style: {link_style}",
    ]
    if link_base:
        lines.append(f"link_base: {link_base}")
    lines += ["```", ""]
    return "\n".join(lines)


def scaffold(vault_path: Path) -> None:
    for folder in STARTER_FOLDERS:
        (vault_path / folder).mkdir(parents=True, exist_ok=True)

    files = {
        vault_path / "Start here.md": WELCOME_NOTE,
        vault_path / "AGENTS.md": VAULT_AGENTS,
        vault_path / "Templates" / "Topic.md": TOPIC_TEMPLATE,
    }
    for path, content in files.items():
        if not path.exists():
            path.write_text(content, encoding="utf-8")


def write_config(config_path: Path, content: str, force: bool) -> None:
    if config_path.exists() and not force:
        raise ValueError(f"configuration already exists: {config_path}; use --force to replace it")
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(content, encoding="utf-8")
    if os.name != "nt":
        config_path.chmod(0o600)


def confirm(prompt: str) -> bool:
    return input(f"{prompt} [y/N]: ").strip().lower() in {"y", "yes"}


def interactive_choice() -> tuple[str, str, bool]:
    if not sys.stdin.isatty():
        raise ValueError(
            "no terminal for interactive setup; rerun with --existing PATH "
            "or --create PATH --yes"
        )
    print("PearlBook first-run setup")
    print("  1. Use an existing Obsidian vault")
    print("  2. Create a new PearlBook vault (recommended for beginners)")
    choice = input("Choose 1 or 2 [2]: ").strip() or "2"
    if choice == "1":
        raw_path = input("Absolute path to the existing vault: ").strip()
        return "existing", raw_path, False
    if choice != "2":
        raise ValueError("choice must be 1 or 2")

    suggested = default_vault_path()
    raw_path = input(f"New vault path [{suggested}]: ").strip() or str(suggested)
    if not confirm(f"Create a new PearlBook vault at {raw_path}?"):
        raise ValueError("setup cancelled; no vault was created")
    return "create", raw_path, True


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Use an existing Obsidian vault or create a PearlBook starter vault."
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--existing", metavar="PATH", help="configure an existing vault")
    mode.add_argument("--create", metavar="PATH", help="create a new starter vault (needs --yes)")
    parser.add_argument("--vault-name")
    parser.add_argument(
        "--access",
        choices=("local", "headless"),
        default="local",
        help="record whether this path is a local vault or a Headless Sync replica",
    )
    parser.add_argument(
        "--link-style",
        choices=LINK_STYLES,
        default="obsidian",
        help="obsidian:// links (default), an opt-in HTTPS bridge, or paths only",
    )
    parser.add_argument(
        "--link-base",
        help="HTTPS redirector base URL; required with --link-style https_bridge",
    )
    parser.add_argument("--config", type=Path, default=default_config_path())
    parser.add_argument(
        "--scaffold-existing",
        action="store_true",
        help="add missing starter folders and files (including AGENTS.md) to an existing vault",
    )
    parser.add_argument("--yes", action="store_true", help="confirm an explicit --create path")
    parser.add_argument("--force", action="store_true", help="replace an existing local config")
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    try:
        args = parse_args(argv)
        link_style, link_base = normalize_link_settings(args.link_style, args.link_base)
        if args.existing:
            mode, raw_path, creation_confirmed = "existing", args.existing, False
        elif args.create:
            mode, raw_path, creation_confirmed = "create", args.create, args.yes
        else:
            mode, raw_path, creation_confirmed = interactive_choice()

        vault_path = safe_path(raw_path)
        vault_name = (args.vault_name or vault_path.name).strip()
        if not vault_name:
            raise ValueError("vault name must not be empty")

        if mode == "existing":
            if not vault_path.is_dir():
                raise ValueError(f"existing vault directory not found: {vault_path}")
        else:
            if not creation_confirmed and not args.dry_run:
                raise ValueError("creating a vault requires confirmation; rerun with --yes")
            if vault_path.exists() and any(vault_path.iterdir()):
                raise ValueError(
                    "new vault path is not empty; use --existing instead to preserve its contents"
                )

        config_path = args.config.expanduser().resolve(strict=False)
        if config_path.exists() and not args.force and not args.dry_run:
            raise ValueError(
                f"configuration already exists: {config_path}; use --force to replace it"
            )
        if args.dry_run:
            print(f"Mode: {mode}")
            print(f"Vault: {vault_name}")
            print(f"Path: {vault_path}")
            print(f"Config: {config_path}")
            print(f"Link style: {link_style}")
            print(f"Scaffold: {mode == 'create' or args.scaffold_existing}")
            return

        if mode == "create":
            vault_path.mkdir(parents=True, exist_ok=True)
        if mode == "create" or args.scaffold_existing:
            scaffold(vault_path)

        write_config(
            config_path,
            markdown_config(vault_name, vault_path, args.access, link_style, link_base),
            args.force,
        )

        print("PearlBook is ready.")
        print(f"Vault folder: {vault_path}")
        print("Next steps:")
        if args.access == "local":
            print("  1. In Obsidian, choose Open folder as vault and select this folder.")
            print("  2. Open this same folder as the project in your agent (Codex, Claude Code, ...).")
            print("  3. Keep one AGENTS.md at the vault root as the shared agent rules.")
            print("  4. Start a new session and ask PearlBook to find or create a learning note.")
            print("  5. Optionally enable Obsidian Sync for access on other devices.")
        else:
            print("  1. Do not open this replica with Obsidian desktop Sync on this host.")
            print("  2. Complete references/headless-chatgpt.md with the user.")
            print("  3. Keep initial Headless Sync and MCP access read-only.")
    except (EOFError, KeyboardInterrupt) as exc:
        print(
            "setup_pearlbook.py: error: setup cancelled; rerun with --existing PATH "
            "or --create PATH --yes",
            file=sys.stderr,
        )
        raise SystemExit(2) from exc
    except (OSError, ValueError, VaultError) as exc:
        print(f"setup_pearlbook.py: error: {exc}", file=sys.stderr)
        raise SystemExit(2) from exc


if __name__ == "__main__":
    main()
