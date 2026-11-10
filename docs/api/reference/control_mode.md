# ControlMode

## Role and public paths

`vmnl_audio::ControlMode`, also under `audio`, identifies who owns control cycles.
Experimental; [Rustdoc](../../../target/doc/vmnl_audio/audio/enum.ControlMode.html).

## Public API and defaults

`Manual`: caller drives `update`; default builder/new policy. `Automatic`: explicitly
enabled worker drives control. Neither variant disables backend-managed output
execution. No public fields or inherent methods. Implementations: `Clone` (`clone`),
`Copy`, `Debug` (`fmt`), `PartialEq` (`eq`) and `Eq`; no `Default` implementation.

## Ownership, costs and errors

A copied policy value with no backend resources or fallible operations. Device
inspection returns configured policy, not worker health. Failed automatic control
remains Automatic and never silently falls back to manual. See [execution](../concepts/execution.md).

## Example and evidence

```rust
# extern crate vmnl_audio;
assert_eq!(vmnl_audio::AudioDevice::builder().control_mode(), vmnl_audio::ControlMode::Manual);
```

Evidence: [contracts](../../../tests/audio/contracts.rs).
