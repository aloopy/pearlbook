#!/usr/bin/env python3
"""Build a Markdown link that opens a vault note in Obsidian.

By default the link is a native ``obsidian://`` URI, which stays on the user's
device. Pass ``--base`` to opt into an HTTPS redirector (for chat surfaces that
do not make ``obsidian://`` links clickable). A redirector receives the vault
name and note path in every request, so use one you trust or host yourself.
"""

from __future__ import annotations

import argparse
from pathlib import PurePosixPath
from urllib.parse import quote, urlparse


def build_link(vault: str, note_path: str, title: str, base: str | None = None) -> str:
    if not vault.strip():
        raise ValueError("vault must not be empty")

    normalized = note_path.replace("\\", "/").strip()
    path = PurePosixPath(normalized)
    if not normalized or path.is_absolute() or ".." in path.parts:
        raise ValueError("file must be a safe vault-relative path")

    vault_q = quote(vault.strip(), safe="")
    file_q = quote(normalized, safe="")
    if base:
        parsed = urlparse(base)
        if parsed.scheme != "https" or not parsed.netloc:
            raise ValueError("base must be an HTTPS URL")
        url = f"{base.rstrip('/')}/?vault={vault_q}&file={file_q}"
    else:
        url = f"obsidian://open?vault={vault_q}&file={file_q}"
    safe_title = title.replace("[", "\\[").replace("]", "\\]")
    return f"[Open “{safe_title}” in Obsidian]({url})"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n", 1)[0])
    parser.add_argument("--vault", required=True)
    parser.add_argument("--file", required=True, dest="note_path")
    parser.add_argument("--title", required=True)
    parser.add_argument(
        "--base",
        default=None,
        help="optional HTTPS redirector base URL (opt-in); omit for obsidian:// links",
    )
    args = parser.parse_args()
    try:
        print(build_link(args.vault, args.note_path, args.title, args.base))
    except ValueError as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    main()
