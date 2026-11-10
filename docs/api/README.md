# vmnl_audio API

This book describes direct use of the independent `vmnl_audio` package. All types
are experimental until the first publication. Start with [first sound](workflows/first_sound.md).

- [Concepts](concepts/resources.md): resources, instances, control and costs.
- [Workflows](workflows/first_sound.md): automatic playback first, manual control when needed.
- [Reference](reference/audio.md): one canonical page per public type/alias.
- [Appendices](appendices/formats.md): formats, defaults, units and evidence limits.
- [Maintenance](maintenance/validation.md): inventories and documentation checks.

Exact signatures and local contracts belong to [Rustdoc](../../target/doc/vmnl_audio/index.html).
The [audio acceptance contract](../audio.md) defines internal invariants and the
remaining qualification target. This book does not promise native device support
or realtime performance merely from deterministic tests.
