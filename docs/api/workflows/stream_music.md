# Stream music

```rust,no_run
# extern crate vmnl_audio;
use vmnl_audio::{AudioDevice, AudioResult, MusicPlayConfig};
# fn main() -> AudioResult<()> {
let audio = AudioDevice::builder().thread(true).build()?;
let track = audio.load_music("examples/assets/music.wav")?;
let handle = track.play_with_config(MusicPlayConfig { volume: 0.5, looping: true })?;
// Keep audio alive in the application's event loop, then stop when leaving it.
handle.stop();
# Ok(())
# }
```

This snippet demonstrates construction only; it stops immediately. The runnable
`stream_music` example waits for stdin. `load_music` checks initial metadata;
each play opens its own decoder, allocates and prefills its ring before registration.
Late decoding failures remain possible. Inspect `take_background_error()` during
the application's lifetime and before teardown.

`set_looping(false)` preserves prefetched PCM, including repetitions. Replaying
after stop requires a new handle from the resource. See [Music](../reference/music.md)
and [MusicHandle](../reference/music_handle.md).
