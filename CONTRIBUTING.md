# Contributing

Read [coding rules](docs/INSTRUCTIONS.md), [architecture](docs/architecture.md),
and the [audio contract](docs/audio.md). Keep public contracts in Rustdoc and user
workflows in the [API book](docs/api/README.md).

## Before submission

Install prerequisites through the explicit [setup procedure](docs/build.md).
Run applicable checks in this order from the repository root:

```sh
just build
just check-fmt
just check-clippy
just doctest
just docs
just docs-api-check
just test-tools
just test-unit
just test-audio
just test-examples
just test-native-compile
just package
```

This is the single completion-order contract. Do not reorder applicable checks
without a technical reason. `build` compiles all examples and integration targets;
`test-examples` executes only `--help`, never playback. `test-native-compile` is an
explicit guard that the ignored probes still build. `test-tools` also checks the
bundled WAV bytes. `package` requires a clean checkout; for pre-commit verification
use `python3 tools/check_package.py --allow-dirty` explicitly, then rerun it clean.

Documentation-only work needs applicable snippet, structure, inventory and link
checks; Rustdoc changes also need doctests and `docs`. Public API changes update
the matrix and canonical pages, then explicitly run `just docs-api-update`, review
the generated diff and run `just docs-api-check`. Ordinary checks never update it.

Hosted CI compiles native probes without executing them. For explicit native
qualification, see [testing](docs/testing.md); record environmental prerequisites
and keep listening and realtime evidence separate. A blocked check must be reported;
continue later checks only when safe and meaningful.

## Pull request descriptions

Use exactly these headings:

```markdown
## Context

<Concrete problem and expected result>

## Changes

- <Relevant final changes>

## Validation

```

`Validation` is reserved for manual operator observations explicitly reported by
the human, labelled as native device execution or listening as appropriate.
Leave it empty when none are supplied. Automatic builds/tests belong in CI or the
delivery report; never invent operator observations or call them hardware evidence.

## Commits and releases

Use `<type>[optional scope]: <imperative lowercase description>`, maximum 72
characters for the subject, without a trailing period. Keep dependency upgrades
and unrelated runtime refactors separate. Releases, tags and publication require
explicit authorization and follow [deployment](docs/deployment.md).
