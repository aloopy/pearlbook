#!/usr/bin/env python3
"""Configure an existing vault or create a private PearlBook starter vault."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path


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

Ask your agent to search before creating a new note and to return a clickable Obsidian link with each vault-backed answer.
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
    home = Path.home().resolve()
    root = Path(path.anchor)
    if path in {root, home, home / "Documents"}:
        raise ValueError("choose a dedicated vault folder, not a root or broad user directory")
    return path


def markdown_config(vault_name: str, vault_path: Path, access_mode: str) -> str:
    return "\n".join(
        (
            "# Local PearlBook configuration",
            "",
            "```yaml",
            f"vault_name: {json.dumps(vault_name)}",
            f"vault_path: {json.dumps(str(vault_path))}",
            f"access_mode: {access_mode}",
            "default_access: read_only",
            "note_changes: explicit_request_only",
            "link_style: obsid_net",
            "link_base: https://obsid.net/",
            "```",
            "",
        )
    )


def scaffold(vault_path: Path) -> None:
    for folder in STARTER_FOLDERS:
        (vault_path / folder).mkdir(parents=True, exist_ok=True)

    welcome = vault_path / "Start here.md"
    if not welcome.exists():
        welcome.write_text(WELCOME_NOTE, encoding="utf-8")

    template = vault_path / "Templates" / "Topic.md"
    if not template.exists():
        template.write_text(TOPIC_TEMPLATE, encoding="utf-8")


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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Use an existing Obsidian vault or create a PearlBook starter vault."
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--existing", metavar="PATH")
    mode.add_argument("--create", metavar="PATH")
    parser.add_argument("--vault-name")
    parser.add_argument(
        "--access",
        choices=("local", "headless"),
        default="local",
        help="record whether this path is a local vault or a Headless Sync replica",
    )
    parser.add_argument("--config", type=Path, default=default_config_path())
    parser.add_argument(
        "--scaffold-existing",
        action="store_true",
        help="add missing starter folders and files to an existing vault",
    )
    parser.add_argument("--yes", action="store_true", help="confirm an explicit --create path")
    parser.add_argument("--force", action="store_true", help="replace an existing local config")
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def main() -> None:
    try:
        args = parse_args()
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
            print(f"Scaffold: {mode == 'create' or args.scaffold_existing}")
            return

        if mode == "create":
            vault_path.mkdir(parents=True, exist_ok=True)
        if mode == "create" or args.scaffold_existing:
            scaffold(vault_path)

        write_config(
            config_path,
            markdown_config(vault_name, vault_path, args.access),
            args.force,
        )

        print("PearlBook is ready.")
        print(f"Vault folder: {vault_path}")
        print("Next steps:")
        if args.access == "local":
            print("  1. In Obsidian, choose Open folder as vault and select this folder.")
            print("  2. In Codex, open this same folder as the project.")
            print("  3. Start a new task and ask PearlBook to find or create a learning note.")
            print("  4. Optionally enable Obsidian Sync for access on other devices.")
        else:
            print("  1. Do not open this replica with Obsidian desktop Sync on this host.")
            print("  2. Complete references/headless-chatgpt.md with the user.")
            print("  3. Keep initial Headless Sync and MCP access read-only.")
    except (OSError, ValueError) as exc:
        print(f"setup_pearlbook.py: error: {exc}", file=sys.stderr)
        raise SystemExit(2) from exc


if __name__ == "__main__":
    main()
