"""Read-only, path-bounded operations for a PearlBook Markdown vault."""

from __future__ import annotations

import hashlib
import os
import re
import tempfile
from difflib import unified_diff
from pathlib import Path
from urllib.parse import urlencode


MAX_NOTE_BYTES = 2_000_000
MAX_READ_CHARS = 200_000
EXCLUDED_PARTS = {".git", ".obsidian", ".trash", "node_modules"}


class VaultError(ValueError):
    """Raised when a vault request crosses a PearlBook safety boundary."""


def authorized_root(raw_path: str | Path) -> Path:
    raw = str(raw_path).strip()
    if not raw:
        raise VaultError("an explicit PearlBook vault path is required")
    root = Path(raw).expanduser().resolve(strict=True)
    if not root.is_dir():
        raise VaultError("the authorized PearlBook vault is not a directory")
    home = Path.home().resolve()
    if root in {Path(root.anchor), home, home / "Documents"}:
        raise VaultError("refusing a root or broad user directory")
    return root


def _safe_note(root: Path, relative_path: str) -> Path:
    candidate_input = Path(relative_path)
    if candidate_input.is_absolute() or ".." in candidate_input.parts:
        raise VaultError("note_path must be a vault-relative path")
    candidate = (root / candidate_input).resolve(strict=True)
    try:
        candidate.relative_to(root)
    except ValueError as exc:
        raise VaultError("note path escapes the authorized vault") from exc
    if candidate.suffix.lower() != ".md" or not candidate.is_file():
        raise VaultError("only existing Markdown notes can be read")
    if candidate.stat().st_size > MAX_NOTE_BYTES:
        raise VaultError("note exceeds the read-only service size limit")
    return candidate


def _safe_write_target(root: Path, relative_path: str) -> Path:
    candidate_input = Path(relative_path)
    if candidate_input.is_absolute() or ".." in candidate_input.parts:
        raise VaultError("note_path must be a vault-relative path")
    if candidate_input.suffix.lower() != ".md":
        raise VaultError("only Markdown notes can be written")
    candidate = (root / candidate_input).resolve(strict=False)
    try:
        candidate.relative_to(root)
    except ValueError as exc:
        raise VaultError("note path escapes the authorized vault") from exc
    try:
        parent = candidate.parent.resolve(strict=True)
    except OSError as exc:
        raise VaultError("note parent directory does not exist") from exc
    try:
        parent.relative_to(root)
    except ValueError as exc:
        raise VaultError("note parent escapes the authorized vault") from exc
    if candidate.exists():
        resolved = candidate.resolve(strict=True)
        try:
            resolved.relative_to(root)
        except ValueError as exc:
            raise VaultError("note path escapes the authorized vault") from exc
        if not resolved.is_file():
            raise VaultError("note target is not a file")
        return resolved
    return candidate


def _iter_notes(root: Path):
    for path in root.rglob("*.md"):
        relative = path.relative_to(root)
        if any(part in EXCLUDED_PARTS or part.startswith(".") for part in relative.parts):
            continue
        try:
            resolved = path.resolve(strict=True)
            resolved.relative_to(root)
        except (OSError, ValueError):
            continue
        if resolved.is_file() and resolved.stat().st_size <= MAX_NOTE_BYTES:
            yield resolved


def _snippet(text: str, query: str, width: int = 360) -> str:
    collapsed = re.sub(r"\s+", " ", text).strip()
    index = collapsed.casefold().find(query.casefold())
    if index < 0:
        return collapsed[:width]
    start = max(0, index - width // 3)
    end = min(len(collapsed), start + width)
    prefix = "..." if start else ""
    suffix = "..." if end < len(collapsed) else ""
    return f"{prefix}{collapsed[start:end]}{suffix}"


def obsidian_link(vault_name: str, relative_path: str) -> str:
    query = urlencode({"vault": vault_name, "file": relative_path}, safe="")
    return f"https://obsid.net/?{query}"


def content_sha256(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def search_notes(root: Path, vault_name: str, query: str, limit: int = 10) -> dict:
    needle = query.strip()
    if not needle:
        raise VaultError("query must not be empty")
    if not 1 <= limit <= 25:
        raise VaultError("limit must be between 1 and 25")

    matches = []
    folded = needle.casefold()
    for path in _iter_notes(root):
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            continue
        title = path.stem
        body_folded = text.casefold()
        title_count = title.casefold().count(folded)
        body_count = body_folded.count(folded)
        if not title_count and not body_count:
            continue
        relative = path.relative_to(root).as_posix()
        matches.append(
            (
                title_count * 100 + min(body_count, 20),
                {
                    "title": title,
                    "note_path": relative,
                    "snippet": _snippet(text, needle),
                    "obsidian_url": obsidian_link(vault_name, relative),
                },
            )
        )

    matches.sort(key=lambda item: (-item[0], item[1]["note_path"].casefold()))
    results = [item[1] for item in matches[:limit]]
    return {"query": needle, "count": len(results), "results": results}


def read_note(root: Path, vault_name: str, note_path: str) -> dict:
    path = _safe_note(root, note_path)
    content = path.read_text(encoding="utf-8")
    if len(content) > MAX_READ_CHARS:
        raise VaultError("note exceeds the response character limit")
    relative = path.relative_to(root).as_posix()
    return {
        "title": path.stem,
        "note_path": relative,
        "content": content,
        "sha256": content_sha256(content),
        "obsidian_url": obsidian_link(vault_name, relative),
    }


def preview_write(
    root: Path,
    vault_name: str,
    note_path: str,
    content: str,
    expected_sha256: str,
) -> dict:
    if "\x00" in content:
        raise VaultError("note content contains a null byte")
    if len(content) > MAX_READ_CHARS or len(content.encode("utf-8")) > MAX_NOTE_BYTES:
        raise VaultError("proposed note exceeds the service size limit")

    target = _safe_write_target(root, note_path)
    exists = target.exists()
    previous = target.read_text(encoding="utf-8") if exists else ""
    current_hash = content_sha256(previous) if exists else "new"
    if expected_sha256 != current_hash:
        raise VaultError(
            "source note changed or was not read; read it again before previewing"
        )

    relative = target.relative_to(root).as_posix()
    diff = "".join(
        unified_diff(
            previous.splitlines(keepends=True),
            content.splitlines(keepends=True),
            fromfile=f"a/{relative}" if exists else "/dev/null",
            tofile=f"b/{relative}",
        )
    )
    return {
        "title": target.stem,
        "note_path": relative,
        "current_sha256": current_hash,
        "proposed_sha256": content_sha256(content),
        "diff": diff or "No changes.",
        "obsidian_url": obsidian_link(vault_name, relative),
    }


def apply_write(
    root: Path,
    vault_name: str,
    note_path: str,
    content: str,
    expected_sha256: str,
) -> dict:
    preview = preview_write(root, vault_name, note_path, content, expected_sha256)
    if preview["diff"] == "No changes.":
        return {**preview, "applied": False}

    target = _safe_write_target(root, note_path)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{target.name}.", suffix=".tmp", dir=str(target.parent)
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, target)
    finally:
        if temporary.exists():
            temporary.unlink()

    return {**preview, "applied": True}
