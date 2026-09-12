# 02: calloc

## Definition
`calloc` (contiguous allocation) is the standard library function declared in `<stdlib.h>` that allocates memory for an array of `num` elements, each of size `size` bytes, and initializes all bytes in the allocated storage to zero (`0`).

## Scope and Boundaries
- **Covers:** `call_oc()` syntax, parameters (`num`, `size`), automatic zero-initialization, built-in overflow checking of element multiplication, and performance traits.
- **Does not cover:** Uninitialized allocation ([[01_malloc]]), resizing ([[03_realloc]]), or deallocation ([[04_free]]).

## Why Does It Exist
Manual zeroing of memory after `malloc` is redundant and error-prone:
- **Built-in Overflow Protection:** Unlike `malloc(num * size)`, which can silently overflow `size_t` and allocate a truncated buffer, `calloc` explicitly validates `num * size` for multiplication overflow and returns `NULL` if an overflow occurs.
- **Guaranteed Clean State:** Instantly zeroes out buffers, preventing bugs arising from uninitialized data structures, uninitialized pointers, or stale state residue.

## Mechanism and Language Rules
- **Function Signature:** `void *calloc(size_t num, size_t size);`
- **Parameters:**
  - `num`: Number of elements to allocate.
  - `size`: Size in bytes of each individual element.
- **Return Value:** Returns a pointer to the zero-initialized allocated block, or `NULL` if allocation or multiplication overflow fails.
- **Zero-Initialization Guarantee:** Every byte in the allocated memory block is set to all-bits-zero (`0x00`). Note: For integer types, pointers, and floating-point types, all-bits-zero corresponds to numeric zero (`0`, `NULL`, `0.0`), though strictly speaking C permits implementations where pointer/float zero is represented differently (though universal on modern hardware).

## Examples
```c
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

typedef struct {
    int *matrix_data;
    size_t rows;
    size_t cols;
} matrix_t;

matrix_t *create_zeroed_matrix(size_t rows, size_t cols) 
{
    if (rows == 0 || cols == 0) {
        return NULL;
    }

    matrix_t *mat = malloc(sizeof(matrix_t));
    if (!mat) {
        return NULL;
    }

    /* calloc safely checks for multiplication overflow of rows * cols */
    mat->matrix_data = calloc(rows * cols, sizeof(int));
    if (!mat->matrix_data) {
        free(mat);
        return NULL;
    }

    mat->rows = rows;
    mat->cols = cols;
    return mat; /* All elements are guaranteed to be initialized to 0 */
}

void destroy_matrix(matrix_t *mat) 
{
    if (mat) {
        free(mat->matrix_data);
        free(mat);
    }
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- **Pointer Null Representation:** While all-bits-zero represents `NULL` pointer values on virtually all modern architectures (x86, ARM, RISC-V), ISO C permits non-zero bit patterns for null pointers in esoteric hardware architectures.
- **Unchecked NULL Return:** Dereferencing the result of `calloc` without checking for `NULL` triggers undefined behavior.

## Edge Cases and Failure Modes
- **Multiplication Overflow Handled:** If `num * size` exceeds `SIZE_MAX`, `calloc` safely returns `NULL` instead of wrapping around and allocating a truncated buffer.
- **Performance overhead of zeroing:** For massive allocations, `calloc` incurs CPU time and cache pollution to write zeroes across every byte, which may be slower than `malloc` if the buffer is going to be immediately overwritten entirely.

## Embedded Implications
- **Deterministic Zeroing:** In firmware, `calloc` ensures security-sensitive buffers (cryptographic keys, auth tokens) do not contain stray flash or RAM remnants from previous allocations.
- **RAM Footprint:** Zero-init touches every memory page immediately, faulting pages into physical RAM and preventing lazy-allocation optimizations present in hosted OSes.

## Firmware Review Angle
- **Replace Unsafe `malloc` Multiplications:** Audit codebases for `malloc(n * sizeof(T))` and replace them with `calloc(n, sizeof(T))` to eliminate multiplication overflow vulnerabilities.
- **Check Zeroing Necessity:** Verify whether zero-initialization is required; if performance is critical and data is instantly overwritten, `malloc` may be preferred.

## Compiler, ABI, and Toolchain Implications
- **Optimized Zeroing:** C runtimes often implement `calloc` using optimized assembly routines (e.g., vector instructions like AVX/Neon or hardware memset acceleration) to zero memory blocks rapidly.

## Performance, Memory, Timing, and Power
- **Performance Trade-off:** `calloc` is marginally slower than `malloc` due to the required memory-clearing operation, but safer and cleaner.
- **Cache Pollution:** Writing zeroes to a multi-megabyte buffer flushes CPU caches of useful data, increasing cache miss latency immediately following allocation.

## Verification / Debugging
- **Valgrind Memcheck:** Valgrind tracks allocations made by `calloc` and marks them fully defined (no uninitialized read warnings possible on newly allocated blocks).
- **ASan Integration:** ASan guards `calloc` blocks with redzones just like `malloc`.

## Safety, Security, and Reliability
- **Information Leak Prevention:** Zero-initializing buffers before releasing or reusing them prevents accidental disclosure of sensitive residual data across security boundaries.
- **Robustness:** Eliminating manual loops to clear buffers (`memset(ptr, 0, size)`) reduces code complexity and eliminates off-by-one errors.

## Trade-offs and Alternatives
- **`calloc` vs. `malloc` + `memset`:** `calloc` is concise, performs internal overflow checking, and is often optimized by the runtime library. `malloc` + `memset` is manual and vulnerable to multiplication overflow.

## Staff-Level Takeaway
`calloc` should be your default allocator whenever allocating arrays or buffers unless profiling explicitly proves that skipping zero-initialization provides a mandatory performance gain. Its built-in overflow check makes it inherently safer than `malloc(a * b)`.

## Related Concepts
- [[00_Chapter_Index]]
- [[01_malloc]]
- [[03_realloc]]
- [[04_free]]
- [[05_Alignment_guarantees]]
