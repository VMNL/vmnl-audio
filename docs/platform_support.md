# Platforms

The CI matrix targets these GitHub-hosted runner/compiler combinations:

| Runner | Architecture | Rust |
|---|---|---|
| `ubuntu-24.04` | x86_64 Linux GNU | 1.87.0 and stable |
| `macos-15` | aarch64 Apple Darwin | 1.87.0 and stable |
| `windows-2022` | x86_64 Windows MSVC | 1.87.0 and stable |

These are the architectures supplied by the [official runner images](https://github.com/actions/runner-images).
The matrix builds all examples/probes and runs device-independent tests and
doctests. Compiler/host guards verify the actual selection. Passing jobs are
evidence only for their recorded commit, runner and compiler; a configured matrix
alone is not evidence of a successful run. Intel macOS is not covered by this matrix.

Native probes are compiled but never executed on hosted runners. Native output
availability, disconnection/recovery, shutdown timing, listening quality and callback
deadlines remain separate qualification tasks. Consult [testing](testing.md) before
running devices; Linux builds require ALSA development files even for headless tests.
No Vulkan, GLFW or display server is required by this package.

## Local native evidence

The [qualification record](qualification.md) reports Linux ALSA/PipeWire startup,
control and nominal device-drop scenarios. It is scoped to its source checksums,
host and workload. It does not qualify Windows/macOS native output, human listening,
backend disconnection/recovery or realtime deadlines.
