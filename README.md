# vmnl_audio

Independent audio domain with a private CPAL backend. Control defaults to manual;
`thread(true)` explicitly enables the VMNL control worker.

- [Getting started](docs/getting_started.md)
- [API book: concepts, workflows and complete reference](docs/api/README.md)
- [Runnable examples and bundled synthetic WAVs](docs/examples.md)
- [Audio architecture and acceptance contract](docs/audio.md)
- [Build prerequisites](docs/build.md)
- [Tests and qualification limits](docs/testing.md#audio-tests)
- [Manual release policy](docs/deployment.md)
- [Contributing and validation order](CONTRIBUTING.md)
- [Documentation index and extraction history](docs/README.md)

Use `vmnl_audio` directly. This repository contains one standalone Cargo package;
it does not require another VMNL checkout. Generate item-level Rustdoc with
`cargo doc --no-deps`.
