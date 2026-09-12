# 06: Zero-Size Allocation Cases

## Definition
Zero-size allocation refers to calling heap allocation functions (`malloc(0)`, `calloc(0, size)`, `calloc(num, 0)`, `realloc(ptr, 0)`) requesting zero bytes of payload memory. ISO C treats this as an edge case with implementation-defined return behavior.

## Scope and Boundaries
- **Covers:** Zero-byte allocation semantics, implementation-defined return values (`NULL` vs. unique valid pointers), portable workarounds, and safety risks.
- **Does not cover:** Normal dynamic allocations ([[01_malloc]], [[02_calloc]]) or deallocations ([[04_free]]).

## Why Does It Exist
Dynamic size calculations (e.g., reading array lengths from files or user inputs) can occasionally evaluate to zero due to empty datasets or boundary conditions. Rather than crashing or requiring mandatory branch checks for zero before every allocation, ISO C standardizes rules for zero-size requests.

## Mechanism and Language Rules
- **ISO C Standard Behavior:** For `malloc(0)`, `calloc(0, size)`, and `realloc(ptr, 0)`, the standard specifies that the implementation may either return a null pointer (`NULL`) or a unique pointer value that can be successfully passed to `free()`.
- **Non-Standard Portability Trap:** Because different C library implementations (e.g., glibc vs. musl vs. Windows MSVCRT vs. embedded newlib) handle zero-size allocations differently (some return `NULL`, others return a valid 1-byte heap block), relying on specific return values is non-portable.
- **Dereferencing Hazard:** Even if a zero-size allocation returns a unique valid pointer, **dereferencing** that pointer is strictly undefined behavior because no object was allocated.

## Examples
```c
#include <stdio.h>
#include <stdlib.h>

void *safe_allocate(size_t count, size_t element_size) 
{
    /* DEFENSIVE PRACTICE: Explicitly guard against zero-size requests */
    if (count == 0 || element_size == 0) {
        return NULL; /* Or handle as a specific domain error */
    }

    return malloc(count * element_size);
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- **Implementation-Defined Return:** Whether `malloc(0)` returns `NULL` or a unique non-null pointer is implementation-defined.
- **Undefined Behavior (Dereferencing):** Writing to or reading from a pointer returned by a zero-size allocation is undefined behavior (buffer overflow / out-of-bounds access).

## Edge Cases and Failure Modes
- **Freeing Zero-Size Pointers:** If `malloc(0)` returns a valid non-null pointer, passing it to `free()` is legal and required to prevent memory leaks (in implementations that allocate metadata tracking blocks for zero-size requests).
- **Conditional Check Ambiguity:** `ptr = malloc(0); if (!ptr)` fails portably on systems where `malloc(0)` returns a valid pointer, leading to logic errors in null-checks.

## Embedded Implications
- **Unpredictable Heap Usage:** Zero-size allocations can allocate internal allocator metadata nodes even for zero payload bytes, causing fragmentation and subtle memory overhead in constrained embedded systems.

## Firmware Review Angle
- **Guard Against Zero Allocation:** Enforce explicit checks `if (size == 0) return NULL;` before calling heap allocation functions to ensure deterministic behavior across all toolchains.
- **Flag Zero-Size API Inputs:** Audit APIs that pass dynamic sizes to ensure zero is handled gracefully without hitting allocators.

## Compiler, ABI, and Toolchain Implications
- **Toolchain Divergence:** GCC on Linux (glibc) typically returns a valid minimal chunk for `malloc(0)`, whereas other embedded toolchains might return `NULL`. Code must never assume either behavior.

## Performance, Memory, Timing, and Power
- **No Performance Benefit:** Calling allocation functions with zero size adds branch overhead and allocator logic execution time with zero functional utility.

## Verification / Debugging
- **AddressSanitizer:** ASan tracks zero-size allocations and immediately flags any read/write dereference through them as an out-of-bounds heap-buffer-overflow.

## Safety, Security, and Reliability
- **Vulnerability Vector:** Zero-size allocations have historically been sources of integer wrap-arounds and heap buffer overflow vulnerabilities when downstream code calculates loop bounds using the requested size rather than the actual allocated memory.

## Trade-offs and Alternatives
- **Explicit Guarding vs. Allocator Reliance:** Always guard against zero explicitly rather than relying on allocator-specific zero-size behaviors.

## Staff-Level Takeaway
Never invoke heap allocators with a size of zero. It introduces toolchain-dependent behavior, cross-platform portability bugs, and severe security vulnerability vectors. Explicitly check for zero-size inputs and handle them as distinct edge cases.

## Related Concepts
- [[00_Chapter_Index]]
- [[01_malloc]]
- [[02_calloc]]
- [[04_free]]
- [[07_Allocation_failure]]
