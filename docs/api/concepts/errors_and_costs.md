# Errors, recovery and costs

Fallible operations return `AudioResult<T>`. Configuration validation happens
before opening the backend where practical. Decode/file failures can happen on
load, music prefill or late refill. Successful `load_music` validates initial
metadata, not the entire source. Exact variants belong to [AudioError](../reference/audio_error.md).

In manual mode a failed refill stops that stream, attempts cleanup and returns
the original error; later cycles can service remaining streams. An automatic
control error/unwinding panic terminates the worker. Automatic global commands and
`update` then return `InvalidState`, with no fallback/restart. Recovery requires a
new device and resources attached to it.

`take_background_error` takes one shared last-error slot for worker and CPAL
diagnostics. It can be overwritten; taking it does not restore worker health.
Inspect it from application control code. Backend errors do not restart streams.
`panic=abort`, native aborts and OS termination are not recovered by panic capture.

Loading sound allocates proportional to decoded length; each music play opens a
decoder, allocates a ring and prefills it on the caller. Playback registration,
voice-limit changes and manual cycles can lock/allocate. None belongs on the audio
data callback. The callback mixes prepared PCM with work proportional to frames
and active playbacks. Snapshot/ring regression evidence does not measure C/backend
allocations, error-callback locking, native shutdown or callback deadlines.

Finite float32 WAV amplitudes outside `[-1, 1]` are accepted without source clipping.
Interpolation preserves finitude or fails before publication; final mixer output
is clamped to `[-1, 1]`. Actual NaN/infinity samples are rejected.
