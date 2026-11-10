# AudioDeviceBuilder

## Role and public paths

`vmnl_audio::AudioDeviceBuilder`, also under `audio`, assembles output settings.
Experimental; [Rustdoc](../../../target/doc/vmnl_audio/audio/struct.AudioDeviceBuilder.html).

## Public API

Private fields. `config` replaces requests; `sample_rate`, `channels` and
`master_volume` override individual settings. `thread` chooses worker use,
`control_mode` inspects that choice and `build` opens output. Implementations:
`Default` (`default`), `Clone` (`clone`), `Debug` (`fmt`).

## Defaults and validation

The default [configuration](audio_config.md) uses manual control. `thread(true)`
explicitly selects automatic. Builder setting methods defer validation to `build`:
nonzero rate, stereo and finite gain in `0.0..=1.0`. Format selection can resolve a
different rate; format priority precedes rate proximity.

## Ownership, costs and errors

Configuration methods consume/return the builder without opening a device.
`build` consumes it and can allocate, query native devices and start stream/worker.
It returns configuration/unsupported-format errors, `BackendInitFailed`, or
`ControlThreadStartFailed`. The resulting [device](audio_device.md) owns teardown.

## Example and evidence

```rust
# extern crate vmnl_audio;
use vmnl_audio::{AudioDevice, ControlMode};
let builder = AudioDevice::builder().thread(true);
assert_eq!(builder.control_mode(), ControlMode::Automatic);
```

Evidence: [public contracts](../../../tests/audio/contracts.rs).
