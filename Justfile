set shell := ["bash", "-euo", "pipefail", "-c"]
export PATH := justfile_directory() / "target/api-tools/bin" + ":" + env("PATH")

default:
    @just --list

# Explicit setup only; ordinary checks never install tools.
tools-prepare:
    bash tools/api_docs_tools.sh

build:
    cargo build --all-targets --all-features --locked

check-fmt:
    cargo fmt --all -- --check

check-clippy:
    cargo clippy --all-targets --all-features --locked -- -D warnings

doctest:
    cargo test --all-features --doc --locked

docs:
    RUSTDOCFLAGS="-D warnings" cargo doc --all-features --no-deps --locked

# Intentional source mutation; review the generated diff.
docs-api-update:
    python3 tools/api_docs.py update

docs-api-check:
    python3 tools/docs_check.py

test-tools:
    python3 -m unittest discover -s tools/tests
    python3 tools/generate_example_audio.py --check

test-unit:
    cargo test --lib --locked

test-audio:
    cargo test --test audio --locked

test-examples:
    python3 tools/check_examples.py

test-native-compile:
    cargo test --test audio-backend --no-run --locked

# Opt-in: opens the native output device. Never used by hosted CI.
test-native:
    cargo test --test audio-backend --locked -- --ignored --test-threads=1

# Launch interactive controls by default; pass an example and optional file/--help.
[positional-arguments]
run example="playback_controls" *args:
    cargo run --locked --example "$1" -- "${@:2}"

package:
    python3 tools/check_package.py
