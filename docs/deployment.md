# Deployment

Releases of `vmnl_audio` are manual. Automation must not create release tags,
GitHub releases or crates.io publications.

No public release has been prepared in this repository. The `0.1.0` manifest
version is development metadata. The first publication requires review of the
public API, defaults, compatibility policy and documented qualification limits.

Before publication, complete the applicable build, lint, documentation and test
checks, inspect `cargo package --list`, and successfully run
`cargo publish --dry-run --locked`. A dry-run validates packaging and compilation;
it neither publishes nor qualifies native devices or realtime behavior.
