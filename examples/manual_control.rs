// SPDX-FileCopyrightText: 2026 VMNL contributors
// SPDX-License-Identifier: MIT

//! Advanced manual refill; the input thread only keeps stdin from blocking control.

#![allow(clippy::print_stdout)]

mod common;

use std::io;
use std::sync::mpsc::{self, TryRecvError};
use std::thread;
use std::time::Duration;
use vmnl_audio::AudioDevice;

fn main() -> common::ExampleResult {
    let Some(path) = common::source_path(
        "music.wav",
        "Manual streaming; Enter, EOF or track completion exits.",
    )?
    else {
        return Ok(());
    };
    let audio = AudioDevice::builder().thread(false).build()?;
    let music = audio.load_music(path)?;
    let handle = music.play()?;
    let (sender, receiver) = mpsc::channel();
    // Do not join a thread potentially blocked on stdin when the track finishes.
    let _input = thread::Builder::new()
        .name("example-stdin".into())
        .spawn(move || {
            let _ = sender.send(io::stdin().read_line(&mut String::new()));
        })?;
    println!("Manual control. Press Enter to stop.");
    while !handle.is_stopped() {
        audio.update()?;
        common::check_background(&audio)?;
        match receiver.try_recv() {
            Ok(input) => {
                input?;
                break;
            }
            Err(TryRecvError::Disconnected) => break,
            Err(TryRecvError::Empty) => {}
        }
        // Illustrative pacing only; decoding/I/O and scheduling vary by workload.
        thread::sleep(Duration::from_millis(5));
    }
    handle.stop();
    common::check_background(&audio)
}
