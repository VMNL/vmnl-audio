# Advanced manual control

```rust,no_run
# extern crate vmnl_audio;
use vmnl_audio::{AudioDevice, AudioResult};
# fn main() -> AudioResult<()> {
let audio = AudioDevice::builder().thread(false).build()?;
let track = audio.load_music("examples/assets/music.wav")?;
let handle = track.play()?;
while !handle.is_stopped() {
    audio.update()?;
    // Integrate input/work and diagnostic handling here without starving refill.
}
# Ok(())
# }
```

This is a control-flow sketch, not a recommended busy loop. The runnable
`manual_control` example uses illustrative pacing and a nonblocking input channel.
The caller owns cadence and should measure buffer supply for its workload. Neither
a fixed sleep nor the worker's internal interval is a universal deadline guarantee.

Manual control is the default and still uses independent CPAL output execution.
`update()` can block on decoding/I/O. Global commands additionally execute a control
cycle immediately in manual mode. Keep this work off data callbacks. A refill error
is returned synchronously and stops its instance; inspect backend diagnostics too.
See [execution](../concepts/execution.md) and [AudioDevice](../reference/audio_device.md).
