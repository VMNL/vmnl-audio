# Testing

## Audio tests

The root manifest registers two integration targets from `tests/audio/`:

| Command | Evidence |
| --- | --- |
| `cargo test --lib --locked` | Private worker lifecycle unit tests; no output device. |
| `cargo test --test audio --locked` | Public configuration/error contracts and private decoder, ring, mixer, playback and worker regressions; no output device. |
| `cargo test --test audio-backend --no-run --locked` | Compiles the native probes without opening a device. |
| `cargo test --test audio-backend --locked -- --ignored --test-threads=1` | Explicit native CPAL device execution. |
| `cargo test --doc --locked` | Public Rustdoc examples; device construction examples are compile-only. |

The deterministic suite includes the same production sources in a private harness.
Its relative paths stay inside this repository, and fixtures are found from the
root package's `CARGO_MANIFEST_DIR`. It does not widen the public API or replace
tests against the compiled public library.

Native probes require a usable stereo output route and must fail if setup fails.
Record the source SHA, OS, compiler, CPAL version, output route and resolved rate,
and initial mute/volume settings. Keep host audio settings fixed. Use an external
watchdog to bound a hung run; a timeout is a failure, not a shutdown guarantee.

Compilation and deterministic tests do not qualify listening quality, backend
disconnection/recovery, native shutdown latency, container padding/timing or
callback deadlines. Keep those results separate. See the
[acceptance contract](audio.md) for the behavioral invariants.
