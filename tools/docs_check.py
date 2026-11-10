#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 VMNL contributors
# SPDX-License-Identifier: MIT

"""Non-mutating source checks; generated build outputs stay under target/."""

from pathlib import Path
from html.parser import HTMLParser
import json
import os
import re
import shutil
import subprocess
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
VERSIONS = {"just": "just 1.57.0", "mdbook": "mdbook v0.5.4", "lychee": "lychee 0.24.2"}


def require_tools() -> None:
    for name, expected in VERSIONS.items():
        actual = subprocess.check_output([name, "--version"], text=True).splitlines()[0].strip()
        if actual != expected:
            raise RuntimeError(f"expected {expected}, got {actual}; see docs/build.md")


def repair_source_links(content: str, page: Path, site: Path) -> str:
    """mdBook changes .md to .html even for source guides outside its SUMMARY."""
    def replace(match: re.Match) -> str:
        url = urlsplit(html_unescape(match[2]))
        if url.scheme or url.netloc or not url.path.endswith(".html"):
            return match[0]
        target = (page.parent / unquote(url.path)).resolve()
        if not target.is_relative_to(site.resolve()):
            raise RuntimeError(f"documentation link escapes the artifact: {page}: {url.path}")
        if not target.exists() and target.with_suffix(".md").is_file():
            return match[1] + match[2].replace(".html", ".md", 1) + match[3]
        return match[0]
    return re.sub(r'(href=")([^"<>]+)(")', replace, content)


def html_unescape(value: str) -> str:
    import html
    return html.unescape(value)


def stage_site(target: Path) -> Path:
    site = target / "documentation"
    if site.exists():
        shutil.rmtree(site)  # Only this builder's documented staging output.
    site.mkdir(parents=True, exist_ok=True)
    # Preserve the source-relative layout used by the book's Rustdoc/evidence links.
    for directory in ("docs", "src", "tests", "examples"):
        shutil.copytree(ROOT / directory, site / directory, dirs_exist_ok=True,
                        ignore=shutil.ignore_patterns("__pycache__"))
    for name in ("README.md", "CONTRIBUTING.md", "AGENTS.md", "LICENSE", "Cargo.toml", "Justfile"):
        shutil.copy2(ROOT / name, site / name)
    shutil.copytree(target / "api-book", site / "docs/api", dirs_exist_ok=True)
    shutil.copytree(target / "doc", site / "target/doc", dirs_exist_ok=True)
    (site / "target/doc/index.html").write_text(
        '<!doctype html><html lang="en"><meta charset="utf-8"><title>Rustdoc</title>'
        '<a href="vmnl_audio/index.html">vmnl_audio Rustdoc</a></html>\n', encoding="utf-8")
    for page in (site / "docs/api").rglob("*.html"):
        page.write_text(repair_source_links(page.read_text(encoding="utf-8"), page, site), encoding="utf-8")
    (site / "index.html").write_text(
        '<!doctype html><html lang="en"><meta charset="utf-8"><title>vmnl_audio documentation</title>'
        '<h1>vmnl_audio</h1><ul><li><a href="docs/api/index.html">API book</a></li>'
        '<li><a href="target/doc/vmnl_audio/index.html">Rustdoc</a></li></ul></html>\n', encoding="utf-8")
    return site


class HtmlLinks(HTMLParser):
    def __init__(self, content: str):
        super().__init__()
        self.links, self.ids = [], set()
        self.feed(content)

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if values.get("href"):
            self.links.append(values["href"])
        if values.get("id"):
            self.ids.add(values["id"])


def validate_rustdoc_ranges(site: Path) -> str:
    """Rustdoc's JS interprets #start-end; these are not literal HTML IDs."""
    source_root = (site / "target/doc/src").resolve()
    known_ids, count = {}, 0
    for page in site.rglob("*.html"):
        for link in HtmlLinks(page.read_text(encoding="utf-8")).links:
            url = urlsplit(link)
            bounds = re.fullmatch(r"([0-9]+)-([0-9]+)", url.fragment)
            if url.scheme or url.netloc or not bounds:
                continue
            target = (page.parent / unquote(url.path)).resolve() if url.path else page.resolve()
            if not target.is_relative_to(source_root):
                continue
            if not target.is_file():
                raise RuntimeError(f"missing Rustdoc range target: {target}")
            if target not in known_ids:
                known_ids[target] = HtmlLinks(target.read_text(encoding="utf-8")).ids
            start, end = map(int, bounds.groups())
            if start > end or any(str(line) not in known_ids[target] for line in range(start, end + 1)):
                raise RuntimeError(f"invalid Rustdoc source range: {target}#{url.fragment}")
            count += 1
    print(f"Rustdoc source ranges: {count} verified against actual line IDs")
    return re.escape(str(source_root)) + r"/.*\.rs\.html#[0-9]+-[0-9]+$"


def markdown_files(root: Path) -> list[str]:
    files = sorted(path for path in root.rglob("*.md")
                   if "target" not in path.relative_to(root).parts and ".git" not in path.relative_to(root).parts)
    if not files:
        raise RuntimeError("empty Markdown inventory")
    return [str(path) for path in files]


def book_library_directory(target: Path) -> Path:
    directory = target / "api-book-libs"
    library = target / "debug/libvmnl_audio.rlib"
    if not library.is_file():
        raise RuntimeError("missing current library; run just build before documentation checks")
    if directory.exists():
        shutil.rmtree(directory)
    directory.mkdir()
    for artifact in (target / "debug/deps").iterdir():
        if artifact.is_file() and not artifact.name.startswith("libvmnl_audio-"):
            (directory / artifact.name).symlink_to(artifact.resolve())
    (directory / "libvmnl_audio.rlib").symlink_to(library.resolve())
    return directory


def main() -> None:
    os.chdir(ROOT)
    require_tools()
    metadata = json.loads(subprocess.check_output(["cargo", "metadata", "--no-deps", "--format-version", "1"], text=True))
    target = Path(metadata["target_directory"])
    if target != ROOT / "target":
        raise RuntimeError("documentation tooling requires the repository-local target/ directory")
    subprocess.run(["python3", "tools/api_docs.py", "check"], check=True)
    libraries = book_library_directory(target)
    subprocess.run(["mdbook", "test", "docs/api", "-L", str(libraries)], check=True)
    subprocess.run(["mdbook", "build", "docs/api"], check=True)
    subprocess.run(["lychee", "--offline", "--include-fragments=full", *markdown_files(ROOT)], check=True)
    site = stage_site(target)
    range_pattern = validate_rustdoc_ranges(site)
    subprocess.run(["lychee", "--offline", "--include-fragments=full", "--root-dir", str(site),
                    "--exclude", range_pattern, str(site)], check=True)
    print(f"Documentation artifact: {site}/index.html")


if __name__ == "__main__":
    main()
