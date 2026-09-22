#!/usr/bin/env python3
"""Bounded stdio MCP server for one explicitly authorized PearlBook vault.

Approval boundary: this server separates preview from apply and rejects stale
or reused proposals, but it cannot see the user. Whether a person actually
approved a write is enforced by the chat client (ChatGPT, Claude, Codex, or
another MCP host) through its tool-confirmation prompts. ``pearlbook_apply_write``
is therefore annotated as destructive so clients treat it as requiring
confirmation.
"""

from __future__ import annotations

import argparse
import secrets
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from threading import Lock

sys.path.insert(0, str(Path(__file__).resolve().parent))

from mcp.server.fastmcp import FastMCP  # noqa: E402
from mcp.types import ToolAnnotations  # noqa: E402

from pearlbook_vault import (  # noqa: E402
    LINK_STYLES,
    VaultError,
    apply_write,
    authorized_root,
    normalize_link_settings,
    preview_write,
    read_note,
    search_notes,
)


PROPOSAL_TTL_SECONDS = 15 * 60

READ_ONLY = ToolAnnotations(
    readOnlyHint=True,
    destructiveHint=False,
    openWorldHint=False,
)
# Applying a write can replace an entire note, so clients should treat it as
# destructive and ask the user before each call.
WRITES_VAULT = ToolAnnotations(
    readOnlyHint=False,
    destructiveHint=True,
    idempotentHint=False,
    openWorldHint=False,
)


@dataclass(frozen=True)
class ProposedWrite:
    note_path: str
    content: str
    expected_sha256: str
    created_at: float


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n", 1)[0])
    parser.add_argument("--vault", required=True, help="absolute path to the vault replica")
    parser.add_argument("--vault-name", default="PearlBook")
    parser.add_argument(
        "--link-style",
        choices=LINK_STYLES,
        default="obsidian",
        help="obsidian:// URIs (default), an opt-in HTTPS bridge, or paths only",
    )
    parser.add_argument(
        "--link-base",
        help="HTTPS redirector base URL; required with --link-style https_bridge",
    )
    return parser.parse_args(argv)


def build_server(
    root: Path,
    vault_name: str,
    link_style: str = "obsidian",
    link_base: str | None = None,
) -> FastMCP:
    link_style, link_base = normalize_link_settings(link_style, link_base)
    proposals: dict[str, ProposedWrite] = {}
    lock = Lock()

    mcp = FastMCP(
        "PearlBook",
        instructions=(
            "Bounded access to one user-authorized clinical learning vault. Search "
            "before reading. Before a write, show the user the exact preview diff "
            "and obtain explicit approval for that specific change before applying "
            "its change_id. Never apply a change the user has not seen."
        ),
    )

    @mcp.tool(annotations=READ_ONLY)
    def pearlbook_search(query: str, limit: int = 10) -> dict:
        """Search titles and Markdown bodies in the authorized PearlBook vault."""
        try:
            return search_notes(root, vault_name, query, limit, link_style, link_base)
        except VaultError as exc:
            return {"error": str(exc), "query": query, "count": 0, "results": []}

    @mcp.tool(annotations=READ_ONLY)
    def pearlbook_read(note_path: str) -> dict:
        """Read one Markdown note using its exact vault-relative path."""
        try:
            return read_note(root, vault_name, note_path, link_style, link_base)
        except (OSError, UnicodeError, VaultError) as exc:
            return {"error": str(exc), "note_path": note_path}

    @mcp.tool(annotations=READ_ONLY)
    def pearlbook_preview_write(
        note_path: str, content: str, expected_sha256: str
    ) -> dict:
        """Preview one exact note write without changing the vault.

        Use the sha256 from pearlbook_read, or 'new' for a new note. Show the
        returned diff to the user before calling pearlbook_apply_write.
        """
        try:
            preview = preview_write(
                root, vault_name, note_path, content, expected_sha256, link_style, link_base
            )
        except (OSError, UnicodeError, VaultError) as exc:
            return {"error": str(exc), "note_path": note_path}

        change_id = secrets.token_urlsafe(24)
        now = time.monotonic()
        with lock:
            expired = [
                key
                for key, proposal in proposals.items()
                if now - proposal.created_at > PROPOSAL_TTL_SECONDS
            ]
            for key in expired:
                proposals.pop(key, None)
            proposals[change_id] = ProposedWrite(
                note_path=note_path,
                content=content,
                expected_sha256=expected_sha256,
                created_at=now,
            )
        return {
            **preview,
            "change_id": change_id,
            "expires_in_seconds": PROPOSAL_TTL_SECONDS,
            "applied": False,
        }

    @mcp.tool(annotations=WRITES_VAULT)
    def pearlbook_apply_write(change_id: str) -> dict:
        """Apply one unexpired, previously previewed write.

        Call only after the user has seen that preview's diff and explicitly
        approved this change. Can replace a note's entire content.
        """
        with lock:
            proposal = proposals.pop(change_id, None)
        if proposal is None:
            return {"error": "change_id is unknown, expired, or already used"}
        if time.monotonic() - proposal.created_at > PROPOSAL_TTL_SECONDS:
            return {"error": "change_id expired; preview the write again"}
        try:
            return apply_write(
                root,
                vault_name,
                proposal.note_path,
                proposal.content,
                proposal.expected_sha256,
                link_style,
                link_base,
            )
        except (OSError, UnicodeError, VaultError) as exc:
            return {"error": str(exc), "note_path": proposal.note_path}

    return mcp


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    try:
        root = authorized_root(args.vault)
        vault_name = args.vault_name.strip() or root.name
        server = build_server(root, vault_name, args.link_style, args.link_base)
    except (OSError, VaultError) as exc:
        print(f"pearlbook_mcp.py: error: {exc}", file=sys.stderr)
        raise SystemExit(2) from exc
    server.run()


if __name__ == "__main__":
    main()
