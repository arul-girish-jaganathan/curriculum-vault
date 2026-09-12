# 07: Allocation Failure

## Definition
Allocation failure occurs when a heap allocation request (`malloc`, `calloc`, `realloc`) cannot be fulfilled by the runtime environment due to memory exhaustion, heap fragmentation, or resource limits, resulting in the allocator returning a `NULL` pointer.

## Scope and Boundaries
- **Covers:** Handling `NULL` return values, OOM (out-of-memory) resilience, fail-safe fallback patterns, and critical system survival strategies.
- **Does not cover:** Embedded static allocation policies ([[12_Embedded_allocation_policy]]) or arena exhaustion ([[11_Pools_and_arenas]]).

## Why Does It Exist
Dynamic memory is inherently finite:
- **Resilience:** Operating systems and embedded devices frequently encounter memory pressure. Robust software must handle allocation failure gracefully rather than crashing catastrophically.
- **Contract Enforcement:** The `NULL` return value is the C language's primary contract indicating that an allocation request could not be honored.

## Mechanism and Language Rules
- **Null Return Check:** Every call to `malloc`, `calloc`, or `realloc` must be checked to verify that the returned pointer is not `NULL`.
- **Flow Control on Failure:** When allocation fails, the program must release any partially acquired resources, log the fault, and return an error code or enter a safe fallback state.
- **No Automatic Exceptions:** Unlike C++ or higher-level languages that throw exceptions (`std::bad_alloc`), C provides no language-level exception handling for memory exhaustion. Everything must be handled via explicit error propagation.

## Examples
```c
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

typedef struct {
    char *buffer_a;
    char *buffer_b;
} dual_buffers_t;

bool init_dual_buffers(dual_buffers_t *ctx, size_t size) 
{
    ctx->buffer_a = NULL;
    ctx->buffer_b = NULL;

    ctx->buffer_a = malloc(size);
    if (!ctx->buffer_a) {
        goto cleanup_failure;
    }

    ctx->buffer_b = malloc(size);
    if (!ctx->buffer_b) {
        goto cleanup_failure;
    }

    return true;

cleanup_failure:
    /* Robust cleanup handling partial allocations */
    free(ctx->buffer_a);
    free(ctx->buffer_b);
    ctx->buffer_a = NULL;
    ctx->buffer_b = NULL;
    return false;
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- **Undefined Behavior (Null Dereference):** Accessing memory through an unchecked pointer returned by `malloc` when OOM occurs results in an immediate segmentation fault or undefined behavior.

## Edge Cases and Failure Modes
- **OOM Killer (Linux):** On Linux systems, `malloc` often succeeds even when memory is exhausted due to overcommit policies. The kernel's OOM killer steps in later, arbitrarily terminating processes when actual memory writes occur.
- **Cascading Failures:** Failing to clean up prior allocations during a failed compound allocation creates memory leaks during error recovery paths.

## Embedded Implications
- **No OOM Safety Net:** Embedded microcontrollers have no virtual memory overcommit or Linux OOM killer. When RAM is exhausted, `malloc` returns `NULL` immediately.
- **Crash vs. Graceful Degradation:** Firmware must decide whether to reboot via watchdog, drop non-critical background telemetry tasks, or enter a safe fault state upon allocation failure.

## Firmware Review Angle
- **Mandatory `NULL` Checks:** Audit every dynamic allocation site to guarantee that `if (!ptr)` error handling exists.
- **Review Recovery Paths:** Inspect error cleanup blocks to ensure all allocated sub-resources are correctly freed without double-frees.

## Compiler, ABI, and Toolchain Implications
- **Link-Time Custom Allocators:** Toolchains allow overriding `malloc` / `free` with custom allocator wrappers (e.g., jemalloc, tcmalloc) that implement specialized OOM hooks or logging.

## Performance, Memory, Timing, and Power
- **Failure Latency:** Searching fragmented free lists during heavy memory pressure can cause allocation functions to take longer before finally returning `NULL`.

## Verification / Debugging
- **Fault Injection:** Simulate low-memory conditions during testing by intercepting `malloc` calls and artificially returning `NULL` to verify application resilience.
- **Static Analysis:** Configure static analyzers to flag unchecked pointer return values from allocation functions.

## Safety, Security, and Reliability
- **Denial of Service (DoS):** Unhandled allocation failures allow malicious inputs to trigger memory exhaustion, crashing servers or embedded controllers.
- **Fail-Safe Design:** Safety-critical systems require deterministic memory allocation at startup so that runtime allocation failure is entirely structurally eliminated.

## Trade-offs and Alternatives
- **Dynamic Allocation with OOM Checks vs. Static Pre-Allocation:** Dynamic allocation requires complex error handling for failures; static pre-allocation guarantees zero runtime allocation failures.

## Staff-Level Takeaway
An unhandled allocation failure is a software bug. In C, memory exhaustion does not throw an exception; it returns `NULL`. Every dynamic allocation site requires an explicit failure recovery path and thorough testing under simulated memory pressure.

## Related Concepts
- [[00_Chapter_Index]]
- [[01_malloc]]
- [[04_free]]
- [[08_Ownership_contracts]]
- [[12_Embedded_allocation_policy]]
