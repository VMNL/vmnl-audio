# Audio extraction provenance

Audio developed in [VMNL/vmnl#84](https://github.com/VMNL/vmnl/pull/84) was
extracted without merging that PR or rewriting either repository's main branch.
The [machine-readable record](provenance.json), [full commit map](commit-map.tsv)
and [38 retained commits](retained-commits.tsv) are durable migration evidence.

| Boundary | Commit |
|---|---|
| Frozen source `feat/miniaudio-wrapper-clean` | `6880cd632a922e2d187e126ae2f86ee2eeafbbac` |
| Filtered history head | `412a79471f013483fb5dbd61059046916021e82b` |
| Existing destination initial commit | `db4d2cae9da8afe9e4139e271b39666dc89eb608` |
| Import merge preserving both histories | `d977224e580e5b3b6020aba6af5660d43c089f0e` |
| Standalone root-package adaptation | `31f6db3637c533ca1bf6fe9be00a328e0a6b335f` |

`git-filter-repo v2.47.0`, pinned upstream commit
`6f79afc8c90c592a3052e6cc53c2ca8907515bca`, selected:

```text
crates/vmnl_audio/
crates/vmnl_native/src/audio/
tests/audio/
docs/audio.md
docs/miniaudio_wrapper.md
docs/api/reference/audio.md
LICENSE
```

The earlier `vmnl_native` location is required to preserve the first audio commits;
path filtering does not automatically follow renames. Filtering retained 38 of
281 examined source commits and rewrote hashes. Null new hashes in the full map
mean the source commit was dropped as irrelevant/empty, not lost retained history.
Commit authors, committers, dates and messages were checked for all retained commits;
56 selected tip files matched modes/blob contents before the root-path adaptation.

The import used a merge with unrelated histories, keeping the destination's initial
commit as one parent and the filtered history as the other. The later root move
changed package metadata and harness paths; `src/audio` runtime files stayed byte
identical. Git history does not carry GitHub reviews, comments or issue state;
the original PR remains the discussion record. No personal working-tree files or
unrelated graphics changes were imported.

For a clone with this history, `git log --all -- docs/history/commit-map.tsv`
locates this record. Use the second map column to inspect a retained rewritten
commit with `git show <new-sha>`; use the first against the original repository.
After the source move, use `git log --follow -- src/audio/device.rs` for one file.

The [miniaudio draft](miniaudio_wrapper.md) is historical; the current backend is CPAL.
