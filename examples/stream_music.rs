// SPDX-FileCopyrightText: 2026 VMNL contributors
// SPDX-License-Identifier: MIT

//! Stream a track while the automatic worker refills its PCM ring.

#![allow(clippy::print_stdout)]

mod common;

use std::io;
use vmnl_audio::AudioDevice;

fn main() -> common::ExampleResult {
    let Some(path) = common::source_path("music.wav", "Stream music; Enter or EOF exits.")? else {
        return Ok(());
    };
    let audio = AudioDevice::builder().thread(true).build()?;
    let music = audio.load_music(path)?;
    let handle = music.play()?;
    common::check_background(&audio)?;
    println!("Streaming. Press Enter to close the device.");
    io::stdin().read_line(&mut String::new())?;
    handle.stop();
    common::check_background(&audio)
}
