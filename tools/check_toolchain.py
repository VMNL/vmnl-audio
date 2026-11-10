#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 VMNL contributors
# SPDX-License-Identifier: MIT

"""CI guard against silently running checks with another installed compiler."""

import os
import subprocess

selected = os.environ["RUSTUP_TOOLCHAIN"]
actual = subprocess.check_output(["rustc", "--version", "--verbose"], text=True)
explicit = subprocess.check_output(["rustup", "run", selected, "rustc", "--version", "--verbose"], text=True)
print(actual)
if actual != explicit:
    raise SystemExit(f"selected compiler differs from {selected}")
release = next(line.removeprefix("release: ") for line in actual.splitlines() if line.startswith("release: "))
if (selected == "1.87.0" and release != selected) or (selected == "stable" and "-" in release):
    raise SystemExit(f"unexpected release {release} for {selected}")
expected_host = os.environ.get("VMNL_EXPECTED_HOST")
if expected_host and f"host: {expected_host}\n" not in actual:
    raise SystemExit(f"unexpected compiler architecture, expected {expected_host}")
