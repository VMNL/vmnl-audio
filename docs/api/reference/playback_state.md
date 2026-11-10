# PlaybackState

## Role and public paths

`vmnl_audio::PlaybackState`, also under `audio`, describes one playback independently
of bus controls. Experimental; [Rustdoc](../../../target/doc/vmnl_audio/audio/enum.PlaybackState.html).

## Public API and transitions

`#[repr(u8)]`: `Playing` = 0, `Paused` = 1, `Stopped` = 2. No inherent methods.
Implementations: `Clone` (`clone`), `Copy`, `Debug` (`fmt`), `PartialEq` (`eq`), `Eq`.
No `Default`. Handles expose state through predicates rather than a state getter.

Playing may consume PCM when its route permits it; Paused freezes that instance;
Stopped is terminal after explicit stop or completion. Pause/resume on Stopped
cannot restart it, including completion/control races. Create a new handle to replay.
Bus pause/mute does not replace these states. Playing does not prove audible output.

## Ownership, costs and errors

Copied enum; no resource, allocation, fallible operation or timing guarantee.
See [handles](sound_handle.md) and [gain/time semantics](../concepts/gain_and_time.md).

## Example and evidence

```rust
# extern crate vmnl_audio;
assert_eq!(vmnl_audio::PlaybackState::Stopped as u8, 2);
```

Evidence: [state transitions](../../../tests/audio/playback_states.rs).
