# Music

## Role and public paths

`vmnl_audio::Music`, also under `audio`, is a reusable streaming source created by
`AudioDevice::load_music`. Experimental;
[Rustdoc](../../../target/doc/vmnl_audio/audio/struct.Music.html).

## Public API and validation

Private fields. `play` starts an independent instance with defaults;
`play_with_config` uses a validated `MusicPlayConfig`. `path` returns the supplied
path without canonicalization. Derived `Clone` (`clone`) shares path/runtime.
No public constructor or `Default`.

## Ownership, costs and errors

Loading opens/checks initial metadata without validating the whole track. Every
play reopens the source, allocates its own decoder/PCM ring and prefills before
registration; file I/O and decoding can block the caller. Plays have independent
cursors. Handles do not keep native output alive; dropping a handle alone does not
stop playback. Source files must remain available for new plays and loop reopens.

Play can fail before registration on invalid gain, file/decoder errors, unsupported
metadata or active-list lock errors. Late refill can fail after successful load/play.
Detected OGG-chain rate/channel changes are unsupported; non-finite WAV PCM is
rejected. Manual update returns the refill failure; automatic failure stops the
worker and reports a diagnostic. See [error recovery](../concepts/errors_and_costs.md).

## Example and evidence

```rust,no_run
# extern crate vmnl_audio;
# fn main() -> vmnl_audio::AudioResult<()> {
let audio = vmnl_audio::AudioDevice::builder().thread(true).build()?;
let track = audio.load_music("examples/assets/music.wav")?;
let handle = track.play()?;
handle.stop();
# Ok(())
# }
```

Related: [MusicHandle](music_handle.md), [streaming](../workflows/stream_music.md).
Evidence: [decoding](../../../tests/audio/decoding.rs), [OGG changes](../../../tests/audio/ogg_chains.rs).
