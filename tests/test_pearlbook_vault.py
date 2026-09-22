from __future__ import annotations

import asyncio
import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPTS = (
    Path(__file__).resolve().parents[1] / "skills" / "codex" / "pearlbook" / "scripts"
)
sys.path.insert(0, str(SCRIPTS))

from build_obsidian_link import build_link  # noqa: E402
from pearlbook_vault import (  # noqa: E402
    VaultError,
    apply_write,
    authorized_root,
    broad_path_reason,
    obsidian_link,
    preview_write,
    read_note,
    search_notes,
)

HAS_MCP = importlib.util.find_spec("mcp") is not None


class PearlBookVaultTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name).resolve()
        (self.root / "Topics").mkdir()
        (self.root / "Topics" / "Neuromuscular blockade.md").write_text(
            "# Neuromuscular blockade\n\nRocuronium reversal pearl.",
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_search_and_read_known_note(self) -> None:
        root = authorized_root(self.root)
        found = search_notes(root, "PearlBook", "rocuronium")
        self.assertEqual(found["count"], 1)
        note_path = found["results"][0]["note_path"]
        note = read_note(root, "PearlBook", note_path)
        self.assertEqual(note["title"], "Neuromuscular blockade")
        self.assertIn("Rocuronium", note["content"])

    def test_rejects_traversal_and_absolute_paths(self) -> None:
        root = authorized_root(self.root)
        for unsafe in ("../outside.md", "/tmp/outside.md"):
            with self.subTest(unsafe=unsafe), self.assertRaises(VaultError):
                read_note(root, "PearlBook", unsafe)

    def test_rejects_symlink_escape(self) -> None:
        outside = self.root.parent / "outside-pearlbook-test.md"
        outside.write_text("not authorized", encoding="utf-8")
        link = self.root / "Topics" / "escape.md"
        try:
            link.symlink_to(outside)
            with self.assertRaises(VaultError):
                read_note(authorized_root(self.root), "PearlBook", "Topics/escape.md")
        finally:
            outside.unlink(missing_ok=True)

    def test_preview_then_apply_update_with_conflict_detection(self) -> None:
        root = authorized_root(self.root)
        note_path = "Topics/Neuromuscular blockade.md"
        current = read_note(root, "PearlBook", note_path)
        proposed = current["content"] + "\nReview sugammadex dosing.\n"
        preview = preview_write(
            root, "PearlBook", note_path, proposed, current["sha256"]
        )
        self.assertIn("+Review sugammadex dosing.", preview["diff"])
        self.assertNotIn("Review sugammadex dosing.", current["content"])

        result = apply_write(
            root, "PearlBook", note_path, proposed, current["sha256"]
        )
        self.assertTrue(result["applied"])
        updated = read_note(root, "PearlBook", note_path)
        self.assertIn("Review sugammadex dosing.", updated["content"])

        with self.assertRaises(VaultError):
            apply_write(root, "PearlBook", note_path, "stale write", current["sha256"])

    def test_create_requires_new_sentinel_and_existing_parent(self) -> None:
        root = authorized_root(self.root)
        with self.assertRaises(VaultError):
            preview_write(
                root,
                "PearlBook",
                "Missing/New pearl.md",
                "# New pearl\n",
                "new",
            )

        (self.root / "Pearls").mkdir()
        result = apply_write(
            root, "PearlBook", "Pearls/New pearl.md", "# New pearl\n", "new"
        )
        self.assertTrue(result["applied"])


class HiddenPathTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name).resolve()
        for folder in (".trash", ".obsidian", ".git", "Topics"):
            (self.root / folder).mkdir()
        (self.root / ".trash" / "deleted.md").write_text("# deleted secret", encoding="utf-8")
        (self.root / ".obsidian" / "note.md").write_text("# config", encoding="utf-8")

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_hidden_paths_are_not_readable(self) -> None:
        root = authorized_root(self.root)
        for hidden in (".trash/deleted.md", ".obsidian/note.md", "Topics/../.trash/deleted.md"):
            with self.subTest(hidden=hidden), self.assertRaises(VaultError):
                read_note(root, "PearlBook", hidden)

    def test_hidden_paths_are_not_writable(self) -> None:
        root = authorized_root(self.root)
        for hidden in (".obsidian/new.md", ".git/new.md", ".trash/deleted.md", ".hidden.md"):
            with self.subTest(hidden=hidden), self.assertRaises(VaultError):
                preview_write(root, "PearlBook", hidden, "x", "new")
        self.assertFalse((self.root / ".obsidian" / "new.md").exists())

    def test_symlink_into_hidden_folder_is_rejected(self) -> None:
        (self.root / "Topics" / "alias.md").symlink_to(self.root / ".trash" / "deleted.md")
        root = authorized_root(self.root)
        with self.assertRaises(VaultError):
            read_note(root, "PearlBook", "Topics/alias.md")
        self.assertEqual(search_notes(root, "PearlBook", "deleted")["count"], 0)


