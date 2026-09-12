# 11: Pools and Arenas

## Definition
Pool and arena allocators are specialized memory management structures designed to allocate memory from a pre-allocated contiguous buffer in $O(1)$ constant time, completely eliminating external fragmentation and individual deallocation overhead.

## Scope and Boundaries
- **Covers:** Fixed-size block memory pools, bump-pointer (arena) allocators, bulk reset semantics, and deterministic allocation patterns.
- **Does not cover:** General-purpose variable-size heap allocators ([[01_malloc]]) or garbage collection.

## Why Does It Exist
General-purpose heap allocators (`malloc`/`free`) are slow, non-deterministic, and prone to fragmentation:
- **$O(1)$ Performance:** Pool and arena allocations involve simple pointer arithmetic or free-list popping, executing in constant time with zero search overhead.
- **Zero Fragmentation:** Fixed-size pools eliminate external fragmentation entirely because all blocks are identical in size.
- **Bulk Deallocation:** Arena allocators release entire memory regions instantly by resetting a single offset pointer, eliminating the need to call `free` on individual objects.

## Mechanism and Language Rules
- **Arena / Bump Allocator:** Allocates memory sequentially from a pre-allocated buffer by advancing a pointer (`offset += size`). Individual `free` calls are unsupported; instead, the entire arena is reset at once (`arena_reset()`).
- **Fixed-Size Block Pool:** Divides a pre-allocated memory chunk into equal-sized blocks linked together in a free-list. `pool_alloc()` pops a block; `pool_free()` pushes it back onto the free-list in $O(1)$ time.

## Examples
```c
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>

#define ARENA_SIZE 4096

typedef struct {
    uint8_t buffer[ARENA_SIZE];
    size_t offset;
} arena_t;

void arena_init(arena_t *arena) 
{
    arena->offset = 0;
}

void *arena_alloc(arena_t *arena, size_t size) 
{
    /* Align size to 8-byte boundary */
    size_t aligned_size = (size + 7) & ~7;

    if (arena->offset + aligned_size > ARENA_SIZE) {
        return NULL; /* Arena exhausted */
    }

    void *ptr = &arena->buffer[arena->offset];
    arena->offset += aligned_size;
    return ptr;
}

void arena_reset(arena_t *arena) 
{
    arena->offset = 0; /* Instantly frees all allocated memory simultaneously */
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- **Undefined Behavior (Use-After-Arena-Reset):** Accessing memory allocated from an arena after calling `arena_reset()` is a severe use-after-free bug.
- **Undefined Behavior (Arena Overflow):** Requesting more bytes than remaining capacity in an arena without checking returns out-of-bounds pointers if unchecked.

## Edge Cases and Failure Modes
- **Lifetime Scope Mismatch:** Arenas are ideal for temporary, phase-based allocations (e.g., frame rendering, request parsing) where all objects share the exact same lifecycle and can be destroyed together. Using arenas for objects with disparate lifecycles causes premature destruction or memory retention.

## Embedded Implications
- **Real-Time Determinism:** Pools and arenas provide deterministic, bounded execution times required for hard real-time embedded systems, completely replacing non-deterministic heap allocators.
- **Zero Fragmentation Guarantee:** Eliminates external fragmentation entirely in long-running embedded firmware.

## Firmware Review Angle
- **Audit Arena Resets:** Ensure that no pointers into an arena survive an `arena_reset()` call.
- **Check Block Pool Sizing:** Verify that fixed-size pools are sized correctly for maximum concurrency to prevent exhaustion faults.

## Compiler, ABI, and Toolchain Implications
- **Static Buffer Storage:** Arenas and pools are typically backed by statically allocated global buffers (`static uint8_t pool[SIZE];`), bypassing OS heap dependencies entirely.

## Performance, Memory, Timing, and Power
- **Lightning Fast:** Bump allocation is merely an integer addition (~2 CPU instructions), making it orders of magnitude faster than `malloc`.
- **Zero Metadata Overhead:** Unlike `malloc`, which prepends metadata headers to every chunk, arena/pools have zero per-allocation metadata overhead.

## Verification / Debugging
- **Bounds Checking:** Instrument arena allocators to verify that allocation requests never exceed buffer boundaries.
- **Sanitizer Poisoning:** Poison arena memory upon reset to immediately catch use-after-reset bugs.

## Safety, Security, and Reliability
- **Safety Certification:** Highly favored in safety-critical systems (DO-178C, ISO 26262) because their deterministic memory management model is easy to verify and analyze.

## Trade-offs and Alternatives
- **Arena vs. General Heap:** Arena allocation is ultra-fast and fragmentation-free but requires grouped lifecycles and lacks individual object deallocation; general heap supports arbitrary individual frees but suffers from fragmentation and slowness.

## Staff-Level Takeaway
For high-performance loops, request handlers, game engines, and embedded firmware, replace general-purpose `malloc`/`free` with arena or fixed-size pool allocators whenever objects share common lifecycles. They deliver $O(1)$ execution speed, zero fragmentation, and instant bulk deallocation.

## Related Concepts
- [[00_Chapter_Index]]
- [[01_malloc]]
- [[04_free]]
- [[09_Memory_fragmentation]]
- [[12_Embedded_allocation_policy]]
