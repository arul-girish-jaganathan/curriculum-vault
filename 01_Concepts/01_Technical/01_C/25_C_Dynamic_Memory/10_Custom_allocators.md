# 10: Custom Allocators

## Definition
Custom allocators are user-defined memory management wrappers or alternative allocation algorithms that intercept standard allocation requests (`malloc`, `free`) or implement specialized allocation strategies tailored to specific application performance, debugging, or security requirements.

## Scope and Boundaries
- **Covers:** Allocator wrappers, debugging instrumentation, leak tracking, red-zoning, and pool-backed custom allocators.
- **Does not cover:** Standard OS heap allocators or embedded static policies ([[12_Embedded_allocation_policy]]).

## Why Does It Exist
Standard system allocators are general-purpose and lack domain-specific optimizations or debugging features:
- **Debugging & Sanitization:** Injecting tracking wrappers to log allocation sites, detect buffer overflows, track leaks, and catch double-frees.
- **Performance Tuning:** Replacing general heap allocators with thread-cached or arena-based allocators to eliminate lock contention and fragmentation.
- **Security Hardening:** Implementing canary values (cookies) around allocated blocks to detect memory corruption instantly.

## Mechanism and Language Rules
- **Wrapper Pattern:** Intercepting calls by defining custom functions (e.g., `my_malloc`, `my_free`) that wrap standard allocators with additional logging or metadata tracking.
- **LD_PRELOAD Interception:** On POSIX systems, defining functions named `malloc` and `free` in a shared library allows overriding standard libc allocator functions dynamically at runtime without recompiling source code.

## Examples
```c
#include <stdio.h>
#include <stdlib.h>
#include <stddef.h>

/* Custom allocation wrapper tracking total allocated bytes */
static size_t g_total_allocated_bytes = 0;

void *debug_malloc(size_t size, const char *file, int line) 
{
    /* Allocate extra space to store allocation metadata */
    size_t actual_size = size + sizeof(size_t);
    void *raw = malloc(actual_size);
    if (!raw) {
        return NULL;
    }

    /* Store size prefix */
    size_t *meta = raw;
    *meta = size;

    g_total_allocated_bytes += size;
    printf("[MEM_LOG] Allocating %zu bytes at %s:%d
", size, file, line);

    /* Return pointer offset past metadata header */
    return (void *)(meta + 1);
}

void debug_free(void *ptr) 
{
    if (!ptr) {
        return;
    }

    /* Retrieve metadata header preceding user pointer */
    size_t *meta = (size_t *)ptr - 1;
    size_t size = *meta;

    g_total_allocated_bytes -= size;
    printf("[MEM_LOG] Freeing %zu bytes
", size);

    free(meta);
}

/* Convenience macro wrapper */
#define DBG_MALLOC(sz) debug_malloc(sz, __FILE__, __LINE__)
#define DBG_FREE(ptr)  debug_free(ptr)
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- **Allocator Mismatch:** Passing a pointer allocated by `debug_malloc` directly to standard system `free()` instead of `debug_free()` bypasses metadata offset retrieval, causing severe heap corruption and undefined behavior.

## Edge Cases and Failure Modes
- **Wrapper Overhead:** Adding tracking headers and logging statements to every allocation introduces CPU overhead and memory footprint expansion, making debug wrappers unsuitable for production release builds.

## Embedded Implications
- **Targeted Instrumentation:** Embedded systems use custom allocator wrappers to route heap requests through memory protection units (MPUs) or log peak RAM consumption during unit testing.

## Firmware Review Angle
- **Audit Allocator Consistency:** Ensure that custom allocators and deallocators maintain strict symmetry; never mix wrapper allocators with native system allocators.

## Compiler, ABI, and Toolchain Implications
- **Linker Wrapping (`--wrap`):** GNU ld provides the `--wrap=symbol` linker flag, allowing developers to seamlessly redirect all calls to `malloc` to `__wrap_malloc` automatically.

## Performance, Memory, Timing, and Power
- **Profiling Cost:** Custom tracking wrappers incur logging and metadata storage overhead, trading execution speed for rigorous memory visibility.

## Verification / Debugging
- **Leak Detection:** Custom allocators with tracking tables provide instant reporting of un-freed memory blocks upon program shutdown, serving as lightweight alternatives to Valgrind.

## Safety, Security, and Reliability
- **Hardened Allocators:** Security-focused custom allocators randomize allocation locations, immediately poison freed memory, and use guard pages to mitigate exploitation.

## Trade-offs and Alternatives
- **Custom Wrapper vs. Standard Sanitizers:** Custom wrappers offer application-specific logging and control; ASan / Valgrind offer deeply integrated compiler and toolchain-level protection.

## Staff-Level Takeaway
Custom allocators and wrappers are powerful architectural tools for instrumenting memory usage, injecting debugging checks, or routing allocations to specialized memory pools. Ensure strict allocation/deallocation symmetry to prevent allocator mismatch faults.

## Related Concepts
- [[00_Chapter_Index]]
- [[01_malloc]]
- [[04_free]]
- [[11_Pools_and_arenas]]
- [[12_Embedded_allocation_policy]]
