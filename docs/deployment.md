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

## Preparation and current blockers

- Complete/review the import PR and first compatibility baseline; no release is
  implied by the development manifest or a draft PR.
- Review the [platform evidence](platform_support.md) at the exact candidate SHA.
  Native startup/error/shutdown, listening and realtime requirements in the
  [audio contract](audio.md) remain independent qualification work. Resolve them
  or explicitly narrow the release contract before claiming qualification.
- Check the crates.io name/ownership and registry state at publication time; no
  name reservation or publication is assumed by this repository.
- Run the [contribution checks](../CONTRIBUTING.md#before-submission), inspect
  `cargo package --list --locked`, then run `cargo publish --dry-run --locked`.
  Verify assets/fixtures/license in the archive and a standalone external client.

The manifest has registry dependencies only; there is no private VMNL dependency
to publish first. Cargo package verification proves the archive builds under the
tested environment, not that all release preconditions have been satisfied.
CI creates downloadable documentation artifacts only, never tags, GitHub releases,
Pages deployments or registry publications. All actual releases remain manual and
require explicit authorization. Before the first public release, do not create
per-change changelog entries. Establish compatibility/deprecation and release-note
policy with the first published version.
