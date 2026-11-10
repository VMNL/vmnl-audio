# Resources, instances and ownership

`AudioDevice` owns native output and must remain alive. A `Sound` or `Music`
resource belongs to that device's runtime; it cannot be moved to a new device by
retaining a handle. Resource clones share their source/runtime. Every `play` call
creates an independent instance; cloned handles control the same instance.

`Sound` keeps complete decoded stereo PCM in memory. `Music` validates initial
metadata when loaded, then opens a decoder and bounded PCM ring for each play.
Music loading cannot validate failures near the end of a track. Both resources
retain shared runtime data after device destruction but cannot keep output alive.

Dropping a playback handle does not stop playback. Call `stop` explicitly if that
is the intended policy. `Stopped`, including EOF, is terminal; replay the resource
to obtain a new handle. Buses are shared controls; their clones affect the same route.

Root paths such as `vmnl_audio::Sound` and `vmnl_audio::audio::Sound` identify the
same type. They are [inventoried as reexports](../appendices/public_symbol_index.md).
No separate VMNL facade package or graphics context participates.
