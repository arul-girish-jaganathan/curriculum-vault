# Pointers in declarators

## Core idea
In a declarator, `*` introduces pointer structure. Qualifiers attached to the pointer and qualifiers attached to the pointed-to type are different contracts: `int * const p` and `const int *p` do not mean the same thing.

## Embedded consequences
Pointer qualifiers influence driver APIs, MMIO access wrappers, callback storage, DMA buffers, and ownership conventions. A declaration should make it clear whether the address may change, whether the object may be modified through the pointer, and whether the pointer participates in a shared interface.

## Common traps
- Confusing top-level and pointed-to `const`.
- Casting away qualifiers to satisfy an incompatible API.
- Assuming pointer representation or size is universally fixed.
- Treating a pointer as a mere integer address without respecting provenance, alignment, and object lifetime.

## Verification
Use compiler diagnostics for incompatible pointer types and qualifier loss. Inspect ABI documentation when a pointer crosses a binary boundary, and test MMIO/DMA code on the actual memory system rather than assuming host behavior.

## Staff-level takeaway
Pointer syntax is the surface of a deeper contract involving object identity, access permissions, lifetime, alignment, and ABI representation.
