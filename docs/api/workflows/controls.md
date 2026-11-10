# Control playback and routes

```rust,no_run
# extern crate vmnl_audio;
use vmnl_audio::{AudioDevice, AudioResult};
# fn main() -> AudioResult<()> {
let audio = AudioDevice::builder().thread(true).build()?;
let music = audio.load_music("examples/assets/music.wav")?;
let handle = music.play()?;
handle.pause();
handle.set_volume(0.4)?;
handle.resume();
let bus = audio.music_bus();
bus.mute(); // PCM is still consumed.
bus.unmute();
handle.set_looping(true);
handle.stop();
let replay = music.play()?; // New instance: resume cannot undo stop.
replay.stop();
# Ok(())
# }
```

The runnable `playback_controls` example keeps these operations interactive.
Handle state queries describe that instance, independently of bus pause/mute and
device health. Master/category controls do not replace its individual gain.
`stop_all`, `pause_all` and `resume_all` queue global commands; automatic execution
may observe them later. Handle/bus operations affect shared state directly, while
already mixed output is unaffected. Check async diagnostics after commands and
before exit; one slot is not an event queue. See [gains and time](../concepts/gain_and_time.md).
