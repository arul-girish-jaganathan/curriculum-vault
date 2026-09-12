# 03: realloc

## Definition
`realloc` (re-allocation) is the standard library function declared in `<stdlib.h>` that changes the size of a previously allocated memory block pointed to by `ptr` to a new size specified in bytes. It can expand or shrink the existing memory block, potentially relocating it to a new memory address.

## Scope and Boundaries
- **Covers:** `realloc()` syntax, in-place growth, relocation semantics, memory preservation up to the minimum of old and new sizes, and failure safety patterns.
- **Does not cover:** Initial allocation ([[01_malloc]], [[02_calloc]]) or deallocation ([[04_free]]).

## Why Does It Exist
Data structures grow and shrink dynamically (e.g., dynamic arrays, growing buffers, streaming parsers):
- **Dynamic Resizing:** Avoids fixed maximum buffer bounds or manual allocation, copy, and free boilerplate when expanding data arrays.
- **Optimization Opportunities:** If adjacent heap space is available, `realloc` expands the block in-place with zero data copying overhead.

## Mechanism and Language Rules
- **Function Signature:** `void *realloc(void *ptr, size_t new_size);`
- **Parameters:**
  - `ptr`: Pointer to the previously allocated memory block (or `NULL`).
  - `new_size`: Desired new size in bytes.
- **Special Cases:**
  - If `ptr` is `NULL`, `realloc` behaves exactly like `malloc(new_size)`.
  - If `new_size` is `0`, `realloc` behaves like `free(ptr)` and returns `NULL` (or a unique pointer that can be safely passed to `free`).
- **Return Value:** Returns a pointer to the newly sized memory block (which may be the same as `ptr` or a new address), or `NULL` if allocation fails.
- **Failure Safety Rule:** If `realloc` fails, the original memory block `ptr` is **left untouched and valid**; it is not freed. However, failing to capture the return value into a temporary variable before assigning it back to the original pointer results in a memory leak if `realloc` returns `NULL`.

## Examples
```c
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int *data;
    size_t size;
    size_t capacity;
} dynamic_array_t;

int array_append(dynamic_array_t *arr, int value) 
{
    if (arr->size >= arr->capacity) {
        size_t new_capacity = arr->capacity == 0 ? 4 : arr->capacity * 2;
        
        /* CORRECT PATTERN: Use a temporary pointer to prevent memory leaks on failure */
        int *temp = realloc(arr->data, new_capacity * sizeof(int));
        if (!temp) {
            return -1; /* arr->data is still valid and unchanged */
        }
        
        arr->data = temp;
        arr->capacity = new_capacity;
    }

    arr->data[arr->size++] = value;
    return 0;
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- **Undefined Behavior (Classic Leak Bug):** `ptr = realloc(ptr, new_size);` — if `realloc` fails and returns `NULL`, `ptr` is overwritten with `NULL`, permanently losing the reference to the original allocated memory block and creating a severe memory leak.
- **Undefined Behavior (Use-After-Free on Old Pointer):** Accessing the old memory address `ptr` after a successful relocation via `realloc` is use-after-free undefined behavior.

## Edge Cases and Failure Modes
- **Shrinking Blocks:** When `new_size` is smaller than the original size, data beyond `new_size` is truncated, and the memory block may be adjusted or kept in place.
- **Zero-Size Request:** Passing `new_size == 0` is implementation-defined; standard ISO C permits returning `NULL` or a zero-sized block. Avoid `realloc(ptr, 0)` due to portability hazards.

## Embedded Implications
- **Heap Fragmentation from Growth:** Frequent incremental `realloc` calls cause severe heap fragmentation as blocks are repeatedly copied and abandoned across the heap.
- **Deterministic Avoidance:** Real-time embedded systems strictly prohibit `realloc` due to unbounded execution time (copying large buffers) and heap exhaustion risks.

## Firmware Review Angle
- **Audit `realloc` Assignment Patterns:** Scan codebase for `ptr = realloc(ptr, ...)` and flag them as memory leak hazards. Require temporary pointer assignment.
- **Check Minimum Capacity Growth:** Ensure dynamic array resizing uses exponential growth (e.g., `capacity * 2`) rather than linear growth (`capacity + 1`), which turns insertion into $O(N^2)$ complexity.

## Compiler, ABI, and Toolchain Implications
- **Internal Optimization:** Modern memory allocators check if the trailing heap chunk is free and can absorb the expansion in-place without copying data bytes.

## Performance, Memory, Timing, and Power
- **Copy Cost:** When relocation is forced, `realloc` must allocate a new block, `memcpy` all existing bytes from old to new, and `free` the old block, incurring $O(N)$ time complexity.
- **Memory Overhead:** Temporary peak memory usage during relocation can reach `old_size + new_size`.

## Verification / Debugging
- **AddressSanitizer:** ASan poisons the old block and validates that no out-of-bounds accesses occur during or after resizing.
- **Valgrind:** Traces reallocations and flags invalid pointer reallocs or use of uninitialized extended space.

## Safety, Security, and Reliability
- **Integer Overflow in Size:** Multiplying count by size before passing to `realloc` is vulnerable to arithmetic overflow. Always validate bounds.
- **Robustness:** Proper temporary pointer handling ensures system stability even under low-memory conditions.

## Trade-offs and Alternatives
- **`realloc` vs. Manual Allocate-Copy-Free:** `realloc` is optimized by the runtime allocator (in-place expansion when possible); manual copy is tedious and slower.
- **Alternatives:** Fixed-capacity ring buffers or pre-allocated arenas.

## Staff-Level Takeaway
`realloc` is extremely convenient but dangerous if misused. Never assign the result of `realloc` directly back to the source pointer without an intermediate variable check. In high-performance or embedded architectures, prefer pre-allocated capacity growth strategies over frequent reallocations.

## Related Concepts
- [[00_Chapter_Index]]
- [[01_malloc]]
- [[02_calloc]]
- [[04_free]]
- [[05_Alignment_guarantees]]
