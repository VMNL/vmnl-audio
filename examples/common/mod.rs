// SPDX-FileCopyrightText: 2026 VMNL contributors
// SPDX-License-Identifier: MIT

//! Small command-line helpers; playback remains visible in each example.

#![allow(clippy::print_stdout)]

use std::error::Error;
use std::io;
use std::path::PathBuf;

use vmnl_audio::AudioDevice;

pub type ExampleResult<T = ()> = Result<T, Box<dyn Error>>;

pub fn source_path(asset: &str, description: &str) -> ExampleResult<Option<PathBuf>> {
    let arguments: Vec<_> = std::env::args_os().skip(1).collect();
    if arguments.iter().any(|arg| arg == "--help" || arg == "-h") {
        println!(
            "{description}\nUsage: [--help] [audio-file]\nThe bundled {asset} is used by default."
        );
        return Ok(None);
    }
    if arguments.len() > 1 {
        return Err(io::Error::new(
            io::ErrorKind::InvalidInput,
            "expected at most one audio file",
        )
        .into());
    }
    Ok(Some(arguments.first().map_or_else(
        || {
            PathBuf::from(env!("CARGO_MANIFEST_DIR"))
                .join("examples/assets")
                .join(asset)
        },
        PathBuf::from,
    )))
}

pub fn check_background(audio: &AudioDevice) -> ExampleResult {
    if let Some(message) = audio.take_background_error() {
        return Err(io::Error::other(message).into());
    }
    Ok(())
}
