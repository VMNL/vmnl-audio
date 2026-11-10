#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 VMNL contributors
# SPDX-License-Identifier: MIT

"""Verify packaged sources/assets and Cargo's archive build, without publishing."""

import argparse
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = {
    "LICENSE", "src/lib.rs", "examples/assets/effect.wav", "examples/assets/music.wav",
    "tests/audio/fixtures/tiny.mp3", "tests/audio/fixtures/tiny.ogg", "tests/audio/fixtures/tiny.flac",
}


def validate_files(files: set[str]) -> None:
    missing = REQUIRED - files
    unwanted = sorted(path for path in files if path.startswith(("target/", ".git/")) or "__pycache__" in path)
    if missing or unwanted:
        raise ValueError(f"invalid package inventory: missing={sorted(missing)}, unwanted={unwanted}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--allow-dirty", action="store_true", help="explicit local pre-commit verification")
    args = parser.parse_args()
    command = ["cargo", "package", "--locked"] + (["--allow-dirty"] if args.allow_dirty else [])
    files = set(subprocess.check_output([*command, "--list"], cwd=ROOT, text=True).splitlines())
    validate_files(files)
    required_sources = {str(path.relative_to(ROOT)) for directory in ("examples", "tests/audio/fixtures")
                        for path in (ROOT / directory).rglob("*") if path.is_file()}
    if missing := required_sources - files:
        raise ValueError(f"packaged examples/fixtures missing: {sorted(missing)}")
    subprocess.run(command, cwd=ROOT, check=True)
    print(f"Package: {len(files)} files; required assets/fixtures included, archive build passed")


if __name__ == "__main__":
    main()
