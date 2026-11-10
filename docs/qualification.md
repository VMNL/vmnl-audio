# Qualification status

This is an evidence inventory, not a claim that the audio acceptance target is
complete. The [audio contract](audio.md) defines the target; [testing](testing.md)
defines how to reproduce checks. Preserve source identity and environmental scope
when adding results. Automated native execution is distinct from human listening.

## Recorded Linux execution — 2026-11-10

Production source: `c4c7b8793a5fbd2a8d80ddba3b4da31332f835c3`.
The execution adds the native lifecycle probe and its test registration to that
revision; production sources and Cargo.lock are unchanged. The
[context record](qualification/linux-2026-11-10/context.json) includes the production
source tree, lockfile checksum, every test-source checksum, toolchain and host
observations. This identifies the tested code without labelling a dirty checkout
as the unmodified source commit.

Environment: Fedora Linux 44 x86_64, kernel 7.2.11-200.fc44.x86_64, Rust 1.95.0,
CPAL 0.18.2, ALSA 1.2.16.1 and PipeWire 1.6.10. ALSA's `default` is configured to
PipeWire; the host default output is the sof-hda-dsp Speaker route. Host volume was
0.25, unmuted, before and after the run; the default route and volume were unchanged.
These are host configuration observations, not a recording of delivered audio.

| Check | Status | Evidence and limits |
|---|---|---|
| Native default constructors and configured modes | PASS | Existing ignored probes executed; no setup failures converted to skips. |
| Automatic refill / manual refill responsibility | PASS | Callback progress beyond initial prefill in automatic mode; manual exhaustion/refill checked. |
| Playback handles, bus controls and terminal worker errors | PASS | Native public API probes, including decoder/refill failures. This does not inject a CPAL device disconnection. |
| OGG metadata transitions and extreme finite WAV playback | PASS | Native load/prefill/late-error paths and consumed-frame completion exercised. |
| Device drop with live Sound/Music resources and handles | PASS, scoped | Ten cycles per control mode; positive PCM consumption before drop, unchanged cursors for 100 ms after drop. |
| Four runnable examples with stdin EOF | PASS | Each exits successfully under a 10 s process timeout. This is startup/EOF behavior, not listening evidence. |
| `just run` example launcher | PASS | Default interactive launch, all four help paths and a quoted source path checked; see the [launcher record](qualification/linux-2026-11-10/just-run.json). |
| Interactive controls | PASS, scoped | Pause/resume/stop/replay predicates and retained bus mute checked; volume/loop commands accepted. Audible behavior was not inspected. |
| Cargo publication dry-run | PASS, scoped | Packaging/build verification at the production revision; upload aborted by `--dry-run`. No registry ownership or publication claim. |

The [native log](qualification/linux-2026-11-10/native.log) contains **12 passed,
0 failed, 0 ignored**, including the new lifecycle probe's 20 cycles. The
[example results](qualification/linux-2026-11-10/examples.json) record exact commands
and observed state output. The [package log](qualification/linux-2026-11-10/package-dry-run.log)
records the separate clean-source dry-run; repeat it for the actual release candidate.

## Lifecycle observations

The [lifecycle probe](../tests/audio/backend_lifecycle.rs) requests the default
44,100 Hz stereo configuration, with master
gain zero. All 20 devices resolved to 44,100 Hz and two channels. A looping cached
sound and streaming music instance both consume PCM before device destruction;
resources and handles stay alive afterwards. The probe also checks their source
paths remain usable and stops the retained handles after observing frozen cursors.

`Instant` measures whole device construction and `drop(device)` on the control
thread, outside callbacks. Values below are descriptive microseconds from this
single run, not deadlines or a comparison of the two modes:

| Mode | Cycles | Build min / median / max (µs) | Drop min / median / max (µs) |
|---|---|---|---|
| Manual | 10 | 19,044 / 20,578.5 / 33,139 | 1,250 / 1,553.5 / 2,417 |
| Automatic | 10 | 16,171 / 18,597 / 21,341 | 892 / 1,351.5 / 1,813 |

The host was not isolated, modes ran in a fixed order and the workload uses a
small local WAV. There is no delayed/blocked I/O injection, no tail-distribution
qualification, and no hardware presentation measurement. Frozen cursors establish
only the finite observation window. The external watchdog bounds a failed test
process; it does not establish an API shutdown deadline.

## Operator feedback — 2026-11-10

The operator reported: **"Le test audio fonctionne"** (the audio test works).
This is a positive manual audio result. The report does not specify the OS,
output route, source or individual control observations; the complete listening
checklist therefore remains partial. It is separate from the automated Linux
execution and timing observations above.

## Remaining evidence

| Requirement | Status | Needed next |
|---|---|---|
| Windows and macOS native output | NOT RUN | Execute the same probes on usable stereo routes; record exact source and environment. Hosted CI only compiles these probes. |
| Human listening | PARTIAL | Positive operator audio result above; still needs OS, device/route, source, volume and explicit controls/EOF/loop observations. |
| CPAL disconnection/error/recovery | NOT RUN | Explicit device/route failure scenario and resulting diagnostics/lifecycle observations. Decoder errors do not substitute for this. |
| Callback deadlines and underruns | NOT RUN | Defined workload and backend buffer/rate data, native callback instrumentation and measured timing/underruns. |
| Shutdown with blocked/slow decoding or I/O | NOT RUN | Controlled delay and lifecycle observations; nominal drop times above are insufficient. |
| Encoder delay, container padding/timing | NOT RUN | Reference streams with known timing and expected decoded/presented boundaries. |
| Registry name/ownership and first compatibility baseline | NOT RUN | Review at the actual release candidate before any manual publication. A successful dry-run neither reserves the name nor establishes ownership. |

The import PR remains a draft. This record does not authorize merging, closing
the original audio PR, removing the original VMNL facade, or publishing a release.

## Reproduce and extend

Complete the ordered [contribution checks](../CONTRIBUTING.md#before-submission),
then run the explicitly ignored native target on a usable route. On Linux:

```sh
timeout --signal=TERM --kill-after=5s 90s \
  cargo test --test audio-backend --locked -- \
  --ignored --test-threads=1 --nocapture
```

Use an appropriate external watchdog on other platforms. Record source SHA and
all uncommitted test changes/checksums, compiler, OS, CPAL/backend, output route,
resolved rate/channels and initial mute/volume. Preserve raw results and nonzero
exit/timeout failures. Do not alter host settings during a qualification run.

For listening, run `cargo run --example playback_controls --locked` and explicitly
report pause/resume, volume, mute/unmute, loop on/off, stop, resume after stop and
replay. Stopped playback must remain stopped until `play` creates a new instance.
Also report the source and whether EOF, errors or audible discontinuities occur.
Only a human operator's explicit observations qualify this listening row.
