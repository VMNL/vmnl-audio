// SPDX-FileCopyrightText: 2026 Nathan Flachat
// SPDX-License-Identifier: MIT

//! Independent audio playback with a private CPAL output backend.
//!
//! [`Sound`] keeps decoded effects in memory; [`Music`] opens a streaming decoder
//! for each playback. [`AudioDevice`] owns the output stream and its resolved
//! stereo sample rate. Resource loading and manual control may allocate and do
//! file I/O; they must not run on the audio callback.
//! Finite float32 WAV samples outside `[-1, 1]` remain accepted. Decoding and
//! resampling preserve finite PCM without source clipping; the mixer clamps its
//! final output to `[-1, 1]`. Non-finite PCM is rejected with [`AudioError::DecoderFailed`].
//! OGG/Vorbis chains must keep the initial channel count and sample rate across
//! their logical streams; a detected change is rejected during decoding.
//! [`AudioDevice::load_music`] checks initial metadata, not the whole track.
//!
//! Control defaults to [`ControlMode::Manual`]: call [`AudioDevice::update`]
//! to process commands, refill music, and clean up. Select
//! [`AudioDeviceBuilder::thread`] with `true` to opt into automatic control.
//! The backend executes its audio callback in either mode.
//! Dropping the device stops output and joins its worker; resources and cloned
//! handles can retain shared runtime data but do not keep that output stream alive.
//!
//! # Development status
//!
//! This API is experimental. Snapshot heap behaviour has device-independent
//! regression coverage; native shutdown and realtime timing remain unqualified.
//! The required target is recorded in the
//! [audio acceptance contract](https://github.com/VMNL/vmnl-audio/blob/main/docs/audio.md).
//! Use this crate directly; it does not require a VMNL facade or graphics context.
//!
//! # Configure without opening a device
//!
//! ```
//! use vmnl_audio::{AudioConfig, AudioResult};
//!
//! # fn main() -> AudioResult<()> {
//! let mut config = AudioConfig::default();
//! config.set_sample_rate(48_000)?;
//! config.set_master_volume(0.5)?;
//! assert_eq!(config.sample_rate(), 48_000);
//! # Ok(())
//! # }
//! ```
//!
//! # Automatic control
//!
//! Select the worker explicitly and keep the device alive in your application.
//! No caller-side refill loop or sleep is required in this mode. Inspect
//! [`AudioDevice::take_background_error`] from the application's control code.
//!
//! ```no_run
//! use vmnl_audio::{AudioDevice, AudioResult};
//! # fn main() -> AudioResult<()> {
//! let audio = AudioDevice::builder().thread(true).build()?;
//! let sound = audio.load_sound("examples/assets/effect.wav")?;
//! let handle = sound.play()?;
//! // Keep audio alive while the application's event loop runs.
//! handle.stop();
//! # Ok(())
//! # }
//! ```
//!
//! # Advanced manual control
//!
//! Opening a device needs a usable native output backend. This example compiles
//! without running that backend; the application must keep updating its control
//! work while playback is active.
//!
//! ```no_run
//! use vmnl_audio::{AudioConfig, AudioDevice, AudioResult};
//!
//! # fn main() -> AudioResult<()> {
//! let audio = AudioDevice::builder()
//!     .config(AudioConfig::default())
//!     .thread(false)
//!     .build()?;
//! audio.update()?; // Call again from the application's control loop.
//! # Ok(())
//! # }
//! ```

pub mod audio;

pub use audio::{
    AudioBus, AudioConfig, AudioDevice, AudioDeviceBuilder, AudioError, AudioResult, ControlMode,
    Music, MusicHandle, MusicPlayConfig, PlaybackState, Sound, SoundHandle, SoundPlayConfig,
};
