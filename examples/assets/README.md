# Synthetic audio

`effect.wav` (200 ms) and `music.wav` (8 s) are original synthetic triangle-wave
signals distributed under this repository's [MIT license](../../LICENSE).
Both contain mono, little-endian PCM16 at 22,050 Hz. They contain no imported
recordings. They are demonstration inputs, not listening-quality references.

From the repository root, regenerate with `python3 tools/generate_example_audio.py`;
verify byte equality without writing with the same command plus `--check`.
The generator uses Python's standard library and integer arithmetic, including
the envelope and note sequence, so it does not depend on floating-point math libraries.