class VaultRootTests(unittest.TestCase):
    def test_refuses_system_and_broad_directories(self) -> None:
        home = Path.home().resolve()
        unsafe = [
            Path("/"),
            Path("/etc"),
            Path("/etc/pearlbook"),
            Path("/usr/local/share"),
            Path("/bin"),
            Path("/var"),
            Path("/tmp"),
            Path("/System/Library"),
            Path("/Library/Application Support"),
            Path("/home"),
            Path("/Users"),
            home,
            home / "Documents",
            home / "Library",
        ]
        for path in unsafe:
            with self.subTest(path=str(path)):
                self.assertIsNotNone(broad_path_reason(path))

    def test_allows_dedicated_vault_folders(self) -> None:
        home = Path.home().resolve()
        for path in (home / "Documents" / "PearlBook", home / "PearlBookHeadless"):
            with self.subTest(path=str(path)):
                self.assertIsNone(broad_path_reason(path))
        with tempfile.TemporaryDirectory() as temp:
            self.assertEqual(authorized_root(temp), Path(temp).resolve())

    def test_authorized_root_refuses_etc(self) -> None:
        with self.assertRaises(VaultError):
            authorized_root("/etc")


class LinkTests(unittest.TestCase):
    def test_default_link_is_native_obsidian_uri(self) -> None:
        url = obsidian_link("My Vault", "Topics/DKA.md")
        self.assertEqual(url, "obsidian://open?vault=My%20Vault&file=Topics%2FDKA.md")

    def test_https_bridge_is_opt_in_and_uses_configured_base(self) -> None:
        with self.assertRaises(VaultError):
            obsidian_link("V", "a.md", "https_bridge", None)
        with self.assertRaises(VaultError):
            obsidian_link("V", "a.md", "https_bridge", "http://insecure.example")
        url = obsidian_link("V", "a.md", "https_bridge", "https://links.example.org")
        self.assertEqual(url, "https://links.example.org/?vault=V&file=a.md")

    def test_path_style_omits_url(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = authorized_root(temp)
            (root / "a.md").write_text("hello", encoding="utf-8")
            note = read_note(root, "V", "a.md", link_style="path")
            self.assertNotIn("obsidian_url", note)

    def test_build_link_defaults_to_obsidian_uri(self) -> None:
        self.assertIn("(obsidian://open?vault=V&file=Topics%2FA.md)", build_link("V", "Topics/A.md", "A"))
        self.assertIn(
            "(https://x.example/?vault=V&file=A.md)",
            build_link("V", "A.md", "A", "https://x.example"),
        )


class SetupScriptTests(unittest.TestCase):
    SCRIPT = SCRIPTS / "setup_pearlbook.py"

    def run_setup(self, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, str(self.SCRIPT), *args],
            stdin=subprocess.DEVNULL,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_non_interactive_without_path_fails_cleanly(self) -> None:
        result = self.run_setup("--dry-run")
        self.assertEqual(result.returncode, 2)
        self.assertIn("--existing PATH", result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_refuses_system_directory(self) -> None:
        result = self.run_setup("--existing", "/etc", "--dry-run")
        self.assertEqual(result.returncode, 2)

    def test_create_writes_agents_md_and_obsidian_link_style(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            vault = Path(temp) / "PearlBook"
            config = Path(temp) / "config" / "local-config.md"
            result = self.run_setup("--create", str(vault), "--yes", "--config", str(config))
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((vault / "AGENTS.md").is_file())
            self.assertFalse((vault / "CLAUDE.md").exists())
            text = config.read_text(encoding="utf-8")
            self.assertIn("link_style: obsidian", text)
            self.assertNotIn("obsid.net", text)


@unittest.skipUnless(HAS_MCP, "mcp package not installed")
class McpAnnotationTests(unittest.TestCase):
    def test_apply_write_is_marked_destructive(self) -> None:
        from pearlbook_mcp import build_server

        with tempfile.TemporaryDirectory() as temp:
            server = build_server(Path(temp).resolve(), "PearlBook")
            tools = {tool.name: tool for tool in asyncio.run(server.list_tools())}
        self.assertTrue(tools["pearlbook_apply_write"].annotations.destructiveHint)
        self.assertFalse(tools["pearlbook_apply_write"].annotations.readOnlyHint)
        for name in ("pearlbook_search", "pearlbook_read", "pearlbook_preview_write"):
            self.assertTrue(tools[name].annotations.readOnlyHint)


if __name__ == "__main__":
    unittest.main()
