#!/usr/bin/env python3
"""Report readiness for a private PearlBook Headless Sync host."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path


def command_version(command: str, *args: str) -> tuple[bool, str]:
    executable = shutil.which(command)
    if not executable:
        return False, "not found"
    try:
        completed = subprocess.run(
            [executable, *args],
            check=False,
            capture_output=True,
            text=True,
            timeout=10,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return False, str(exc)
    output = (completed.stdout or completed.stderr).strip().splitlines()
    summary = output[0] if output else f"exit {completed.returncode}"
    return completed.returncode == 0, summary


def node_major(version: str) -> int | None:
    token = version.strip().lstrip("v").split(".", 1)[0]
    return int(token) if token.isdigit() else None


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--vault", type=Path, required=True)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()

    node_ok, node_version = command_version("node", "--version")
    major = node_major(node_version) if node_ok else None
    checks = {
        "python_3_10_or_later": {
            "ok": sys.version_info >= (3, 10),
            "detail": sys.version.split()[0],
        },
        "node_22_or_later": {
            "ok": bool(node_ok and major is not None and major >= 22),
            "detail": node_version,
        },
        "npm": dict(zip(("ok", "detail"), command_version("npm", "--version"))),
        "obsidian_headless": dict(
            zip(("ok", "detail"), command_version("ob", "--version"))
        ),
        "tunnel_client": dict(
            zip(("ok", "detail"), command_version("tunnel-client", "--version"))
        ),
    }

    vault = args.vault.expanduser().resolve(strict=False)
    checks["vault_directory"] = {
        "ok": vault.is_dir(),
        "detail": str(vault),
    }

    if args.as_json:
        print(json.dumps({"vault": str(vault), "checks": checks}, indent=2))
        return

    print("PearlBook headless readiness")
    for name, result in checks.items():
        label = "READY" if result["ok"] else "TODO"
        print(f"[{label}] {name}: {result['detail']}")
    print("\nThis check does not validate Obsidian credentials, Sync health, backups, or")
    print("ChatGPT workspace/tunnel permissions. Complete those interactively.")


if __name__ == "__main__":
    main()
