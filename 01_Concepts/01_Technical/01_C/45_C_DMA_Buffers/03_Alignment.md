# Alignment

> Canonical C topic note — Chapter 45. DMA alignment must satisfy both the C object's alignment requirements and the hardware's address, descriptor, and cache-line requirements.

## Definition
C alignment determines which addresses are valid for objects of a given type. DMA hardware can impose additional constraints such as descriptor alignment, buffer alignment, burst boundaries, or cache-line requirements.

## Mechanism and language rules
An object declared with its type has an alignment requirement; `_Alignof` can query it. Converting a pointer does not make the pointed-to storage correctly aligned. Accessing an object through an improperly aligned lvalue can violate C requirements and can also fault on the target.

### What to reason about
- What alignment does the C type require?
- What alignment does the DMA engine require?
- Does the linker guarantee placement alignment?
- Does the buffer cross cache-line or burst boundaries?
- Is a packed structure being used as a DMA descriptor?

## Embedded implications
Misalignment can cause bus faults, slower accesses, split DMA transactions, or hardware rejection. Descriptor rings often require alignment stronger than the natural alignment of their C fields.

### Firmware review angle
Encode alignment in declarations or linker placement rather than relying on incidental addresses. Check section placement and map files for DMA pools.

## Edge cases and failure modes
- Stack pointer happens to be aligned on one build but not another.
- Packed descriptor violates hardware alignment.
- Cache-line sharing causes unintended maintenance effects.
- Address alignment is correct but length/burst constraints are not.

## Example pattern
```c
#include <stdint.h>

struct dma_desc {
    uint32_t addr;
    uint32_t length;
    uint32_t flags;
};

_Alignas(32) static struct dma_desc desc;
```
The `32` is illustrative; production alignment must come from the hardware contract.

## Verification / debugging
Check `_Alignof`, `sizeof`, and actual addresses. Inspect linker maps and section placement. Test boundary addresses and cache-line crossings, not just naturally aligned allocations.

Staff-level questions: Which alignment requirement is strongest? Who guarantees it—compiler, linker, allocator, or driver? What happens when a buffer crosses a cache line?

## Staff-level takeaway
DMA alignment is an **intersection of C, hardware, linker, and cache constraints**. Encode the strongest requirement explicitly and verify actual placement rather than assuming type alignment is enough.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
