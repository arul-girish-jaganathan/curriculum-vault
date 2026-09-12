# Memory barriers

> Canonical C topic note — Chapter 45. Barriers constrain visibility and ordering at different layers: compiler, CPU memory model, cache/coherency system, and device/bus fabric. They are not interchangeable.

## Definition
A compiler barrier constrains compiler motion; a CPU memory barrier constrains hardware memory ordering; a DMA/device barrier establishes ordering needed for a device or bus master. ISO C atomics define language-level ordering for atomic operations but do not automatically express every device-specific requirement.

## Mechanism and language rules
A release store can publish prior ordinary writes to an acquiring C thread. For DMA, the descriptor and buffer may require cache clean plus a CPU/device barrier before the DMA start register is written. Completion may require the reverse sequence before CPU consumption.

### What to reason about
- Which observer must see the writes?
- Is the problem compiler ordering, CPU ordering, cache visibility, or all three?
- Is the DMA engine coherent?
- Does the architecture require a device memory barrier?
- Is the barrier stronger than necessary and therefore costly?

## Embedded implications
Incorrect ordering can cause hardware to observe a descriptor before its fields are fully visible. Excessive barriers can increase latency and reduce throughput, especially on weakly ordered multicore systems.

### Firmware review angle
Use architecture/vendor primitives through a small abstraction. Document exactly which visibility guarantee each helper provides rather than naming every operation generically “memory barrier.”

## Edge cases and failure modes
- `volatile` is used as a supposed DMA barrier.
- Compiler barrier is mistaken for cache maintenance.
- CPU barrier is used without cleaning dirty cache lines.
- Descriptor ownership is changed before descriptor fields are visible.

## Example pattern
```c
prepare_descriptor(desc);
cache_clean(desc, sizeof *desc);
device_write_barrier();
DMA_START = 1U;
```
All operations are platform-specific except the ordinary C assignment; the sequence illustrates the conceptual boundary.

## Verification / debugging
Use stress tests that maximize CPU/DMA overlap. Inspect architecture documentation and generated code, and use hardware trace or logic analyzers where visibility timing must be demonstrated.

## Staff-level takeaway
When debugging DMA ordering, ask **which layer is failing**: compiler, C memory model, CPU, cache, or device fabric. Apply the smallest barrier that establishes the required contract.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
