# Build

## Prerequisites

- Rust matching or newer than the `rust-version` in the root `Cargo.toml` (1.87).
- Cargo and the platform's Rust linker/toolchain.
- A C compiler for the MP3 decoder dependency.
- On Linux, `pkg-config` and ALSA development headers and libraries, including for
  device-independent tests.

Linux package names include `libasound2-dev` on Debian/Ubuntu, `alsa-lib-devel` on
Fedora/RHEL and `alsa-lib` on Arch. Check discovery without opening a device:

```sh
pkg-config --exists alsa
```

## Standalone package

Run from this repository's root. Cargo checks need no documentation tools:

```sh
cargo build --all-targets --locked
cargo doc --no-deps --locked
```

The root manifest owns its metadata, lints and build profiles. No parent Cargo
workspace, VMNL checkout, Vulkan, GLFW or shaderc is required.

## Explicit documentation-tool setup

The documentation pipeline additionally needs Python 3.10+, Bash, curl, tar,
gzip, sha256sum and the pinned toolchain/tools below. Installing these is an
explicit preparation step, never a side effect of a check:

| Tool | Version / purpose |
|---|---|
| Just | 1.57.0 / recipes |
| mdBook | 0.5.4 / book and snippets |
| cargo-public-api | 0.52.0 / public snapshot |
| lychee | 0.24.2 / offline local links/fragments |
| Rust nightly | nightly-2026-03-12 / API inventory only |

Install the nightly explicitly if missing; this does not select it for regular
checks. Then prepare repository-local tools (automatic bootstrap: Linux x86_64):

```sh
rustup toolchain install nightly-2026-03-12 --profile minimal
bash tools/api_docs_tools.sh
export PATH="$PWD/target/api-tools/bin:$PATH"
just --list
```

The script installs under `target/api-tools/`, verifies pinned archive checksums
and checks versions. It never installs host packages or changes the default Rust
toolchain. On other documentation hosts, build the same versions explicitly with
`cargo install --locked --root target/api-tools --version VERSION NAME` (package
names: `just`, `mdbook`, `cargo-public-api`, `lychee`) using a compatible compiler;
the checked documentation CI environment is Linux. Core Rust checks work without
this bootstrap on all target platforms.

`Justfile` puts local tools first. `docs-api-check` fails for absent/wrong versions;
only `docs-api-update` intentionally rewrites tracked inventories. Network access
is needed for initial Cargo dependencies and tool preparation; API extraction
then uses Cargo offline with its own target directory. Regular Rustdoc/snippets
use the chosen stable/MSRV compiler, not the API nightly. The docs pipeline expects
the repository-local `target/` directory (no custom `CARGO_TARGET_DIR`).

See the single ordered completion contract in [CONTRIBUTING](../CONTRIBUTING.md#before-submission).
The built book and Rustdoc, with their source-relative links, are staged together
at `target/documentation/index.html` and uploaded by CI. This is not a deployment.

See [tests](testing.md) for device-independent and native commands and
[deployment](deployment.md) for package verification and manual releases.
