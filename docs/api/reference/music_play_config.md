# MusicPlayConfig

## Role and public paths

`vmnl_audio::MusicPlayConfig`, also under `audio`, initializes one stream before
prefill/registration. Experimental; [Rustdoc](../../../target/doc/vmnl_audio/audio/struct.MusicPlayConfig.html).

## Public API and defaults

Public fields: `volume` (`f32`, finite linear `0.0..=1.0`, default 1.0) and
`looping` (`bool`, default false). Implementations: `Default` (`default`),
`Clone` (`clone`), `Copy`, `Debug` (`fmt`). No inherent methods.

## Ownership, costs and errors

A copied value, not shared live controls. `Music::play_with_config` validates gain
before registration, returning `InvalidState` for invalid values; prefill can also
fail on source/decoder errors. Looping can reopen the source. Disabling a live loop
retains prefetched PCM, including repeated passes. Constructing settings alone
does not open files/devices or start threads.

## Example and evidence

```rust
# extern crate vmnl_audio;
let config = vmnl_audio::MusicPlayConfig { volume: 0.4, looping: true };
assert!(config.looping);
```

Related: [Music](music.md), [MusicHandle](music_handle.md).
Evidence: [contracts](../../../tests/audio/contracts.rs), [playback](../../../tests/audio/playback_states.rs).
