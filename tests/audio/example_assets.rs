// SPDX-FileCopyrightText: 2026 VMNL contributors
// SPDX-License-Identifier: MIT

//! Shipped examples remain decodable with the package's own WAV dependency.

#[test]
fn bundled_wavs_have_the_documented_shape_and_duration() {
    for (name, frames) in [("effect.wav", 4_410), ("music.wav", 176_400)] {
        let path = std::path::Path::new(env!("CARGO_MANIFEST_DIR"))
            .join("examples/assets")
            .join(name);
        let mut reader = hound::WavReader::open(path).expect("bundled WAV opens");
        let spec = reader.spec();
        assert_eq!(spec.channels, 1);
        assert_eq!(spec.sample_rate, 22_050);
        assert_eq!(spec.bits_per_sample, 16);
        assert_eq!(spec.sample_format, hound::SampleFormat::Int);
        assert_eq!(reader.duration(), frames);
        let samples: Vec<_> = reader
            .samples::<i16>()
            .collect::<Result<_, _>>()
            .expect("valid PCM16");
        assert!(samples.iter().any(|sample| *sample != 0));
        assert_eq!(samples.first(), Some(&0));
        assert_eq!(samples.last(), Some(&0));
    }
}
