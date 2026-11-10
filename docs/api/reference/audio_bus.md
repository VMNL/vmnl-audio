# AudioBus

## Role and public paths

`vmnl_audio::AudioBus`, also under `audio`, shares category controls obtained from
`music_bus`/`sfx_bus`. Experimental; [Rustdoc](../../../target/doc/vmnl_audio/audio/struct.AudioBus.html).

## Public API and defaults

Private fields. `set_volume` / `volume` set/read finite linear gain in `0.0..=1.0`.
`mute`, `unmute`, `is_muted` control silence without losing stored volume.
`pause`, `resume`, `is_paused` freeze the route independently of handle states.
`gain` reports zero when muted or paused. Initial volume 1.0, unmuted, unpaused.
Implementations: shared `Clone` (`clone`), `Debug` (`fmt`). No public constructor.

## Ownership, costs and errors

Clones target the same route/runtime. Mute/zero gain consume PCM; pause freezes it.
Resuming the route preserves individual pause/stop. These controls do not keep
output alive after device destruction. Invalid volume returns `InvalidState` and
preserves the previous value. Gain alone cannot distinguish mute from pause.
No source decoding occurs here; controls apply to later mixes, not output already
handed to the backend.

## Example and evidence

```rust,no_run
# extern crate vmnl_audio;
# fn main() -> vmnl_audio::AudioResult<()> {
let audio = vmnl_audio::AudioDevice::builder().thread(true).build()?;
let bus = audio.music_bus();
bus.mute();
assert!(bus.is_muted());
assert_eq!(bus.volume(), 1.0);
# Ok(())
# }
```

Related: [gain and time](../concepts/gain_and_time.md).
Evidence: [gain semantics](../../../tests/audio/gain_semantics.rs).
