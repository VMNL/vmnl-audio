# Getting started

Install [build prerequisites](build.md). No public release has been prepared yet;
from a neighboring development application, add the checkout directly:

```toml
[dependencies]
vmnl_audio = { path = "../vmnl-audio" }
```

Import `vmnl_audio::{AudioDevice, Sound, Music}` directly. No other VMNL package
or parent workspace is needed. Start with [automatic playback](api/workflows/first_sound.md)
and keep `AudioDevice` alive for the duration of playback. Automatic control is
an explicit `.thread(true)` choice; the library default remains manual.

Run a bundled example from the repository root:

```sh
cargo run --example play_sound --locked
cargo run --example stream_music --locked
cargo run --example playback_controls --locked
cargo run --example manual_control --locked -- --help
```

Examples use original synthetic WAVs and accept an optional source path after
`--`. Enter or stdin EOF exits; the interactive example also accepts `quit`.
`--help` never opens a device. Actual playback needs a usable native audio route.
See [example controls and error handling](examples.md).
