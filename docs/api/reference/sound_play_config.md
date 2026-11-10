# SoundPlayConfig

## Role and public paths

`vmnl_audio::SoundPlayConfig`, also under `audio`, initializes one voice before
registration. Experimental; [Rustdoc](../../../target/doc/vmnl_audio/audio/struct.SoundPlayConfig.html).

## Public API and defaults

Public fields: `volume` (`f32`, finite linear `0.0..=1.0`, default 1.0) and
`looping` (`bool`, default false). Implementations: `Default` (`default`),
`Clone` (`clone`), `Copy`, `Debug` (`fmt`). No inherent methods.

## Ownership, costs and errors

A copied value, not shared live controls. `Sound::play_with_config` validates gain
before registering a voice; invalid values yield `InvalidState`. Change the handle
for later controls. Disabling a live sound loop finishes its current repetition;
stop is terminal. No native work occurs merely by constructing this value.

## Example and evidence

```rust
# extern crate vmnl_audio;
let config = vmnl_audio::SoundPlayConfig { volume: 0.4, looping: false };
assert!(!config.looping);
```

Related: [Sound](sound.md), [SoundHandle](sound_handle.md).
Evidence: [contracts](../../../tests/audio/contracts.rs), [playback](../../../tests/audio/playback_states.rs).
