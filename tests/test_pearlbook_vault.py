from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path


SCRIPTS = (
    Path(__file__).resolve().parents[1] / "skills" / "codex" / "pearlbook" / "scripts"
)
sys.path.insert(0, str(SCRIPTS))

from pearlbook_vault import (
    VaultError,
    apply_write,
    authorized_root,
    preview_write,
    read_note,
    search_notes,
)


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


if __name__ == "__main__":
    unittest.main()
