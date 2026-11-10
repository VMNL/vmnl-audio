# Defaults and policies

| Setting | Default / policy | Explicit control |
|---|---|---|
| VMNL control | Manual | `AudioDeviceBuilder::thread(true)` opts into Automatic. |
| Requested rate | 44,100 Hz | Configuration or builder; inspect device's resolved rate. |
| Output channels | 2 | Other counts rejected. |
| Master / bus / playback gains | 1.0 | Finite linear `0.0..=1.0`. |
| Mute / pause | false | Shared bus or individual pause controls. |
| Playback loop | false | Play config / handle. |
| Sound voice limit | 64 | Device clamps zero to one and stops oldest excess voices. |
| Output device | CPAL default | No public device selector. |
| Output sample format | F32, I16, U16, I32, U32, F64, I8/U8 priority | No public override. |
| Rate resolution | Nearest supported range within format priority | Inspect `sample_rate()`. |
| Backend buffer | Backend default | No public latency/buffer-size selector. |
| Music ring | Internal 500 ms PCM capacity | No public size control or universal update deadline. |
| Async diagnostics | One shared last-error slot | `take_background_error()` consumes it. |

Current fixed policies are explicit limitations, not configurable API promises.
See [device](../reference/audio_device.md), [execution](../concepts/execution.md)
and [qualification](qualification.md).
