# Examples

| Cargo example | Behavior | Control mode |
|---|---|---|
| `play_sound` | Decode/cache and play the 200 ms effect once; wait for Enter/EOF. | Explicit automatic worker |
| `stream_music` | Stream the 8 s track; wait for Enter/EOF. | Explicit automatic worker |
| `playback_controls` | Pause, resume, instance volume, music-bus mute, looping, stop and replay. | Explicit automatic worker |
| `manual_control` | Drive refill/cleanup in a control loop until Enter/EOF or completion. | Explicit manual |

Each accepts `--help` before any device construction and an optional filename:

```sh
cargo run --example stream_music --locked -- /path/to/track.flac
cargo run --example playback_controls --locked -- --help
```

The interactive commands are `pause`, `resume`, `volume 0.5`, `mute`, `unmute`,
`loop on`, `loop off`, `stop`, `play`, `status` and `quit`. `play` stops the previous
instance and creates a new handle; `resume` cannot restart a stopped instance.
Mute belongs to the music bus and therefore persists across replay. Instance
volume and loop settings are copied into each new playback configuration.

Synchronous errors propagate to `main`. All programs consult the shared last-error
slot after control work and before exit. Automatic examples block on stdin; they
do not continuously inspect errors during that wait. Interactive diagnostics are
checked after each command. Applications can integrate diagnostic polling into
their own event loop without taking ownership of refill work.

The manual example uses a separate stdin thread so blocking input cannot starve
refill. It does not join a reader still blocked when the track ends; process exit
ends that example-only thread. Its 5 ms sleep is illustrative pacing, with no
universal streaming/deadline guarantee. The three automatic examples need neither
`update()` nor sleep for refill.

Assets resolve from the package's `CARGO_MANIFEST_DIR`, independently of the
working directory. [Generation and MIT licensing](../examples/assets/README.md)
are documented beside the files. Regeneration is explicit:

```sh
python3 tools/generate_example_audio.py
python3 tools/generate_example_audio.py --check
```

The generator uses standard-library Python and integer triangle waves/envelopes.
Tests verify exact regeneration and PCM shape/duration; `--help` checks and
compilation do not qualify audible playback.
