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

Run from this repository's root:

```sh
cargo build --all-targets --locked
cargo doc --no-deps --locked
```

The root manifest owns its metadata, lints and build profiles. No parent Cargo
workspace, VMNL checkout, Vulkan, GLFW or shaderc is required.

See [tests](testing.md) for device-independent and native commands and
[deployment](deployment.md) for package verification and manual releases.
