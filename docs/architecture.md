# Architecture

`vmnl_audio` is one independently consumable Rust package. Applications import its
types directly. There is no aggregate facade, graphics context, application-loop
owner, or public audio singleton. CPAL and codec adapters remain private.

```text
application -> vmnl_audio
                 AudioDevice (output stream owner)
                 control: caller update() OR opt-in worker
                 resources -> independent playback instances
                 prepared PCM -> CPAL data callback -> output
```

`src/audio/` implements the domain; `src/lib.rs` exports its types. Root reexports
and `audio` paths refer to the same types. These are package entrypoints, not an
extra facade package. Their identity is checked in the generated inventories.

`Sound` caches complete decoded PCM. `Music` opens a decoder and bounded PCM ring
per playback. Cloned handles control one instance; resources create independent
instances. The device alone keeps native output alive. Loading, refill and cleanup
run on the control side. The callback consumes prepared PCM and mixes final output.

Manual control is the default. `.thread(true)` explicitly enables the control
worker; CPAL executes output independently in both modes. Neither mode owns the
application loop. A failed worker requires a new device, with no hidden fallback.

This migration preserves the implementation and API. Native behavior, listening
and realtime deadlines require separate qualification under the [audio contract](audio.md).
Networking, graphics, engine services and automatic releases are outside this package.
