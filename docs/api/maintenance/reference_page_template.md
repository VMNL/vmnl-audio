# Reference page conventions

Each canonical audio item page must explain:

1. Role, experimental maturity, actual public paths and local Rustdoc link.
2. Every public field/variant/inherent method and relevant explicit or derived
   trait implementation; spell each member as a separate backticked identifier.
3. Defaults, units, valid ranges and validation timing.
4. Ownership, resource lifetime, threads, allocations, locks and blocking I/O where applicable.
5. Failure/recovery behavior and unsupported policies.
6. A minimal tested example and related types/workflows/evidence.

Use compact shared sections when a value type has no device/threads/errors. Do not
add graphics/Vulkan requirements to audio. Rustdoc owns exact signatures; link it
rather than maintaining a competing signature inventory. Blanket impls are omitted.
The generated snapshot retains explicit/derived and auto traits for review.

One canonical page covers identity-based reexports, listing other public paths in
the symbol index. Distinct IDs remain distinct even if names match. Token presence
checks prevent accidental omissions; they do not prove the prose correct.
