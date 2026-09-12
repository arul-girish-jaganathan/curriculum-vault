# 01: Structure Layout

## Definition
Structure layout refers to the physical arrangement of structure members in linear memory. In ISO C, members are allocated in declaration order with monotonically increasing addresses. Compilers insert padding bytes between members (internal padding) and after the final member (trailing padding) to satisfy the natural alignment constraints of each individual member and the structure as a whole.

## Scope and Boundaries
Covers: Member ordering, natural alignment constraints, internal padding, trailing padding, `sizeof` calculation, and `offsetof` macro.
Does not cover: Dynamic packing pragmas (see `12_Protocol_and_register_layouts`), flexible array members (see `06_Flexible_array_members`), or bitfields (see `02_Structure_members`).

## Why Does It Exist
Modern microprocessors (especially 32-bit and 64-bit architectures like ARM Cortex-M, RISC-V, and x86) access memory across specific bus boundaries (2, 4, 8 bytes). Unaligned memory accesses can cause CPU hard faults, bus pipeline stalls, or require multiple bus cycles. Structure padding ensures that every member begins at an address satisfying its architecture-mandated natural alignment while maintaining an aggregate alignment suitable for contiguous array indexing.

## Mechanism and Language Rules
1. **Monotonic Order:** ISO C requires `&(s.member_b) > &(s.member_a)` if `member_b` is declared after `member_a`.
2. **First Member Address:** The address of the first member equals the address of the structure itself (`(void *)&s == (void *)&(s.first_member)`). There is no leading padding.
3. **Internal Padding:** Bytes inserted between members to align the subsequent member to a multiple of its natural alignment `alignof(T)`.
4. **Trailing Padding:** Bytes inserted after the last member so that `sizeof(struct S)` is an exact integer multiple of the structure's overall alignment (`max(alignof(member))`). This guarantees array elements `arr[i]` maintain correct alignment.
5. **Offsetof Macro:** `<stddef.h>` defines `offsetof(type, member)`, returning the byte offset of a member from the start of the structure as a `size_t`.

## Examples
```c
#include <stddef.h>
#include <stdint.h>
#include <assert.h>

/* Naive layout: 12 bytes on a 32-bit architecture */
struct NaiveLayout {
    uint8_t  flag;     /* Offset 0, size 1, 3 padding bytes */
    uint32_t counter;  /* Offset 4, size 4 */
    uint16_t id;       /* Offset 8, size 2, 2 trailing padding bytes */
};

/* Optimized layout: 8 bytes on a 32-bit architecture */
struct OptimizedLayout {
    uint32_t counter;  /* Offset 0, size 4 */
    uint16_t id;       /* Offset 4, size 2 */
    uint8_t  flag;     /* Offset 6, size 1, 1 trailing padding byte */
};

static_assert(sizeof(struct NaiveLayout) == 12, "Unexpected NaiveLayout size");
static_assert(sizeof(struct OptimizedLayout) == 8, "Unexpected OptimizedLayout size");
static_assert(offsetof(struct OptimizedLayout, id) == 4, "Offset mismatch");
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- **Padding Contents:** The byte values of padding areas are indeterminate and unspecified. Two structs containing identical member values are not guaranteed to match byte-for-byte under `memcmp`.
- **Implementation Alignment:** The specific natural alignment requirements for standard types are implementation-defined by the Target ABI.

## Edge Cases and Failure Modes
- **Memcmp False Negatives:** Using `memcmp(&a, &b, sizeof(struct S))` to test equality will yield false negatives because indeterminate padding bytes may differ.
- **Array Stride Bloat:** Poor member ordering causes trailing padding that multiplies across large array allocations, exhausting constrained SRAM.

## Embedded Implications
- **SRAM Exhaustion:** In bare-metal systems with 16KB-64KB SRAM, unoptimized struct ordering in tables/pools can silently waste 20-40% of available memory on padding.
- **Bus Faults:** Mapping an unpadded struct over hardware registers or packed wire packets without explicit packing attributes triggers misalignment faults.

## Firmware Review Angle
- **Reorder by Decreasing Alignment:** Order fields from largest alignment requirement to smallest (e.g., `uint64_t` -> `uint32_t` -> `uint16_t` -> `uint8_t`) to eliminate internal padding.
- **Enforce `static_assert`:** Require static assertions on `sizeof` and `offsetof` for any structure interacting with DMA, IPC, or external storage.

## Compiler, ABI, and Toolchain Implications
- ARM AAPCS requires aggregate alignment equal to the maximum alignment of its members.
- LTO cannot reorder structure fields; the C standard forbids compiler reordering of struct fields.

## Performance, Memory, Timing, and Power
- Optimal alignment enables single-cycle 32-bit load/store instructions (`LDR`/`STR`).
- Reduced memory footprint improves L1 data cache line utilization and reduces flash/RAM power consumption.

## Verification / Debugging
- Use compiler flags `-Wpadded` to detect unexpected padding insertion.
- In GDB: `ptype /o struct OptimizedLayout` displays offsets and hole sizes.

## Safety, Security, and Reliability
- **Information Leak (CWE-200):** Copying an uninitialized struct to an external interface (network, user space, flash) leaks raw stack/heap data contained in padding bytes. Always `memset` before exporting.
- MISRA C:2012 Rule 19.2 advises strict awareness of overlapping/padded types.

## Trade-offs and Alternatives
- **Manual Ordering vs Packed:** Reordering fields preserves natural alignment and execution speed without incurring the bus-penalty or compiler code-bloat of `__attribute__((packed))`.

## Staff-Level Takeaway
Never rely on visual inspection to determine struct size. Reorder fields by descending alignment size and lock critical layouts with compile-time assertions (`_Static_assert`). Treat padding bytes as security liabilities.

## Related Concepts
- `00_Chapter_Index`
- `02_Structure_members`
- `12_Protocol_and_register_layouts`
