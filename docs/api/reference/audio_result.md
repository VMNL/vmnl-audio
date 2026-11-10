# AudioResult

## Role and public paths

`vmnl_audio::AudioResult<T>`, also under `audio`, aliases
`Result<T, AudioError>`. Experimental;
[Rustdoc](../../../target/doc/vmnl_audio/audio/type.AudioResult.html).

## Public API, ownership and errors

This is an alias, not a new wrapper or ABI boundary. It introduces no fields,
variants, inherent methods or explicit implementations of its own. Standard
`Result` operations and `?` apply. Ownership/costs depend on the success value and
[AudioError](audio_error.md); constructing a result does not open a backend.
There are no audio defaults attached to the alias.

## Example and evidence

```rust
# extern crate vmnl_audio;
fn settings() -> vmnl_audio::AudioResult<vmnl_audio::AudioConfig> {
    let mut config = vmnl_audio::AudioConfig::default();
    config.set_master_volume(0.5)?;
    Ok(config)
}
assert!(settings().is_ok());
```

Evidence: [public contracts](../../../tests/audio/contracts.rs).
