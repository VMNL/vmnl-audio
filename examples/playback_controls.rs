// SPDX-FileCopyrightText: 2026 VMNL contributors
// SPDX-License-Identifier: MIT

//! Control a music instance and its shared bus; replay creates a new handle.

#![allow(clippy::print_stdout)]

mod common;

use std::io::{self, BufRead};
use vmnl_audio::{AudioDevice, MusicPlayConfig};

const COMMANDS: &str = "\
╭──────────── \x1b[1mAudio Commands\x1b[0m ────────────╮
  \x1b[2mListening\x1b[0m
    \x1b[4mplay\x1b[0m          \x1b[3mPlay the sound\x1b[0m
    \x1b[4mpause\x1b[0m         \x1b[3mPause the sound\x1b[0m
    \x1b[4mresume\x1b[0m        \x1b[3mUnpause the sound\x1b[0m
    \x1b[4mstop\x1b[0m          \x1b[3mStop the sound\x1b[0m

  \x1b[2mSettings\x1b[0m
    \x1b[4mvolume 0.5\x1b[0m    \x1b[3mChange volume (values from 0 to 1)\x1b[0m
    \x1b[4mmute\x1b[0m          \x1b[3mMute the sound\x1b[0m
    \x1b[4munmute\x1b[0m        \x1b[3mUnmute the sound\x1b[0m
    \x1b[4mloop on/off\x1b[0m   \x1b[3mLoop on the sound / deactivate the loop\x1b[0m

  \x1b[2mInformation\x1b[0m
    \x1b[4mstatus\x1b[0m        \x1b[3mDisplay status\x1b[0m
    \x1b[4mquit\x1b[0m          \x1b[3mQuit\x1b[0m
╰───────────────────────────────────────╯";

fn main() -> common::ExampleResult {
    let Some(path) = common::source_path("music.wav", COMMANDS)? else {
        return Ok(());
    };
    let audio = AudioDevice::builder().thread(true).build()?;
    let music = audio.load_music(path)?;
    let bus = audio.music_bus();
    let mut config = MusicPlayConfig::default();
    let mut handle = music.play_with_config(config)?;
    common::check_background(&audio)?;
    println!("{COMMANDS}");

    for line in io::stdin().lock().lines() {
        let line = line?;
        let words: Vec<_> = line.split_whitespace().collect();
        match words.as_slice() {
            ["pause"] => handle.pause(),
            ["resume"] => handle.resume(),
            ["volume", value] => {
                let volume = value.parse()?;
                handle.set_volume(volume)?;
                config.volume = volume;
            }
            ["mute"] => bus.mute(),
            ["unmute"] => bus.unmute(),
            ["loop", value @ ("on" | "off")] => {
                config.looping = *value == "on";
                handle.set_looping(config.looping);
            }
            ["stop"] => handle.stop(),
            ["play"] => {
                handle.stop();
                handle = music.play_with_config(config)?;
            }
            ["status"] => println!(
                "playing={} paused={} stopped={} cursor={} frames muted={}",
                handle.is_playing(),
                handle.is_paused(),
                handle.is_stopped(),
                handle.cursor_frames(),
                bus.is_muted(),
            ),
            ["quit"] => break,
            _ => println!("{COMMANDS}"),
        }
        common::check_background(&audio)?;
    }
    handle.stop();
    common::check_background(&audio)
}
