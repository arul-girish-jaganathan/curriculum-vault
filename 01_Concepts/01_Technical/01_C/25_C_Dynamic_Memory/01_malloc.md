# 01: malloc

## Definition
`malloc` (memory allocation) is the standard library function declared in `<stdlib.h>` that allocates a specified number of bytes from the heap and returns a pointer to the first byte of the allocated memory block. The contents of the allocated memory are indeterminate (uninitialized).

## Scope and Boundaries
- **Covers:** `malloc()` syntax, byte-size calculations, uninitialized memory semantics, alignment requirements, and return value validation.
- **Does not cover:** Zero-initialized allocation ([[02_calloc]]), resizing ([[03_realloc]]), or deallocation ([[04_free]]).

## Why Does It Exist
Static and stack allocations require fixed sizes known at compile time:
- **Runtime Sizing:** Enables data structures (arrays, trees, buffers) whose sizes are determined dynamically at runtime based on user input, files, or network streams.
- **Lifetime Extension:** Heap allocations persist beyond the scope of the function that created them, allowing data to be returned to callers or shared across modules until explicitly freed.

## Mechanism and Language Rules
- **Function Signature:** `void *malloc(size_t size);`
- **Parameters:** `size` specifies the number of bytes to allocate.
- **Return Value:** Returns a generic pointer (`void *`) to the allocated block, or `NULL` if the allocation request fails (e.g., out of memory).
- **Alignment Guarantee:** ISO C guarantees that `malloc` returns a pointer suitably aligned for any object type with fundamental alignment requirements (equivalent to `max_align_t`).
- **Indeterminate State:** The memory returned by `malloc` contains whatever arbitrary bit pattern happened to reside in that heap block; reading from it without prior writing invokes indeterminate behavior / uninitialized data bugs.

## Examples
```c
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

typedef struct {
    uint32_t id;
    float *samples;
    size_t count;
} sensor_buffer_t;

sensor_buffer_t *create_sensor_buffer(size_t count) 
{
    /* Always check for potential overflow in multiplication */
    if (count == 0 || count > SIZE_MAX / sizeof(float)) {
        return NULL;
    }

    sensor_buffer_t *buf = malloc(sizeof(sensor_buffer_t));
    if (!buf) {
        return NULL;
    }

    buf->samples = malloc(count * sizeof(float));
    if (!buf->samples) {
        free(buf); /* Clean up previously allocated resources on failure */
        return NULL;
    }

    buf->id = 101;
    buf->count = count;
    return buf;
}

void destroy_sensor_buffer(sensor_buffer_t *buf) 
{
    if (buf) {
        free(buf->samples);
        free(buf);
    }
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- **Undefined Behavior (Dereferencing NULL):** If `malloc` returns `NULL` on allocation failure and the code dereferences the pointer without checking, undefined behavior (segmentation fault / hard fault) occurs.
- **Undefined Behavior (Reading Uninitialized Data):** Reading values directly from `malloc`'d memory before writing to it yields indeterminate values.

## Edge Cases and Failure Modes
- **Integer Overflow in Size Calculation:** Calculating size via `malloc(num * size)` where `num * size` overflows `size_t` results in allocating a tiny buffer while writing a large amount of data, causing heap corruption.
- **Memory Leaks:** Forgetting to pair every successful `malloc` with a corresponding `free` leads to progressive memory exhaustion.

## Embedded Implications
- **Heap Fragmentation:** Repeatedly calling `malloc` and `free` with varying sizes causes external heap fragmentation, eventually causing allocation failures even when total free memory is theoretically sufficient.
- **Deterministic Latency:** Standard heap allocators (`ptmalloc`, `dlmalloc`) have non-deterministic execution times due to internal searching and coalescing algorithms, making them unsuitable for hard real-time tasks.

## Firmware Review Angle
- **Multiplication Overflow Audit:** Inspect all `malloc(a * b)` calls for potential arithmetic overflow before allocation.
- **Null-Check Enforcement:** Verify that every single `malloc` call has an immediate `if (!ptr)` failure handling path.
- **Partial Allocation Cleanup:** Check complex initialization routines to ensure all allocated sub-blocks are freed if any intermediate allocation fails.

## Compiler, ABI, and Toolchain Implications
- **Allocator Implementation:** `malloc` is typically provided by the C runtime library (`libc`), which manages a system-level heap via kernel calls (`brk`, `sbrk`, `mmap` on POSIX).
- **Optimization Barriers:** `malloc` acts as a memory barrier and allocation source; the compiler knows that a newly allocated pointer does not alias any existing active object.

## Performance, Memory, Timing, and Power
- **Allocation Cost:** System heap allocation involves traversing internal free-lists and locking heap mutexes (in multi-threaded environments), costing hundreds of CPU cycles.
- **Overhead:** Allocators typically prepend metadata headers (e.g., block size, flags) to each chunk, consuming extra RAM per allocation.

## Verification / Debugging
- **AddressSanitizer (ASan):** Use `-fsanitize=address` to detect heap buffer overflows, use-after-free, and memory leaks at runtime.
- **Valgrind Memcheck:** Run binaries under Valgrind to track uninitialized memory reads (`--track-origins=yes`) and leaked allocations.

## Safety, Security, and Reliability
- **Security Vulnerabilities:** Unchecked `malloc` return values combined with subsequent writes lead to null-pointer dereference denial-of-service or arbitrary write primitives if offset calculations follow.
- **MISRA C Compliance:** Safety standards (MISRA C:2012 Rule 21.3) heavily restrict or ban dynamic heap allocation due to non-determinism and memory leak risks.

## Trade-offs and Alternatives
- **`malloc` vs. Stack Allocation:** Heap allocation allows large or dynamic sizes but incurs allocation overhead and leakage risks; stack allocation is fast and self-cleaning but limited by small stack sizes and compile-time bounds.
- **Alternatives:** Static global buffers or fixed-size memory pools.

## Staff-Level Takeaway
`malloc` is a low-level primitive, not a high-level memory manager. Treat every `malloc` call as an explicit contract requiring a corresponding `free` and robust failure handling. In safety-critical embedded systems, eliminate `malloc` entirely in favor of static memory allocation and object pools.

## Related Concepts
- [[00_Chapter_Index]]
- [[02_calloc]]
- [[03_realloc]]
- [[04_free]]
- [[05_Alignment_guarantees]]
