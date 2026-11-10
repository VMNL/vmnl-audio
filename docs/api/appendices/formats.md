# Formats and units

| Input | Adapter | Restrictions |
|---|---|---|
| WAV | hound | Supported integer PCM/float32 WAV; actual NaN/Inf rejected. |
| MP3 | minimp3 | Decoded mono/stereo only. |
| OGG/Vorbis | lewton | Chains must retain initial sample rate and channels. |
| FLAC | claxon | Decoded mono/stereo only. |

Source rate must be nonzero. Sources convert to interleaved stereo at the resolved
device rate. Finite float32 WAV amplitudes outside `[-1, 1]` are accepted without
source clipping; interpolation preserves finite PCM or returns `DecoderFailed`.
Only final mixed output is clamped to `[-1, 1]`. Sound validates the whole uncached
source on load; music errors may appear on prefill or later refill.

Streaming uses exact integer phase: N source frames at rate S converted to rate T
produce `ceil(N*T/S)` frames independently of read sizes. End interpolation retains
the final sample. This is decoded PCM accounting, not encoder-delay or container
padding/timestamp qualification.

Rates are Hz; gains are linear multipliers, not dB; cursors are consumed PCM frames
at device rate, not source samples or hardware time. Source paths are retained
without canonicalization. Output is currently exactly two channels.
