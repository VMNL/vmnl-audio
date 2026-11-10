# Documentation maintenance and validation

Follow the single ordered contract in [CONTRIBUTING](../../../CONTRIBUTING.md#before-submission).
Prepare pinned tools explicitly through [build instructions](../../build.md).
Normal checks never install tools or rewrite tracked inventories.

For a public API change, update Rustdoc, canonical reference pages and the
[coverage matrix](coverage_matrix.md), then run `just docs-api-update`. Review
the [snapshot](public_api_snapshot.md), [symbols](../appendices/public_symbol_index.md)
and [methods](../appendices/method_index.md) before `just docs-api-check`.

`cargo-public-api 0.52.0` uses `nightly-2026-03-12` in the separate
`target/api-public-api` directory. Only blanket impls are omitted. Rustdoc JSON
item IDs determine public-path identity: root/audio reexports share a page, while
distinct types/aliases with the same leaf name never merge. Private implementation
module paths do not become invented public paths. Unsupported new exported item
kinds fail closed until tooling and docs are extended together.

The check rejects missing/stale matrix entries, absent pages/evidence/Rustdoc,
undocumented member identifiers, unresolved method owners, missing Rustdoc method
anchors and stale generated files. Tool tests exercise identity, module-only
exports, omissions, stale outputs and artifact link handling. Semantic accuracy
still requires reviewing prose against contracts/tests.

Snippets run through mdBook with the same compiler-built library used by the
regular checks; device construction blocks use `no_run`, not hidden native tests.
The snippet library directory selects `target/debug/libvmnl_audio.rlib` explicitly,
excluding stale crate rlibs/rmetas while retaining transitive dependencies. It
replaces only its own `target/api-book-libs` output, without cleaning Cargo caches.
Offline lychee checks local Markdown/HTML and fragments; it does not verify remote
website availability. mdBook uses `create-missing = false`.
Rustdoc source `#start-end` links are interpreted by Rustdoc JavaScript rather
than literal HTML IDs; the checker verifies every selected line ID separately
and excludes only those already-verified ranges from lychee's fragment lookup.

The build stages `target/documentation/index.html`, containing book, Rustdoc and
source evidence in a source-relative layout. Out-of-book Markdown guides remain
readable source files; links rewritten by mdBook to nonexistent HTML are restored
to those Markdown files. This generated directory is replaced by each build and
uploaded as one CI artifact. Nothing is deployed or published automatically.
