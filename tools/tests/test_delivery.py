# SPDX-FileCopyrightText: 2026 VMNL contributors
# SPDX-License-Identifier: MIT

import importlib.util
from pathlib import Path
import tempfile
import unittest


def load(name):
    spec = importlib.util.spec_from_file_location(name, Path(__file__).parents[1] / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


docs = load("docs_check")
package = load("check_package")


class ArtifactTests(unittest.TestCase):
    def test_rustdoc_js_ranges_validate_actual_source_lines(self):
        with tempfile.TemporaryDirectory() as directory:
            site = Path(directory)
            source = site / "target/doc/src/audio.rs.html"
            source.parent.mkdir(parents=True)
            source.write_text('<a id=2></a><a id=3></a><a id=4></a>')
            page = site / "index.html"
            page.write_text('<a href="target/doc/src/audio.rs.html#2-4">source</a>')
            docs.validate_rustdoc_ranges(site)
            page.write_text('<a href="target/doc/src/audio.rs.html#2-5">source</a>')
            with self.assertRaisesRegex(RuntimeError, "invalid Rustdoc source range"):
                docs.validate_rustdoc_ranges(site)

    def test_book_uses_only_current_crate_artifact_without_cleaning_cargo(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            deps = target / "debug/deps"
            deps.mkdir(parents=True)
            current = target / "debug/libvmnl_audio.rlib"
            current.write_text("current")
            stale = deps / "libvmnl_audio-old.rlib"
            stale.write_text("old")
            (deps / "libvmnl_audio-check.rmeta").write_text("metadata")
            (deps / "libdependency.rlib").write_text("dependency")
            libraries = docs.book_library_directory(target)
            self.assertEqual(sorted(path.name for path in libraries.iterdir()),
                             ["libdependency.rlib", "libvmnl_audio.rlib"])
            self.assertEqual((libraries / "libvmnl_audio.rlib").read_text(), "current")
            self.assertEqual(stale.read_text(), "old")

    def test_external_guide_link_is_repaired_and_rustdoc_is_preserved(self):
        with tempfile.TemporaryDirectory() as directory:
            site = Path(directory)
            page = site / "docs/api/concepts/page.html"
            page.parent.mkdir(parents=True)
            (site / "docs/audio.md").write_text("# Contract\n")
            before = '<a href="../../audio.html#scope">contract</a><a href="../../../target/doc/vmnl_audio/index.html">Rustdoc</a>'
            self.assertEqual(docs.repair_source_links(before, page, site), before.replace("audio.html", "audio.md"))

    def test_artifact_relative_link_cannot_escape(self):
        with tempfile.TemporaryDirectory() as directory:
            site = Path(directory)
            with self.assertRaisesRegex(RuntimeError, "escapes"):
                docs.repair_source_links('<a href="../../elsewhere.html">x</a>', site / "index.html", site)

    def test_markdown_discovery_handles_spaces_and_excludes_build_outputs(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "with spaces.md").write_text("# Guide\n")
            (root / "target").mkdir()
            (root / "target/generated.md").write_text("# Output\n")
            self.assertEqual(docs.markdown_files(root), [str(root / "with spaces.md")])

    def test_empty_markdown_inventory_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(RuntimeError, "empty"):
                docs.markdown_files(Path(directory))


class PackageTests(unittest.TestCase):
    def test_requires_assets_and_fixtures(self):
        with self.assertRaisesRegex(ValueError, "missing="):
            package.validate_files({"src/lib.rs"})

    def test_forbids_build_outputs(self):
        with self.assertRaisesRegex(ValueError, "target/leak"):
            package.validate_files(package.REQUIRED | {"target/leak"})

    def test_required_inventory_passes(self):
        package.validate_files(package.REQUIRED)


if __name__ == "__main__":
    unittest.main()
