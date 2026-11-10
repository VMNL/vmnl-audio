# MusicHandle

## Role and public paths

`vmnl_audio::MusicHandle`, also under `audio`, controls one stream. Experimental;
[Rustdoc](../../../target/doc/vmnl_audio/audio/struct.MusicHandle.html).

## Public API and state

Private fields. `stop` is terminal; `pause` freezes a live instance, `resume` resumes
only a paused one. `set_volume` validates finite linear `0.0..=1.0`; zero consumes
PCM. `set_looping` governs subsequent refill: enabling on a live stream permits
reopening after decoder EOF; disabling preserves prefetched repetitions. Stopped
instances never restart. `is_playing`, `is_paused`, `is_stopped` inspect the instance,
independently of bus pause/mute and worker health. `cursor_frames` counts consumed
device-rate frames cumulatively across loops; underrun silence does not advance it.
Derived `Clone` (`clone`) controls the same stream.

## Ownership, costs and errors

Dropping a handle does not stop playback or keep native output alive after device
drop. Controls cannot withdraw mixed output. Invalid volume yields `InvalidState`
without changing it. State queries do not prove audible output or absence of
underruns. Completion can win a race with enabling looping; replay through `Music`
creates a new stream/decoder. Control methods do not synchronously refill the ring.

## Example and evidence

```rust,no_run
# extern crate vmnl_audio;
# fn main() -> vmnl_audio::AudioResult<()> {
let audio = vmnl_audio::AudioDevice::builder().thread(true).build()?;
let music = audio.load_music("examples/assets/music.wav")?;
let handle = music.play()?;
handle.set_looping(true);
handle.stop();
assert!(handle.is_stopped());
# Ok(())
# }
```

Related: [Music](music.md), [state](playback_state.md), [gain and time](../concepts/gain_and_time.md).
Evidence: [playback](../../../tests/audio/playback_states.rs), [OGG EOF](../../../tests/audio/ogg_playback.rs).
