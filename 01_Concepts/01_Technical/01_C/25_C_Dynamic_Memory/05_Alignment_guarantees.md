# 05: Alignment Requirements and Guarantees

## Definition
Memory alignment refers to the requirement that an object of a given type must be stored at a memory address evenly divisible by a specific power of two (its alignment requirement). Standard dynamic allocators (`malloc`, `calloc`, `realloc`) provide strict alignment guarantees to ensure returned pointers can accommodate any standard data type without hardware faults.

## Scope and Boundaries
- **Covers:** Fundamental alignment, `max_align_t`, standard allocator alignment guarantees, and unaligned access hardware faults.
- **Does not cover:** Custom alignment functions (`aligned_alloc`), struct padding bytes ([[../27_C_Alignment_Object_Representation/06_Padding_bytes]]), or CPU cache line alignment.

## Why Does It Exist
Hardware architectures enforce strict rules on memory access:
- **Hardware Faults:** Many CPU architectures (e.g., ARM Cortex-M0/M3 without unaligned support, older RISC architectures) trigger hard faults or bus errors when attempting to load/store multi-byte types (like `uint32_t` or `double`) from unaligned addresses.
- **Performance Penalty:** Even on architectures that support unaligned access in hardware (e.g., x86_64), unaligned memory accesses cross cache line boundaries, requiring multiple bus cycles and degrading performance.

## Mechanism and Language Rules
- **Fundamental Alignment:** ISO C guarantees that `malloc`, `calloc`, and `realloc` return memory pointers aligned to at least `alignof(max_align_t)`.
- **`max_align_t`:** A standard type defined in `<stddef.h>` whose alignment requirement is at least as strict as every scalar type supported by the implementation (typically 8 or 16 bytes on 64-bit platforms).
- **Custom Alignment (`aligned_alloc`):** Introduced in C11, `void *aligned_alloc(size_t alignment, size_t size);` permits allocating memory with user-specified custom alignments (e.g., 32 or 64 bytes for SIMD vector registers like AVX-512).

## Examples
```c
#include <stdio.h>
#include <stdlib.h>
#include <stddef.h>
#include <stdalign.h>

typedef struct {
    uint64_t timestamp;
    double sensor_reading;
} __attribute__((aligned(32))) aligned_sensor_packet_t;

void *safe_aligned_allocation(size_t count) 
{
    size_t alignment = alignof(aligned_sensor_packet_t);
    size_t size = count * sizeof(aligned_sensor_packet_t);

    /* C11 aligned_alloc requires size to be a multiple of alignment */
    if (size % alignment != 0) {
        size = ((size + alignment - 1) / alignment) * alignment;
    }

    return aligned_alloc(alignment, size);
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- **Undefined Behavior (`aligned_alloc` constraints):** ISO C mandates that for `aligned_alloc(alignment, size)`, `size` **must** be a multiple of `alignment`. Violating this constraint results in undefined behavior or allocation failure.
- **Unaligned Casts:** Casting an unaligned `char *` pointer to a `uint32_t *` and dereferencing it triggers undefined behavior and potential CPU alignment faults.

## Edge Cases and Failure Modes
- **Freeing `aligned_alloc` Memory:** Standard `free()` is fully compatible with memory allocated via `aligned_alloc` across all modern standard C libraries.
- **Alignment Mismatch:** Assuming `malloc` guarantees 64-byte alignment for AVX-512 buffers leads to illegal instruction or bus faults; explicit `aligned_alloc` is mandatory.

## Embedded Implications
- **DMA Buffer Alignment:** Direct Memory Access (DMA) controllers often require transfer source and destination addresses to be aligned to cache line boundaries (e.g., 32 or 64 bytes). Standard `malloc` alignment may be insufficient; `aligned_alloc` is required.
- **Cortex-M Faults:** Unaligned pointer casts in interrupt handlers on constrained MCUs trigger HardFault exceptions immediately.

## Firmware Review Angle
- **Verify Cast Alignment:** Inspect pointer casting operations where raw byte buffers (e.g., UART receive buffers) are cast directly to complex structs.
- **Check `aligned_alloc` Usage:** Ensure that any call to `aligned_alloc` strictly passes a size that is a multiple of the requested alignment.

## Compiler, ABI, and Toolchain Implications
- **ABI Compliance:** Standard library allocators ensure internal bookkeeping headers do not violate the required alignment boundary of the returned payload pointer.

## Performance, Memory, Timing, and Power
- **SIMD Efficiency:** Properly aligned memory enables vector processing instructions to load full cache lines in single clock cycles, maximizing throughput.

## Verification / Debugging
- **UBSan (Undefined Behavior Sanitizer):** `-fsanitize=alignment` detects unaligned pointer dereferences at runtime.
- **Hardware Debuggers:** Monitor CPU Fault Status Registers (CFSR / HFSR) on ARM to diagnose precise instruction addresses causing alignment faults.

## Safety, Security, and Reliability
- **Crash Prevention:** Adhering strictly to hardware alignment requirements prevents unexpected exceptions and system resets in mission-critical firmware.

## Trade-offs and Alternatives
- **Standard `malloc` vs. `aligned_alloc`:** `malloc` provides fundamental alignment suitable for standard scalars; `aligned_alloc` provides custom power-of-two alignments for hardware peripherals and SIMD.

## Staff-Level Takeaway
Never assume raw heap memory is aligned to anything beyond fundamental scalars. When interfacing with hardware DMA engines, cryptographic accelerators, or SIMD vector registers, always utilize `aligned_alloc` with explicit alignment constraints to prevent hardware bus faults.

## Related Concepts
- [[00_Chapter_Index]]
- [[01_malloc]]
- [[../27_C_Alignment_Object_Representation/01_Alignment_requirements]]
- [[../27_C_Alignment_Object_Representation/10_DMA_alignment]]
