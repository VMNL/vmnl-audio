// SPDX-FileCopyrightText: 2026 VMNL contributors
// SPDX-License-Identifier: MIT

//! Native teardown observations with live resources and playback handles.

use std::time::{Duration, Instant};

use crate::backend_support::lock_backend_tests;
use crate::common::{wait_until, TempAudioFile};
use vmnl_audio::{AudioDevice, MusicPlayConfig, SoundPlayConfig};

#[test]
#[ignore = "requires a usable CPAL stereo output device"]
#[allow(clippy::print_stderr)] // Opt-in native diagnostics, not callback instrumentation.
fn device_drop_stops_consumption_while_resources_and_handles_stay_alive() {
    let _guard = lock_backend_tests();
    let wav = TempAudioFile::new("wav");
    wav.write_pcm16_wav(2, 44_100, 44_100 * 2, 2_000);

    for threaded in [false, true] {
        for iteration in 1..=10 {
            let build_started = Instant::now();
            let device = AudioDevice::builder()
                .thread(threaded)
                .master_volume(0.0)
                .build()
                .expect("native lifecycle probe requires a CPAL stereo output device");
            let build_us = build_started.elapsed().as_micros();
            let mode = device.control_mode();
            let rate = device.sample_rate();
            let channels = device.channels();
            let sound = device.load_sound(wav.path()).expect("load native sound");
            let music = device.load_music(wav.path()).expect("load native music");
            let sound_handle = sound
                .play_with_config(SoundPlayConfig {
                    volume: 1.0,
                    looping: true,
                })
                .expect("start native sound");
            let music_handle = music
                .play_with_config(MusicPlayConfig {
                    volume: 1.0,
                    looping: true,
                })
                .expect("prefill native music");
            assert!(
                wait_until(Duration::from_secs(2), || {
                    sound_handle.cursor_frames() > 0 && music_handle.cursor_frames() > 0
                }),
                "both muted playbacks must consume PCM before teardown"
            );
            assert!(device.take_background_error().is_none());

            let drop_started = Instant::now();
            drop(device);
            let drop_us = drop_started.elapsed().as_micros();
            let sound_frames = sound_handle.cursor_frames();
            let music_frames = music_handle.cursor_frames();
            std::thread::sleep(Duration::from_millis(100));
            assert_eq!(sound_handle.cursor_frames(), sound_frames);
            assert_eq!(music_handle.cursor_frames(), music_frames);
            assert_eq!(sound.path(), wav.path());
            assert_eq!(music.path(), wav.path());
            sound_handle.stop();
            music_handle.stop();

            eprintln!(
                "native_lifecycle mode={mode:?} iteration={iteration} rate={rate} \
                 channels={channels} master_volume=0 build_us={build_us} drop_us={drop_us} \
                 sound_frames={sound_frames} music_frames={music_frames}"
            );
        }
    }
}
