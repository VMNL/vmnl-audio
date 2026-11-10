# Public reference

All public types are experimental. Root reexports and `audio` paths identify the
same items; exact signatures and local contracts live in Rustdoc.

| Item | Role |
|---|---|
| [AudioBus](audio_bus.md) | Shared route controls |
| [AudioConfig](audio_config.md) | Requested output settings |
| [AudioDevice](audio_device.md) | Output stream/runtime owner |
| [AudioDeviceBuilder](audio_device_builder.md) | Configuration and worker selection |
| [AudioError](audio_error.md) | Structured synchronous failures |
| [AudioResult](audio_result.md) | Fallible result alias |
| [ControlMode](control_mode.md) | Manual or automatic control |
| [Music](music.md) | Streaming resource |
| [MusicHandle](music_handle.md) | One music instance |
| [MusicPlayConfig](music_play_config.md) | Initial music settings |
| [PlaybackState](playback_state.md) | Instance state |
| [Sound](sound.md) | Cached sound resource |
| [SoundHandle](sound_handle.md) | One sound instance |
| [SoundPlayConfig](sound_play_config.md) | Initial sound settings |

See [concepts](../concepts/resources.md), [first playback](../workflows/first_sound.md),
[symbol aliases](../appendices/public_symbol_index.md), [method index](../appendices/method_index.md)
and [qualification limits](../appendices/qualification.md).
