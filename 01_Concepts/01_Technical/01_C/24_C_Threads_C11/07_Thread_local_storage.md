# 07: Thread Local Storage

## Definition
Thread-Local Storage (TLS) in C11 provides distinct per-thread instances of variables. Declared via the `_Thread_local` keyword (or the convenience macro `thread_local` defined in `<threads.h>`), a thread-local variable possesses thread storage duration: its lifetime encompasses the entire execution of the thread, and its value is completely isolated from other threads.

## Scope and Boundaries
- **Covers:** `_Thread_local`, `thread_local`, variable lifetimes, initialization semantics, storage duration, and link-time / runtime costs.
- **Does not cover:** Static/global variables, mutex synchronization, or compiler-specific keywords like `__thread` or `__declspec(thread)`.

## Why Does It Exist
Global and static variables create concurrency hazards because their storage is shared across all threads:
- **Lock-Free Thread Isolation:** Eliminates data races and locking overhead by giving every thread its own private copy of state.
- **Thread-Safe Legacy APIs:** Used to make inherently non-reentrant standard C library functions thread-safe (e.g., `errno`, `strtok`).
- **High-Performance Contexts:** Allows threads to maintain local caches, random number generators, or statistics accumulators without mutex contention.

## Mechanism and Language Rules
- **Syntax:** `thread_local int my_counter = 0;` or `_Thread_local static uint32_t worker_state;`
- **Permitted Declarations:** Can be applied to:
  - Global variables (file scope).
  - File-scope static variables.
  - Block-scope static variables (`static thread_local int counter;`).
  - Cannot be applied to automatic (local stack) variables or function arguments.
- **Initialization:**
  - Initialized to zero if not explicitly initialized.
  - Explicit initializers must be compile-time constant expressions.
- **Lifetime:** Allocated when the thread begins execution; destroyed and unmapped when the thread terminates.
- **Address Operator:** The address of a thread-local variable can be taken (`&my_counter`). It is a valid pointer that can be passed to other threads, but accessing it after the owner thread has terminated is undefined behavior.

## Examples
```c
#include <threads.h>
#include <stdio.h>
#include <stdlib.h>

/* Each thread has its own isolated error state and seed */
static thread_local int tl_error_code = 0;
static thread_local unsigned int tl_prng_state = 123456789;

static unsigned int thread_prng(void) 
{
    /* Linear congruential generator on thread-private state */
    tl_prng_state = tl_prng_state * 1103515245A + 12345;
    return (tl_prng_state / 65536) % 32768;
}

static int worker_task(void *arg) 
{
    int thread_id = (int)(intptr_t)arg;
    tl_prng_state ^= (unsigned int)thread_id; /* Seed uniquely */

    for (int i = 0; i < 5; ++i) {
        printf("Thread %d generated: %u\n", thread_id, thread_prng());
    }

    if (thread_id == 2) {
        tl_error_code = -42;
    }
    printf("Thread %d exit with local error code: %d\n", thread_id, tl_error_code);
    return 0;
}

int main(void) 
{
    thrd_t t1, t2;
    thrd_create(&t1, worker_task, (void *)(intptr_t)1);
    thrd_create(&t2, worker_task, (void *)(intptr_t)2);

    thrd_join(t1, NULL);
    thrd_join(t2, NULL);

    /* Main thread's own tl_error_code remains untouched */
    printf("Main thread local error code: %d\n", tl_error_code);
    return EXIT_SUCCESS;
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- **Undefined Behavior (Dangling TLS Pointer):** Taking the address of a thread-local variable, passing it to another thread, and accessing it after the owning thread terminates is a use-after-free undefined behavior.
- **Implementation-Defined:** Maximum size of thread-local storage blocks and the dynamic linking TLS models supported (`General Dynamic`, `Local Dynamic`, `Initial Exec`, `Local Exec`).

## Edge Cases and Failure Modes
- **Hidden Memory Multiplication:** If a module defines a 2 MB thread-local buffer and the application spawns 100 threads, total RAM consumed by that buffer is 200 MB.
- **Dynamic Module Loading (`dlopen`):** Using thread-local variables in dynamically loaded shared objects can exhaust the OS thread-local allocation pools or induce significant latency on first access.
- **Initialization Constraints:** Non-constant dynamic initializers are forbidden in ISO C11 (unlike C++).

## Embedded Implications
- **Severe Memory Footprint:** On microcontrollers with 64 KB RAM, thread-local variables can blow through SRAM rapidly because the linker reserves the entire TLS segment for every task stack/TCB.
- **Linker Script Requirements:** Freestanding embedded toolchains require explicit `.tbss` and `.tdata` sections in the linker script (`linker.ld`), along with RTOS runtime support for thread-pointer registers (e.g., `TPIDRURW` on ARM Cortex-A, or software thread pointer).

## Firmware Review Angle
- **Audit TLS Allocations:** Ban large arrays or structs marked `thread_local` in embedded targets; restrict TLS to scalar IDs, handles, or state flags.
- **Inspect Pointers to TLS:** Verify that pointers to thread-local variables never escape into global structures or outlive the owning thread.
- **Ensure Proper Headers:** Include `<threads.h>` to use `thread_local` or use the standard keyword `_Thread_local` directly.

## Compiler, ABI, and Toolchain Implications
- **Thread Pointer Register:** Modern architectures allocate a dedicated register to point to the current thread's TLS block (e.g., `FS` on x86_64, `TP` on RISC-V, `R9`/`R13` on ARM).
- **Access Costs:** Accessing a static TLS variable in an executable uses the fast `Local Exec` model (a single instruction offset from thread register). In shared libraries, it may require a `__tls_get_addr` runtime function call.

## Performance, Memory, Timing, and Power
- **Performance:** Reads and writes are as fast as normal static variables (in Local Exec model) with zero lock contention.
- **Zero Inter-Core Cache Invalidation:** Eliminates false sharing and cache ping-pong between CPU cores because each core accesses its own independent cache lines.

## Verification / Debugging
- **GDB Inspection:** GDB inspects thread-local variables correctly using `print variable_name`, automatically reading the version associated with the currently selected thread context.
- **Static Analysis:** Tools flag excessive TLS usage and dangling pointer escapes.

## Safety, Security, and Reliability
- **Safety Advantages:** TLS eliminates race conditions by structural architectural design rather than runtime locks, drastically reducing deadlock risks.
- **Memory Safety:** Ensure thread-local memory initialization is zeroed before use to prevent leakage of secrets across recycled thread contexts.

## Trade-offs and Alternatives
- **TLS vs. Explicit Context Struct:**
  - *TLS:* Implicit, clean signatures; hides state, making functions non-pure and complicating unit test isolation.
  - *Context Pointer (`void *ctx`):* Explicit, completely reentrant, pure dependency injection; requires passing pointers through every function call.

## Staff-Level Takeaway
Thread-local storage provides lock-free concurrency at the cost of memory multiplication and architectural opacity. Use TLS sparingly for cross-cutting runtime infrastructure (allocators, trace IDs, thread PRNGs), but prefer explicit parameter-passed context structures for domain logic to keep dependencies visible and testable.

## Related Concepts
- [[00_Chapter_Index]]
- [[01_thrd_create]]
- [[05_Mutexes]]
- [[11_Freestanding_limitations]]
- [[12_Thread_safe_module_design]]
