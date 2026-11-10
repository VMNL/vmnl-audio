#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 VMNL contributors
# SPDX-License-Identifier: MIT

"""Generate byte-reproducible PCM16 WAV examples using integer arithmetic only."""

from __future__ import annotations

import argparse
import io
from pathlib import Path
import struct
import wave

ROOT = Path(__file__).resolve().parents[1]
RATE = 22_050
ASSETS = {"effect.wav": RATE // 5, "music.wav": RATE * 8}


def wav_bytes(frames: int, *, music: bool) -> bytes:
    samples = bytearray()
    notes = (220, 275, 330, 440, 330, 275, 220, 165)
    for frame in range(frames):
        note = frame // RATE if music else 0
        frequency = notes[note % len(notes)] if music else 660
        phase = (frame * frequency * 65_536 // RATE) % 65_536
        triangle = 32_767 - 2 * abs(phase - 32_768)
        # Integer fade at each note boundary avoids discontinuous full-scale steps.
        position = frame % RATE if music else frame
        length = RATE if music else frames
        fade = RATE // 100
        envelope = min(position, length - 1 - position, fade)
        sample = triangle * envelope // (fade * 5)
        samples.extend(struct.pack("<h", sample))
    output = io.BytesIO()
    with wave.open(output, "wb") as wav:
        wav.setparams((1, 2, RATE, 0, "NONE", "not compressed"))
        wav.writeframes(samples)
    return output.getvalue()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="verify without writing")
    args = parser.parse_args()
    directory = ROOT / "examples" / "assets"
    for name, frames in ASSETS.items():
        path = directory / name
        expected = wav_bytes(frames, music=name == "music.wav")
        if args.check:
            if not path.is_file() or path.read_bytes() != expected:
                raise SystemExit(f"stale or missing asset: {path}; run {Path(__file__).name}")
        else:
            directory.mkdir(parents=True, exist_ok=True)
            path.write_bytes(expected)
        print(f"{name}: {frames} frames, mono PCM16, {RATE} Hz")


if __name__ == "__main__":
    main()
