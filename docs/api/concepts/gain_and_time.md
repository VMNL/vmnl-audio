# Gains, pause and time

Gains are finite linear multipliers in `0.0..=1.0`, not decibels. Instance, category
and master gains multiply. Music and SFX have separate buses. Bus mute preserves
the configured volume; its effective gain becomes zero.

Mute and zero gain silence output **while consuming PCM**. A muted non-looping
instance can reach EOF. Pause freezes consumption: handle pause affects one
instance, category pause freezes its route, and `pause_all` freezes both routes.
Bus pause does not replace instance state; resuming a bus leaves explicitly paused
and stopped handles unchanged. Effective gain alone cannot distinguish pause/mute.

`cursor_frames()` counts complete PCM frames consumed by the mixer at the resolved
device rate, cumulatively across loops. It is not a hardware presentation clock.
Music underrun silence does not advance its cursor. Bus mute continues advancing
it; pause freezes it. Commands cannot withdraw output already handed to the backend.

Decoder EOF does not complete music until buffered PCM drains. Disabling music
looping preserves prefetched repetitions; disabling a sound loop finishes its current
pass. Enabling looping cannot restart a stopped instance. See [controls](../workflows/controls.md).
