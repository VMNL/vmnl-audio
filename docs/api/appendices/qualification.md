# Qualification limits

| Evidence | Establishes | Does not establish |
|---|---|---|
| Build/Clippy/example compilation | Rust target/compiler and code checks | Device availability or playback. |
| `--help` execution | CLI path works without constructing a device | Native route, controls or listening quality. |
| Deterministic audio suite | Decoder, resampling, ring, mixer/state/worker contracts under controlled inputs | Hardware timing, backend shutdown, external C heap behavior. |
| Native probes | Only the explicitly executed device scenarios/environment | Human listening or realtime deadlines. |
| Human listening | Operator's reported source/route/observations | General platform support or hard timing bounds. |
| Realtime measurement | Recorded workload and measurement scope | Universal OS scheduling guarantees. |

Hosted CI runs the first three categories and compiles native probes only. Native
shutdown, disconnection/recovery, listening, container padding/timing and callback
deadline qualification remain separate work. See [test protocol](../../testing.md)
and the [technical acceptance target](../../audio.md). No evidence is implied by
merely documenting a platform or providing a probe.

Local Linux native startup/control/teardown observations are recorded in the
[qualification inventory](../../qualification.md), with source checksums, raw
results and explicit exclusions. They are not hosted-CI or listening evidence.
