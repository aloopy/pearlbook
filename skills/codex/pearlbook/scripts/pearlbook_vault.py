"""Path-bounded search, read, and preview-then-apply write operations for one
PearlBook Markdown vault.

Every operation is confined to a single explicitly authorized vault root.
Hidden paths (any segment starting with ".", such as .obsidian, .trash, or
.git) are excluded from search, reads, and writes alike.
"""

from __future__ import annotations

import hashlib
import os
import re
import tempfile
from difflib import unified_diff
from pathlib import Path
from urllib.parse import quote, urlparse


MAX_NOTE_BYTES = 2_000_000
MAX_READ_CHARS = 200_000
EXCLUDED_PARTS = {".git", ".obsidian", ".trash", "node_modules"}

LINK_STYLES = ("obsidian", "https_bridge", "path")
LEGACY_LINK_STYLES = {"obsid_net": "https_bridge"}

# Directories that must never be used as, or contain, a vault root.
_SYSTEM_TREES_POSIX = (
    "/bin",
    "/boot",
    "/dev",
    "/etc",
    "/lib",
    "/lib64",
    "/proc",
    "/sbin",
    "/sys",
    "/usr",
    "/System",
    "/Library",
    "/Applications",
    "/private/etc",
    "/cores",
)
# Broad directories that must not be the vault root itself, although a
# dedicated subfolder inside them can be legitimate (for example a temporary
# test directory or a synced Obsidian folder).
_BROAD_DIRS_POSIX = (
    "/",
    "/home",
    "/Users",
    "/root",
    "/opt",
    "/srv",
    "/mnt",
    "/media",
    "/tmp",
    "/var",
    "/private",
    "/private/tmp",
    "/private/var",
    "/Volumes",
)
_BROAD_HOME_CHILDREN = (
    "Documents",
    "Desktop",
    "Downloads",
    "Library",
    "Library/CloudStorage",
    "Library/Mobile Documents",
    "Dropbox",
    "OneDrive",
    "Google Drive",
    "iCloud Drive",
)


class VaultError(ValueError):
    """Raised when a vault request crosses a PearlBook safety boundary."""


def _windows_system_trees() -> tuple[str, ...]:
    candidates = [
        os.environ.get("SystemRoot") or os.environ.get("WINDIR") or r"C:\Windows",
        os.environ.get("ProgramFiles") or r"C:\Program Files",
        os.environ.get("ProgramFiles(x86)") or r"C:\Program Files (x86)",
        os.environ.get("ProgramData") or r"C:\ProgramData",
    ]
    return tuple(c.rstrip("\\/").casefold() for c in candidates if c)


