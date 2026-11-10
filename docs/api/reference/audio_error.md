# AudioError

## Role and public paths

`vmnl_audio::AudioError`, also under `audio`, represents configuration, decoding,
backend and control failures. Experimental;
[Rustdoc](../../../target/doc/vmnl_audio/audio/enum.AudioError.html).

## Public API

| Variant | Payload / meaning |
|---|---|
| `BackendInitFailed` | String: native output query/build/start failure. |
| `ControlThreadStartFailed` | String: opt-in worker could not start. |
| `DecoderFailed` | String: metadata, decoding or PCM conversion failed. |
| `InvalidState` | String: invalid gain/rate/buffer or failed worker. |
| `UnsupportedFormat` | String: codec/channels/output format or changing OGG-chain metadata. |
| `CommandQueuePoisoned` | Global queue mutex poisoned. |
| `SoundCachePoisoned` | Cached decoded-source lock poisoned. |
| `ActiveSoundVoicesPoisoned` | Active voice list lock poisoned. |
| `ActiveMusicStreamsPoisoned` | Active stream list lock poisoned. |
| `MusicDecoderPoisoned` | Stream decoder/scratch lock poisoned. |
| `Io` | `std::io::Error` from file operations. |

No inherent methods. Implementations: `Debug` and `Display` (both `fmt`),
`std::error::Error` (no custom `source` override) and `From<std::io::Error>` (`from`).
No Clone/default; payload strings are diagnostic text, not stable machine codes.

## Ownership, costs and recovery

An owned error can carry allocated text or I/O data. Codec adapters may translate
their file/codec errors to `DecoderFailed`; do not assume every file failure is `Io`.
Manual refill errors return synchronously and stop the instance. An automatic
worker error/panic is reported as a diagnostic string in a shared overwritable
slot and leaves the worker failed; rebuilding the device is required for recovery.
Backend diagnostics do not restart output. See [recovery](../concepts/errors_and_costs.md).

## Example and evidence

```rust
# extern crate vmnl_audio;
let mut config = vmnl_audio::AudioConfig::default();
assert!(matches!(config.set_sample_rate(0), Err(vmnl_audio::AudioError::InvalidState(_))));
```

Related: [AudioResult](audio_result.md).
Evidence: [public contracts](../../../tests/audio/contracts.rs), [worker](../../../tests/audio/worker.rs).
