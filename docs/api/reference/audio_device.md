# AudioDevice

## Role and public paths

`vmnl_audio::AudioDevice`, also under `audio`, owns one CPAL output stream and
its runtime/optional worker. Experimental; [Rustdoc](../../../target/doc/vmnl_audio/audio/struct.AudioDevice.html).

## Public API

| Methods | Behavior |
|---|---|
| `builder`, `new` | Builder or immediate manual construction with `AudioConfig`. |
| `sample_rate`, `channels`, `control_mode` | Resolved rate (Hz), stereo channels and configured control policy. |
| `load_sound`, `load_music` | Cached complete sound or reusable streaming source. |
| `set_master_volume`, `master_volume` | Shared finite linear master gain. |
| `music_bus`, `sfx_bus` | Shared category controls. |
| `update` | Manual command/refill/cleanup cycle; healthy automatic mode is a no-op. |
| `stop_all`, `pause_all`, `resume_all` | Queue global controls; manual mode also runs a cycle immediately. |
| `set_max_sound_voices` | Clamp to at least one; stop oldest excess voices immediately. |
| `take_background_error` | Take the shared last worker/CPAL diagnostic. |

Private fields; no `Clone`. Explicit `Drop` (`drop`) joins the worker, then destroys
the stream before runtime ownership. Auto traits are inventoried, not promises
that a native stream is valid on every platform/thread.

## Defaults and validation

Manual by default; opt into automatic via the builder. Default output device,
stereo, requested 44,100 Hz/gain 1.0, initially 64 sound voices. Formats rank F32,
I16, U16, I32, U32, F64, I8/U8; rate is clamped within a supported range of that
priority. CPAL chooses default buffering; no fixed latency is requested.

## Ownership, costs and errors

Keep the device alive: resources/handles retain runtime data but not the stream.
Loading, playback creation, manual cycles and limit changes can lock, allocate
or perform I/O; they must not run on a data callback. Shutdown can block on
in-flight decode/I/O without a deadline. Backend creation needs usable native output.

Invalid configuration fails before querying output where practical. Load/refill
can fail on files, codecs or unsupported metadata changes. Global controls expose
queue/manual cycle errors; after automatic worker failure they return `InvalidState`.
`control_mode` still reports Automatic. Recovery needs a new device/resources.
The diagnostic slot can be overwritten and taking it does not restore the worker.
See [errors and costs](../concepts/errors_and_costs.md) and [AudioError](audio_error.md).

## Example and evidence

```rust,no_run
# extern crate vmnl_audio;
# fn main() -> vmnl_audio::AudioResult<()> {
let audio = vmnl_audio::AudioDevice::builder().thread(true).build()?;
assert_eq!(audio.channels(), 2);
// Keep audio alive for the application's playback lifetime.
# Ok(())
# }
```

Evidence: [contracts](../../../tests/audio/contracts.rs),
[worker behavior](../../../tests/audio/worker.rs), [native probes](../../../tests/audio/backend.rs)
(opt-in; compilation is not native execution).
