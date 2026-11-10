# SPDX-FileCopyrightText: 2026 VMNL contributors
# SPDX-License-Identifier: MIT

"""Contract regressions for alias identity, coverage and stale-file detection."""

import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest

SPEC = importlib.util.spec_from_file_location("api_docs", Path(__file__).parents[1] / "api_docs.py")
api = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = api
SPEC.loader.exec_module(api)


def item(inner, name=None, visibility="public"):
    return {"crate_id": 0, "name": name, "visibility": visibility, "inner": inner}


def graph():
    return {"format_version": 57, "root": 0, "index": {
        "0": item({"module": {"items": [1, 3, 4]}}),
        "1": item({"module": {"items": [2]}}, "audio"),
        "2": item({"use": {"id": 5, "name": "Sound", "is_glob": False}}),
        "3": item({"use": {"id": 5, "name": "Sound", "is_glob": False}}),
        "4": item({"struct": {}}, "Hidden", "default"),
        "5": item({"struct": {}}, "Sound"),
    }}


class IdentityTests(unittest.TestCase):
    def test_reexports_share_identity_and_private_items_are_not_public(self):
        self.assertEqual(api.public_paths(graph()), {
            "vmnl_audio::audio::Sound": "vmnl_audio::Sound", "vmnl_audio::Sound": "vmnl_audio::Sound"})

    def test_distinct_same_name_type_is_never_merged(self):
        doc = graph()
        doc["index"]["2"]["inner"]["use"]["id"] = 6
        doc["index"]["6"] = item({"struct": {}}, "Sound")
        self.assertEqual(api.public_paths(doc)["vmnl_audio::audio::Sound"], "vmnl_audio::audio::Sound")

    def test_module_only_export_does_not_invent_a_root_alias(self):
        doc = graph()
        doc["index"]["0"]["inner"]["module"]["items"] = [1]
        self.assertEqual(api.public_paths(doc), {"vmnl_audio::audio::Sound": "vmnl_audio::audio::Sound"})

    def test_real_type_alias_has_its_own_identity(self):
        doc = graph()
        doc["index"]["0"]["inner"]["module"]["items"].append(6)
        doc["index"]["6"] = item({"type_alias": {}}, "SoundAlias")
        self.assertEqual(api.public_paths(doc)["vmnl_audio::SoundAlias"], "vmnl_audio::SoundAlias")

    def test_unresolved_and_new_export_kinds_fail_closed(self):
        doc = graph()
        doc["index"]["2"]["inner"]["use"]["id"] = None
        with self.assertRaisesRegex(api.ApiDocsError, "unresolved"):
            api.public_paths(doc)
        doc = graph()
        doc["index"]["5"]["inner"] = {"function": {}}
        with self.assertRaisesRegex(api.ApiDocsError, "unsupported exported item"):
            api.public_paths(doc)

    def test_methods_follow_the_exported_owner_identity(self):
        surface = api.parse_surface(
            "pub struct vmnl_audio::audio::Sound\npub fn vmnl_audio::Sound::play(&self)\n",
            api.public_paths(graph()))
        self.assertEqual(surface.items, (api.PublicItem("struct", "vmnl_audio::Sound"),))
        self.assertEqual(surface.methods, (api.PublicMethod("vmnl_audio::Sound", "play"),))

    def test_unresolved_method_and_unknown_inventory_fail(self):
        for text, message in [("pub fn vmnl_audio::Missing::play(&self)", "owning exported item"),
                              ("pub bewildering vmnl_audio::Thing", "unknown")]:
            with self.assertRaisesRegex(api.ApiDocsError, message):
                api.parse_surface(text, api.public_paths(graph()))

    def test_missing_export_in_text_fails(self):
        aliases = {"vmnl_audio::Sound": "vmnl_audio::Sound", "vmnl_audio::Music": "vmnl_audio::Music"}
        with self.assertRaisesRegex(api.ApiDocsError, "absent from text"):
            api.parse_surface("pub struct vmnl_audio::Sound\n", aliases)


class CoverageTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.item = api.PublicItem("struct", "vmnl_audio::Sound")
        self.row = api.CoverageRow(self.item, "sound.md", "sound.html", "tests.rs")
        self.surface = api.Surface("surface\n", (self.item,), (api.PublicMethod(self.item.symbol, "play"),),
                                   (), {self.item.symbol: self.item.symbol})
        (self.root / "sound.md").write_text("# Sound\n`play` starts playback.\n")
        (self.root / "sound.html").write_text('<section id="method.play"></section>')
        (self.root / "tests.rs").write_text("// evidence\n")
        self.matrix = self.root / "coverage.md"

    def validate(self, surface=None, rows=None):
        api.validate_coverage(surface or self.surface, rows if rows is not None else (self.row,), self.matrix)

    def test_valid_coverage(self):
        self.validate()

    def test_missing_or_stale_matrix_entries_fail(self):
        with self.assertRaisesRegex(api.ApiDocsError, "coverage mismatch"):
            self.validate(rows=())
        other = api.CoverageRow(api.PublicItem("enum", "vmnl_audio::Other"), "a", "b", "c")
        with self.assertRaisesRegex(api.ApiDocsError, "stale="):
            self.validate(rows=(self.row, other))

    def test_missing_evidence_or_rustdoc_fails(self):
        for name in ("tests.rs", "sound.html"):
            path = self.root / name
            original = path.read_text()
            path.unlink()
            with self.assertRaisesRegex(api.ApiDocsError, "missing coverage target"):
                self.validate()
            path.write_text(original)

    def test_missing_method_or_field_documentation_fails(self):
        (self.root / "sound.md").write_text("# Sound\n")
        with self.assertRaisesRegex(api.ApiDocsError, "undocumented.*play"):
            self.validate()
        surface = api.Surface("surface\n", (self.item,), (), (api.PublicMethod(self.item.symbol, "volume"),), {})
        with self.assertRaisesRegex(api.ApiDocsError, "undocumented.*volume"):
            self.validate(surface)

    def test_missing_rustdoc_anchor_fails(self):
        (self.root / "sound.html").write_text("<main></main>")
        with self.assertRaisesRegex(api.ApiDocsError, "method anchor"):
            self.validate()

    def test_stale_output_fails_without_rewriting(self):
        path = self.root / "snapshot.md"
        path.write_text("old\n")
        with self.assertRaisesRegex(api.ApiDocsError, "stale generated"):
            api.verify_outputs({path: "new\n"})
        self.assertEqual(path.read_text(), "old\n")
        api.verify_outputs({path: "old\n"})

    def test_duplicate_matrix_rows_fail(self):
        row = "| struct | `vmnl_audio::Sound` | [Sound](sound.md) | [Rustdoc](sound.html) | [Test](tests.rs) |\n"
        self.matrix.write_text("| Kind | Symbol | Canonical page | Rustdoc | Evidence |\n|---|---|---|---|---|\n" + row * 2)
        with self.assertRaisesRegex(api.ApiDocsError, "duplicate"):
            api.parse_matrix(self.matrix)


if __name__ == "__main__":
    unittest.main()
