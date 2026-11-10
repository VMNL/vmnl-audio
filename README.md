# vmnl_audio

Independent audio domain with a private CPAL backend. Control defaults to manual;
`thread(true)` explicitly enables the VMNL control worker.

- [Public API, usage, defaults, and costs](docs/api/reference/audio.md)
- [Audio architecture and acceptance contract](docs/audio.md)
- [Build prerequisites](docs/build.md)
- [Tests and qualification limits](docs/testing.md#audio-tests)
- [Manual release policy](docs/deployment.md)

Use `vmnl_audio` directly. This repository contains one standalone Cargo package;
it does not require another VMNL checkout. Generate item-level Rustdoc with
`cargo doc --no-deps`.
