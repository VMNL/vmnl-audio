#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 VMNL contributors
# SPDX-License-Identifier: MIT

"""Run only --help (never native playback), with bounded subprocess execution."""

import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ("play_sound", "stream_music", "playback_controls", "manual_control")


def main() -> None:
    metadata = subprocess.check_output(["cargo", "metadata", "--no-deps", "--format-version", "1"], cwd=ROOT, text=True)
    import json
    target = Path(json.loads(metadata)["target_directory"])
    suffix = ".exe" if os.name == "nt" else ""
    for example in EXAMPLES:
        output = subprocess.run([str(target / "debug/examples" / (example + suffix)), "--help"],
                                stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=10, check=True)
        if "Usage:" not in output.stdout or output.stderr:
            raise SystemExit(f"unexpected --help output for {example}: {output}")
        print(f"{example} --help: PASS (no device construction)")


if __name__ == "__main__":
    main()
