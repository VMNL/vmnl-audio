# vmnl_audio agent rules

Read closer rules, inspect `git status`, and preserve unrelated changes before editing.
Read [documentation](docs/README.md), [coding rules](docs/INSTRUCTIONS.md), and the
[architecture](docs/architecture.md) for architecture/API changes. Classify the task
as Feature, Fix, Maintenance or Read-only; inspection alone never authorizes writes.

Keep this a standalone audio package. Clients depend on `vmnl_audio` directly.
CPAL is private. Do not introduce a facade, graphics dependency, public backend
types, automatic worker default, or dependency upgrade as part of unrelated work.
Rustdoc owns local public contracts; [docs/audio.md](docs/audio.md) owns technical
acceptance invariants. Report contradictions instead of silently choosing a contract.

Keep patches scoped. Reproduce fixes with focused regressions and test changed
observable contracts. Preserve SPDX and `// SAFETY:` invariants. Never manually
edit generated inventories or Cargo.lock. Assess Rustdoc, book, guides, examples,
navigation and release-note impacts; explain when documentation needs no update.

Use the single ordered completion contract in [CONTRIBUTING.md](CONTRIBUTING.md#before-submission).
Tool preparation is explicit; checks must not install tools or rewrite inventories.
Native probes are opt-in. Distinguish compilation, deterministic tests, native
execution, listening and realtime measurements; none substitutes for another.

Do not install host packages, use sudo, change host audio settings, delete unrelated
build outputs, or invoke workspace-wide fixes without authorization. Documentation
builds may replace their own `target/api-book`, `target/api-book-libs` and
`target/documentation` outputs.
Do not push, edit GitHub, merge, publish or create releases/tags without explicit
authorization. Existing session authorization remains valid. Releases are manual;
follow [deployment](docs/deployment.md). Before the first public release, add no
per-change changelog entries. Prepare PR descriptions only when requested, using
the [contribution template](CONTRIBUTING.md#pull-request-descriptions).
