# First sound with automatic control

Add only `vmnl_audio` as a [direct dependency](../../getting_started.md). Select
the worker explicitly and keep the device alive while the application waits:

```rust,no_run
# extern crate vmnl_audio;
use vmnl_audio::AudioDevice;
# fn main() -> Result<(), Box<dyn std::error::Error>> {
let audio = AudioDevice::builder().thread(true).build()?;
let sound = audio.load_sound("examples/assets/effect.wav")?;
let handle = sound.play()?;
std::io::stdin().read_line(&mut String::new())?;
handle.stop();
if let Some(message) = audio.take_background_error() {
    return Err(std::io::Error::other(message).into());
}
# Ok(())
# }
```

The input wait belongs to the example's lifetime, not audio scheduling. A real
application keeps the device alongside its own event loop and checks diagnostics
there. No `update()` or sleep is needed for refill in this mode. The supplied
path is relative to the current directory; packaged examples resolve their own
default asset paths independently of it. Actual device opening is not executed
by this snippet test. Run `cargo run --example play_sound --locked` to try it.
