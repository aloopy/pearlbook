#!/usr/bin/env python3
"""Bounded stdio MCP server for one explicitly authorized PearlBook vault."""

from __future__ import annotations

import argparse
import secrets
import time
from dataclasses import dataclass
from threading import Lock

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

from pearlbook_vault import (
    VaultError,
    apply_write,
    authorized_root,
    preview_write,
    read_note,
    search_notes,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--vault", required=True, help="absolute path to the vault replica")
    parser.add_argument("--vault-name", default="PearlBook")
    return parser.parse_args()


ARGS = parse_args()
ROOT = authorized_root(ARGS.vault)
VAULT_NAME = ARGS.vault_name.strip() or ROOT.name

mcp = FastMCP(
    "PearlBook",
    instructions=(
        "Bounded access to one user-authorized clinical learning vault. Search "
        "before reading. Before a write, preview the exact diff and obtain explicit "
        "user approval before applying its change_id."
    ),
)

READ_ONLY = ToolAnnotations(
    readOnlyHint=True,
    destructiveHint=False,
    openWorldHint=False,
)
WRITES_VAULT = ToolAnnotations(
    readOnlyHint=False,
    destructiveHint=False,
    openWorldHint=False,
)


@dataclass(frozen=True)
class ProposedWrite:
    note_path: str
    content: str
    expected_sha256: str
    created_at: float


PROPOSALS: dict[str, ProposedWrite] = {}
PROPOSAL_LOCK = Lock()
PROPOSAL_TTL_SECONDS = 15 * 60


@mcp.tool(annotations=READ_ONLY)
def pearlbook_search(query: str, limit: int = 10) -> dict:
    """Search titles and Markdown bodies in the authorized PearlBook vault."""
    try:
        return search_notes(ROOT, VAULT_NAME, query, limit)
    except VaultError as exc:
        return {"error": str(exc), "query": query, "count": 0, "results": []}


@mcp.tool(annotations=READ_ONLY)
def pearlbook_read(note_path: str) -> dict:
    """Read one Markdown note using its exact vault-relative path."""
    try:
        return read_note(ROOT, VAULT_NAME, note_path)
    except (OSError, UnicodeError, VaultError) as exc:
        return {"error": str(exc), "note_path": note_path}


@mcp.tool(annotations=READ_ONLY)
def pearlbook_preview_write(
    note_path: str, content: str, expected_sha256: str
) -> dict:
    """Preview one exact note write; use 'new' as the hash for a new note."""
    try:
        preview = preview_write(
            ROOT, VAULT_NAME, note_path, content, expected_sha256
        )
    except (OSError, UnicodeError, VaultError) as exc:
        return {"error": str(exc), "note_path": note_path}

    change_id = secrets.token_urlsafe(24)
    now = time.monotonic()
    with PROPOSAL_LOCK:
        expired = [
            key
            for key, proposal in PROPOSALS.items()
            if now - proposal.created_at > PROPOSAL_TTL_SECONDS
        ]
        for key in expired:
            PROPOSALS.pop(key, None)
        PROPOSALS[change_id] = ProposedWrite(
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
    """Apply one unexpired, previously previewed write after user approval."""
    with PROPOSAL_LOCK:
        proposal = PROPOSALS.pop(change_id, None)
    if proposal is None:
        return {"error": "change_id is unknown, expired, or already used"}
    if time.monotonic() - proposal.created_at > PROPOSAL_TTL_SECONDS:
        return {"error": "change_id expired; preview the write again"}
    try:
        return apply_write(
            ROOT,
            VAULT_NAME,
            proposal.note_path,
            proposal.content,
            proposal.expected_sha256,
        )
    except (OSError, UnicodeError, VaultError) as exc:
        return {"error": str(exc), "note_path": proposal.note_path}


if __name__ == "__main__":
    mcp.run()
