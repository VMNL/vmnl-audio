# Sound

## Role and public paths

`vmnl_audio::Sound`, also under `audio`, is a reusable fully decoded sound-effect
resource created by `AudioDevice::load_sound`. Experimental;
[Rustdoc](../../../target/doc/vmnl_audio/audio/struct.Sound.html).

## Public API and validation

Private fields. `play` starts an instance with default settings; `play_with_config`
uses a validated `SoundPlayConfig`. `path` returns the supplied path without
canonicalization. Derived `Clone` (`clone`) shares runtime and decoded PCM;
it does not clone a cursor. No public constructor or `Default`.

## Ownership, costs and errors

Loading decodes/converts the full source to device-rate stereo and may allocate,
lock/cache and perform file I/O. A cached source can be reused without reading it
again; a load still converts it for the device. Each play allocates/registers an
independent voice. Dropping its handle does not stop it. The resource retains data
but does not keep output alive after device drop.

Loading rejects unsupported formats/channels or changing OGG-chain metadata and
non-finite WAV PCM. Finite out-of-range amplitudes are preserved until final mixer
clipping. Play reports invalid gain or active-list lock errors. Loading/play belong
on the control side, outside the audio callback. See [formats](../appendices/formats.md).

## Example and evidence

```rust,no_run
# extern crate vmnl_audio;
# fn main() -> vmnl_audio::AudioResult<()> {
let audio = vmnl_audio::AudioDevice::builder().thread(true).build()?;
let effect = audio.load_sound("examples/assets/effect.wav")?;
let handle = effect.play()?;
handle.stop();
# Ok(())
# }
```

Related: [SoundHandle](sound_handle.md), [multiple playbacks](../workflows/multiple_playbacks.md).
Evidence: [decoding](../../../tests/audio/decoding.rs), [mixer](../../../tests/audio/runtime_mixer.rs).
