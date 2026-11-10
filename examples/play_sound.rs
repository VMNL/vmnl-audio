// SPDX-FileCopyrightText: 2026 VMNL contributors
// SPDX-License-Identifier: MIT

//! Play a cached effect using explicitly automatic control.

#![allow(clippy::print_stdout)]

mod common;

use std::io;
use vmnl_audio::AudioDevice;

fn main() -> common::ExampleResult {
    let Some(path) =
        common::source_path("effect.wav", "Play one cached sound; Enter or EOF exits.")?
    else {
        return Ok(());
    };
    let audio = AudioDevice::builder().thread(true).build()?;
    let sound = audio.load_sound(path)?;
    let handle = sound.play()?;
    common::check_background(&audio)?;
    println!("Playing. Press Enter to close the device.");
    io::stdin().read_line(&mut String::new())?;
    handle.stop();
    common::check_background(&audio)
}
