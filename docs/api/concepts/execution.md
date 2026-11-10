# Execution and threads

Default construction selects `ControlMode::Manual`. Explicit `.thread(true)`
selects `Automatic`: a VMNL worker processes commands, refills music and cleans up.
Automatic clients do not need a refill `update()` loop or sleep. A healthy automatic
`update()` is a no-op; it never adds a competing control producer.

Manual clients drive `update()` from their own control loop. That call can allocate,
lock, decode and perform file I/O. There is no universally safe interval: workload,
device rate and scheduling affect buffer supply. The internal music ring currently
holds 500 ms of output PCM, which is not a scheduling or latency guarantee.

CPAL output runs independently in both modes. Manual mode does not render output
synchronously on the caller and does not suppress backend threads. Native thread
and teardown behavior require platform-specific qualification.

Dropping the device requests worker stop, wakes its idle wait and joins in-flight
work before dropping the stream. Joining can block on decoding/I/O; no shutdown
deadline is guaranteed. Keep loading, playback creation and control work outside
the audio data callback.
