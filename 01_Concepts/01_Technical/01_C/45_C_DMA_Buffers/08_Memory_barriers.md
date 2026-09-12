# Memory barriers

> Canonical C topic note — Chapter 45. Memory barriers constrain ordering and visibility between memory operations, but a compiler barrier, CPU memory barrier, cache operation, and device synchronization primitive solve different problems.

## Definition
A barrier establishes an ordering relationship appropriate to a particular memory system. C11 atomics define language-level ordering for participating atomic operations; platform barriers address CPU/device ordering; cache maintenance addresses stale/dirty cache state.

## Mechanism and language rules
A DMA engine is not a C thread, so the C memory model alone does not describe every device interaction. A typical publication sequence may require CPU writes to payload, a compiler/CPU/device ordering primitive, descriptor ownership update, and DMA start.

### What to reason about
- Is the other observer another C thread, an ISR, or a DMA device?
- Which memory domain is being ordered?
- Is cache coherence guaranteed?
- Is the barrier before or after ownership publication?
- Does the platform require a stronger device barrier than a normal atomic fence?

Do not insert barriers randomly. First identify the visibility guarantee that is missing.

## Embedded implications
Incorrect ordering can make a device see a descriptor before its payload or make the CPU consume a buffer before DMA writes are visible. Barriers can also have measurable latency costs.

### Firmware review angle
Use the platform's documented DMA synchronization APIs rather than hand-written assembly when available. Keep barrier semantics close to ownership-transfer code so reviewers can see the protocol.

## Edge cases and failure modes
- Compiler barrier used where hardware ordering is required.
- CPU barrier used without cache maintenance on a non-coherent system.
- Ownership bit published before descriptor fields are visible.
- Excessive barriers reduce throughput without fixing a real race.

## Example pattern
```c
prepare_descriptor(d);
DMA_SYNC_FOR_DEVICE(d);
d->owner = DMA_OWNS;
DEVICE_BARRIER();
start_dma();
```
The macros are placeholders for platform-defined primitives; their ordering semantics must come from the hardware/software platform.

## Verification / debugging
Use weak-memory stress tests where possible and inspect generated assembly. Test with caches enabled, multiple cores if applicable, and real DMA traffic. Confirm the documented barrier primitive actually covers the intended memory domain.

Staff-level questions: What observer are we ordering against? Is cache coherency involved? What exact guarantee does this barrier provide? Can ownership be encoded by a stronger primitive?

## Staff-level takeaway
“Barrier” is not one universal operation. Correct DMA synchronization requires **compiler ordering, CPU/device ordering, cache coherency, and ownership** to be treated as distinct layers.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
