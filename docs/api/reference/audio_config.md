# AudioConfig

## Role and public paths

`vmnl_audio::AudioConfig` (also `vmnl_audio::audio::AudioConfig`) stores requested
output settings without opening a device. Experimental; [Rustdoc](../../../target/doc/vmnl_audio/audio/struct.AudioConfig.html)
defines exact signatures.

## Public API

Private fields. `master_volume`, `sample_rate` and `channels` inspect requests;
`set_master_volume`, `set_sample_rate` and `set_channels` validate before replacement.
Explicit/derived implementations: `Default` (`default`), `Clone` (`clone`) and
`Debug` (`fmt`). No public backend types.

## Defaults and validation

Default stereo, 44,100 Hz and gain 1.0. Rate must be nonzero, channels exactly two,
gain finite in `0.0..=1.0`. Setters preserve the old value on failure. A requested
rate is not the resolved output rate; inspect the constructed device.

## Ownership, costs and errors

An ordinary owned value; cloning does not share mutable settings or start threads.
Invalid rate/gain yields `InvalidState`, invalid channels `UnsupportedFormat`.
No device, I/O or decode work occurs here.

## Example and evidence

```rust
# extern crate vmnl_audio;
let mut config = vmnl_audio::AudioConfig::default();
assert!(config.set_sample_rate(0).is_err());
assert_eq!(config.sample_rate(), 44_100);
```

Related: [builder](audio_device_builder.md), [defaults](../appendices/defaults.md).
Evidence: [public contracts](../../../tests/audio/contracts.rs).
