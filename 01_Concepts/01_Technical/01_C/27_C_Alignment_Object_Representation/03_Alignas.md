# 03: Alignas

## Definition
`_Alignas` (introduced in C11) is a type specifier/qualifier that requests a stricter (larger) alignment requirement for an object than its natural type alignment. Including `<stdalign.h>` provides the convenience macro `alignas`, which expands to `_Alignas`. It allows developers to enforce alignment constraints on variables, structure members, and structure definitions.

## Scope and Boundaries
- **Covers:** `_Alignas` / `alignas` syntax, over-alignment, structure member padding control, and stack/data alignment.
- **Does not cover:** Relaxing alignment (you cannot make an alignment smaller than fundamental alignment), operator querying ([[02_Alignof]]), or dynamic memory alignment.

## Why Does It Exist
Hardware accelerators, SIMD instruction sets, and DMA controllers require data to be aligned to specific cache line or vector register boundaries:
- **SIMD Vectorization:** AVX-512 or NEON vector instructions require 32-byte or 64-byte alignments; unaligned vector loads trigger hardware exceptions or performance degradation.
- **Hardware DMA Buffers:** Ensuring receive/transmit buffers do not cross cache lines or memory page boundaries.

## Mechanism and Language Rules
- **Syntax:** `_Alignas(expression)` or `_Alignas(type-name)`.
- **Placement:** Can be applied to variable declarations, file-scope definitions, and structure member declarations.
- **Stricter Only:** You can only request an alignment that is greater than or equal to the natural alignment of the type. Requesting an alignment smaller than fundamental alignment is a constraint violation and triggers a compilation error.
- **Power of Two:** The expression passed to `_Alignas` must evaluate to a valid alignment value (a positive integer power of two).

## Examples
```c
#include <stdio.h>
#include <stdalign.h>
#include <stdint.h>

/* Force structure to align to 64-byte cache line boundary */
struct alignas(64) cache_line_packet {
    uint32_t header_id;
    uint32_t payload_len;
    uint8_t data[56];
};

int main(void) 
{
    struct alignas(64) cache_line_packet pkt;
    
    printf("Alignment of packet struct: %zu\n", alignof(struct cache_line_packet));
    printf("Address of packet instance: %p\n", (void *)&pkt);
    
    /* Verify address is a multiple of 64 */
    if ((uintptr_t)&pkt % 64 == 0) {
        printf("Packet is 64-byte cache-line aligned.\n");
    }
    
    return 0;
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- **Implementation-Defined:** Maximum supported alignment limits vary by compiler and target ABI (e.g., some environments cap maximum alignment at 4096 bytes). Requesting an alignment exceeding platform limits causes a compilation error.

## Edge Cases and Failure Modes
- **Under-Alignment Attempt:** Trying to write `alignas(1) uint64_t x;` on a 64-bit architecture where `uint64_t` requires 8-byte alignment violates C constraints, resulting in a compilation error.
- **Array Alignment:** When applied to an array (`alignas(32) int arr[10];`), the alignment applies to the **array as a whole**, meaning every element is properly aligned.

## Embedded Implications
- **DMA Buffer Safety:** Using `alignas(32)` on receive/transmit buffers prevents DMA write-back cache corruption and ensures compliance with MCU peripheral bus controller specifications.

## Firmware Review Angle
- **Audit SIMD/DMA Buffers:** Check that all high-speed DMA and cryptographic acceleration buffers are explicitly marked with `alignas()` matching hardware peripheral constraints.
- **Verify Stack Variables:** Ensure large stack buffers required by hardware drivers use `alignas()` to prevent subtle unaligned bus faults.

## Compiler, ABI, and Toolchain Implications
- **Linker and Loader Support:** Over-aligned global variables require linker script support to ensure output sections respect alignment requirements.

## Performance, Memory, Timing, and Power
- **SIMD Acceleration:** Proper over-alignment unlocks high-speed vectorized SIMD instructions (`_mm256_load_ps`), boosting throughput for DSP algorithms.

## Verification / Debugging
- **Static Assertions:** Validate alignment requirements at compile time:
  `_Static_assert(alignof(struct cache_line_packet) == 64, "Alignment mismatch");`

## Safety, Security, and Reliability
- **Reliability:** Prevents hardware bus faults caused by passing unaligned buffers into optimized hardware driver peripherals.

## Trade-offs and Alternatives
- **`alignas` vs. Heap Alignment:** `alignas` provides static compile-time over-alignment with zero allocation overhead, whereas heap allocations require specialized aligned allocation APIs (`aligned_alloc`).

## Staff-Level Takeaway
`_Alignas` bridges the gap between high-level C data structures and low-level hardware constraints. Use it deliberately when interfacing with SIMD vector units, DMA controllers, and high-performance hardware peripherals.

## Related Concepts
- [[00_Chapter_Index]]
- [[01_Alignment_requirements]]
- [[02_Alignof]]
- [[10_DMA_alignment]]
- [[11_Cache_line_alignment]]
