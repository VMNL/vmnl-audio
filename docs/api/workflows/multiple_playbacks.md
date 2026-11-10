# Multiple playbacks

```rust,no_run
# extern crate vmnl_audio;
use vmnl_audio::{AudioDevice, AudioResult, SoundPlayConfig};
# fn main() -> AudioResult<()> {
let audio = AudioDevice::builder().thread(true).build()?;
let effect = audio.load_sound("examples/assets/effect.wav")?;
let first = effect.play()?;
let second = effect.play_with_config(SoundPlayConfig { volume: 0.3, looping: false })?;
let same_instance = first.clone();
same_instance.pause(); // first pauses; second remains independent.
first.stop();
second.stop();
# Ok(())
# }
```

A resource clone shares PCM/path/runtime, not a playback cursor. Music plays each
open a separate decoder/ring. Sound has an initial limit of 64 active voices;
`set_max_sound_voices` clamps zero to one and stops oldest excess voices. There is
no corresponding public music-stream limit. Mixing work and prepared PCM memory
grow with active instances. Shared `sfx_bus` and `music_bus` controls affect each
category together; dropping handles alone does not stop runtime-owned playback.
