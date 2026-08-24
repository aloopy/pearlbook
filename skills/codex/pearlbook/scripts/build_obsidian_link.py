#!/usr/bin/env python3
"""Build a chat-safe HTTPS link that opens a vault note in Obsidian."""

from __future__ import annotations

import argparse
from pathlib import PurePosixPath
from urllib.parse import quote, urlparse


def build_link(vault: str, note_path: str, title: str, base: str) -> str:
    if not vault.strip():
        raise ValueError("vault must not be empty")

    normalized = note_path.replace("\\", "/").strip()
    path = PurePosixPath(normalized)
    if not normalized or path.is_absolute() or ".." in path.parts:
        raise ValueError("file must be a safe vault-relative path")

    parsed = urlparse(base)
    if parsed.scheme != "https" or not parsed.netloc:
        raise ValueError("base must be an HTTPS URL")

    clean_base = base.rstrip("/") + "/"
    url = (
        f"{clean_base}?vault={quote(vault.strip(), safe='')}"
        f"&file={quote(normalized, safe='')}"
    )
    safe_title = title.replace("[", "\\[").replace("]", "\\]")
    return f"[Open “{safe_title}” in Obsidian]({url})"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--vault", required=True)
    parser.add_argument("--file", required=True, dest="note_path")
    parser.add_argument("--title", required=True)
    parser.add_argument("--base", default="https://obsid.net/")
    args = parser.parse_args()
    try:
        print(build_link(args.vault, args.note_path, args.title, args.base))
    except ValueError as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    main()