def _is_within(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
    except ValueError:
        return False
    return True


def broad_path_reason(path: Path) -> str | None:
    """Return why ``path`` is unsafe as a vault root, or ``None`` if acceptable.

    ``path`` should already be absolute and resolved.
    """
    home = Path.home().resolve()
    if path == Path(path.anchor):
        return "refusing a filesystem root"
    if path == home or path == home.parent:
        return "refusing a home directory or the directory that contains home directories"
    for child in _BROAD_HOME_CHILDREN:
        if path == home / child:
            return f"refusing the broad user directory ~/{child}; choose a dedicated vault folder"

    if os.name == "nt":
        folded = str(path).rstrip("\\/").casefold()
        for tree in _windows_system_trees():
            if folded == tree or folded.startswith(tree + "\\"):
                return "refusing a Windows system directory"
        return None

    for tree in _SYSTEM_TREES_POSIX:
        tree_path = Path(tree)
        if path == tree_path or _is_within(path, tree_path):
            # /Library is a system tree, but ~/Library is under home and is
            # handled above; only the root-level /Library matches here.
            return f"refusing a system directory ({tree})"
    for broad in _BROAD_DIRS_POSIX:
        if path == Path(broad):
            return f"refusing a broad shared directory ({broad})"
    return None


def authorized_root(raw_path: str | Path) -> Path:
    raw = str(raw_path).strip()
    if not raw:
        raise VaultError("an explicit PearlBook vault path is required")
    root = Path(raw).expanduser().resolve(strict=True)
    if not root.is_dir():
        raise VaultError("the authorized PearlBook vault is not a directory")
    reason = broad_path_reason(root)
    if reason:
        raise VaultError(reason)
    return root


def _is_hidden(relative: Path) -> bool:
    return any(part in EXCLUDED_PARTS or part.startswith(".") for part in relative.parts)


def _check_relative_input(relative_path: str) -> Path:
    candidate_input = Path(relative_path)
    if candidate_input.is_absolute() or ".." in candidate_input.parts:
        raise VaultError("note_path must be a vault-relative path")
    if _is_hidden(candidate_input):
        raise VaultError("hidden or application folders are outside the PearlBook scope")
    return candidate_input


def _safe_note(root: Path, relative_path: str) -> Path:
    candidate_input = _check_relative_input(relative_path)
    candidate = (root / candidate_input).resolve(strict=True)
    try:
        resolved_relative = candidate.relative_to(root)
    except ValueError as exc:
        raise VaultError("note path escapes the authorized vault") from exc
    if _is_hidden(resolved_relative):
        raise VaultError("hidden or application folders are outside the PearlBook scope")
    if candidate.suffix.lower() != ".md" or not candidate.is_file():
        raise VaultError("only existing Markdown notes can be read")
    if candidate.stat().st_size > MAX_NOTE_BYTES:
        raise VaultError("note exceeds the service size limit")
    return candidate


def _safe_write_target(root: Path, relative_path: str) -> Path:
    candidate_input = _check_relative_input(relative_path)
    if candidate_input.suffix.lower() != ".md":
        raise VaultError("only Markdown notes can be written")
    candidate = (root / candidate_input).resolve(strict=False)
    try:
        resolved_relative = candidate.relative_to(root)
    except ValueError as exc:
        raise VaultError("note path escapes the authorized vault") from exc
    if _is_hidden(resolved_relative):
        raise VaultError("hidden or application folders are outside the PearlBook scope")
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
        if _is_hidden(relative):
            continue
        try:
            resolved = path.resolve(strict=True)
            resolved_relative = resolved.relative_to(root)
        except (OSError, ValueError):
            continue
        if _is_hidden(resolved_relative):
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


def normalize_link_settings(style: str | None, base: str | None) -> tuple[str, str | None]:
    """Validate a link style and base URL.

    ``obsidian`` (default) returns native ``obsidian://`` URIs, ``path``
    returns no URL, and ``https_bridge`` is an explicit opt-in that sends the
    vault name and note path to the configured HTTPS redirector.
    """
    chosen = (style or "obsidian").strip()
    legacy_bridge = chosen == "obsid_net"
    chosen = LEGACY_LINK_STYLES.get(chosen, chosen)
    if chosen not in LINK_STYLES:
        raise VaultError(f"link style must be one of {', '.join(LINK_STYLES)}")
    if chosen != "https_bridge":
        return chosen, None
    if not base and legacy_bridge:
        base = "https://obsid.net/"
    parsed = urlparse(base or "")
    if parsed.scheme != "https" or not parsed.netloc:
        raise VaultError("https_bridge link style requires an HTTPS link base")
    return chosen, base.rstrip("/") + "/"


def obsidian_link(
    vault_name: str,
    relative_path: str,
    style: str = "obsidian",
    base: str | None = None,
) -> str | None:
    style, base = normalize_link_settings(style, base)
    vault_q = quote(vault_name, safe="")
    file_q = quote(relative_path, safe="")
    if style == "path":
        return None
    if style == "https_bridge":
        return f"{base}?vault={vault_q}&file={file_q}"
    return f"obsidian://open?vault={vault_q}&file={file_q}"


def content_sha256(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def _with_link(result: dict, vault_name: str, relative: str, style: str, base: str | None) -> dict:
    url = obsidian_link(vault_name, relative, style, base)
    if url:
        result["obsidian_url"] = url
    return result


def search_notes(
    root: Path,
    vault_name: str,
    query: str,
    limit: int = 10,
    link_style: str = "obsidian",
    link_base: str | None = None,
) -> dict:
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
                _with_link(
                    {
                        "title": title,
                        "note_path": relative,
                        "snippet": _snippet(text, needle),
                    },
                    vault_name,
                    relative,
                    link_style,
                    link_base,
                ),
            )
        )

    matches.sort(key=lambda item: (-item[0], item[1]["note_path"].casefold()))
    results = [item[1] for item in matches[:limit]]
    return {"query": needle, "count": len(results), "results": results}


def read_note(
    root: Path,
    vault_name: str,
    note_path: str,
    link_style: str = "obsidian",
    link_base: str | None = None,
) -> dict:
    path = _safe_note(root, note_path)
    content = path.read_text(encoding="utf-8")
    if len(content) > MAX_READ_CHARS:
        raise VaultError("note exceeds the response character limit")
    relative = path.relative_to(root).as_posix()
    return _with_link(
        {
            "title": path.stem,
            "note_path": relative,
            "content": content,
            "sha256": content_sha256(content),
        },
        vault_name,
        relative,
        link_style,
        link_base,
    )


def preview_write(
    root: Path,
    vault_name: str,
    note_path: str,
    content: str,
    expected_sha256: str,
    link_style: str = "obsidian",
    link_base: str | None = None,
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
    return _with_link(
        {
            "title": target.stem,
            "note_path": relative,
            "current_sha256": current_hash,
            "proposed_sha256": content_sha256(content),
            "diff": diff or "No changes.",
        },
        vault_name,
        relative,
        link_style,
        link_base,
    )


def apply_write(
    root: Path,
    vault_name: str,
    note_path: str,
    content: str,
    expected_sha256: str,
    link_style: str = "obsidian",
    link_base: str | None = None,
) -> dict:
    preview = preview_write(
        root, vault_name, note_path, content, expected_sha256, link_style, link_base
    )
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
