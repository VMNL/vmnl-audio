# SoundHandle

## Role and public paths

`vmnl_audio::SoundHandle`, also under `audio`, controls one voice. Experimental;
[Rustdoc](../../../target/doc/vmnl_audio/audio/struct.SoundHandle.html).

## Public API and state

Private fields. `stop` is terminal; `pause` freezes a live voice, `resume` resumes
only a paused one. `set_volume` validates finite linear `0.0..=1.0`; zero still
consumes PCM. `set_looping` changes future mixing without restarting stopped
playback; disabling a loop finishes its current pass. `is_playing`, `is_paused`,
`is_stopped` inspect instance state independently of bus controls/device health.
`cursor_frames` counts consumed device-rate PCM frames, cumulatively across loops,
not hardware presentation time. An unlooped sound never advances past its length.
Derived `Clone` (`clone`) controls the same instance, not a second playback.

## Ownership, costs and errors

Dropping a handle does not stop the runtime-owned voice or keep native output
alive after device drop. Control changes do not withdraw already mixed output.
Invalid volume returns `InvalidState` without replacing it. Pausing, resuming,
gain or loop changes cannot undo terminal stop, including completion races.
Replay uses `Sound::play` for a new instance. No source decode occurs in these
methods; caller-side control state is shared with later mixing.

## Example and evidence

```rust,no_run
# extern crate vmnl_audio;
# fn main() -> vmnl_audio::AudioResult<()> {
let audio = vmnl_audio::AudioDevice::builder().thread(true).build()?;
let sound = audio.load_sound("examples/assets/effect.wav")?;
let handle = sound.play()?;
handle.pause();
handle.resume();
handle.stop();
assert!(handle.is_stopped());
# Ok(())
# }
```

Related: [Sound](sound.md), [state](playback_state.md), [gain and time](../concepts/gain_and_time.md).
Evidence: [state transitions](../../../tests/audio/playback_states.rs).
