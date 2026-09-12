# 01: thrd_create

## Definition
`thrd_create` is the C11 standard library function declared in `<threads.h>` that spawns a new concurrent thread of execution. It initializes an execution context executing the specified entry-point function `thrd_start_t` with a single generic argument (`void *`) and stores the thread identifier in an object of type `thrd_t`.

## Scope and Boundaries
- **Covers:** `thrd_create` syntax, parameter marshalling, thread function prototype (`int (*)(void *)`), return codes (`thrd_success`, `thrd_nomem`, `thrd_error`), and initial thread execution attributes.
- **Does not cover:** Thread joining ([[02_thrd_join]]), thread detaching ([[03_thrd_detach]]), thread synchronization primitives ([[05_Mutexes]], [[06_Condition_variables]]), or C11 atomics.

## Why Does It Exist
Prior to C11, C lacked a language-level concurrency specification. Multithreading relied on platform-specific APIs (`pthread_create` on POSIX, `CreateThread` on Win32):
- **Universal Standard:** Provides an ISO-compliant, vendor-neutral interface for creating concurrent execution units.
- **Runtime Abstract Mapping:** Maps cleanly onto underlying OS kernels or RTOS schedulers while isolating application logic from OS-specific type signatures.
- **Memory Model Alignment:** Works in tandem with the C11 memory model (`<stdatomic.h>`) to formalize happens-before relationships during thread spawning.

## Mechanism and Language Rules
- **Function Signature:** `int thrd_create(thrd_t *thr, thrd_start_t func, void *arg);`
- **Entry-Point Signature:** `typedef int (*thrd_start_t)(void *);` — unlike pthreads which returns `void *`, C11 thread routines must return `int`.
- **Return Values:** Returns `thrd_success` on success, `thrd_nomem` if insufficient system memory exists to allocate stack/context, or `thrd_error` if the request could not be honored.
- **Synchronization Guarantee:** The completion of `thrd_create` synchronizes-with the beginning of the execution of the new thread. Any memory stores preceding `thrd_create` in the caller thread are guaranteed visible to the new thread upon entry.
- **Thread Lifetime:** The created thread executes until `func` returns, `thrd_exit` is called, or the entire process terminates via `exit`, `quick_exit`, or returning from `main`.

## Examples
```c
#include <threads.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

typedef struct {
    int worker_id;
    uint32_t payload_size;
} worker_ctx_t;

/* Correct entry function signature: returns int, takes void* */
static int worker_routine(void *arg) 
{
    worker_ctx_t *ctx = (worker_ctx_t *)arg;
    if (!ctx) {
        return thrd_error;
    }
    printf("Worker %d processing payload: %u\n", ctx->worker_id, ctx->payload_size);
    return thrd_success;
}

int main(void) 
{
    thrd_t thread_handle;
    worker_ctx_t ctx = { .worker_id = 1, .payload_size = 4096 };

    /* Thread creation */
    int res = thrd_create(&thread_handle, worker_routine, &ctx);
    if (res != thrd_success) {
        fprintf(stderr, "Failed to create thread: %d\n", res);
        return EXIT_FAILURE;
    }

    /* Wait for completion to prevent use-after-free of ctx */
    int thread_result = 0;
    thrd_join(thread_handle, &thread_result);
    return EXIT_SUCCESS;
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- **Undefined Behavior:** Passing a null pointer for `thr` or `func` is undefined behavior.
- **Undefined Behavior (Dangling Context):** Passing the address of an automatic (stack) variable whose enclosing scope exits before the child thread reads it results in use-after-free undefined behavior.
- **Implementation-Defined:** Stack size, scheduling policy, thread priority, and system limits on the maximum concurrent thread count are implementation-defined.

## Edge Cases and Failure Modes
- **Stack Overflow on Creation:** Spawning threads with large local stack allocations on microcontrollers or constrained environments triggers silent stack corruption if guard pages are absent.
- **Resource Exhaustion:** Rapidly creating threads in a loop without joining or detaching leads to exhaustion of OS thread handles (`thrd_nomem` / `thrd_error`) and kernel memory leaks.
- **Context Racing:** Passing a mutable struct pointer to multiple threads without locking or passing the same loop variable address `&i` during loop thread generation.

## Embedded Implications
- **RTOS Memory Footprints:** Under RTOSes (e.g., Zephyr, FreeRTOS ports of `<threads.h>`), thread creation typically requires allocating a Task Control Block (TCB) and pre-sized stack buffer from a heap pool.
- **Deterministic Latency:** In hard real-time systems, `thrd_create` is typically forbidden in time-critical cyclic loops due to non-deterministic dynamic allocation latency. Threads must be statically allocated during system boot.

## Firmware Review Angle
- **Verify Argument Lifetimes:** Ensure that `arg` points to statically allocated memory, heap memory whose ownership transfer is verified, or stack memory guarded by a strict `thrd_join`.
- **Check Return Codes:** Ensure the caller verifies `res == thrd_success` and does not assume thread execution began.
- **Stack Sizing:** Validate that the system default thread stack size is sufficient for the target entry function call chain and ISR preemption stack frame.

## Compiler, ABI, and Toolchain Implications
- **Calling Convention:** The entry point follows platform standard ABI calling conventions for standard function pointers.
- **Linker Flags:** Under GCC/Clang on POSIX platforms, linking usually requires `-pthread` even when using `<threads.h>` to bind standard thread runtime primitives.

## Performance, Memory, Timing, and Power
- **Creation Overhead:** Thread creation involves kernel mode transitions, context structure allocation, and virtual memory page mapping, incurring significant CPU overhead compared to thread pools.
- **Power Impact:** Spawning threads across multiple physical cores prevents SoC deep low-power sleep states (`C-states`).

## Verification / Debugging
- **Sanitizers:** ThreadSanitizer (`-fsanitize=thread`) instruments `thrd_create` to register parent-child synchronization edges.
- **GDB Commands:** Use `info threads` and `thread <id>` to inspect newly spawned threads.

## Safety, Security, and Reliability
- **MISRA C:2012:** Thread creation must strictly comply with deterministic concurrency guidelines. Unbounded dynamic thread spawning is restricted in safety-critical code (IEC 61508 / ISO 26262).
- **Type Safety:** `thrd_start_t` requires casting through `void *`. Verify payload schema integrity to avoid type confusion vulnerabilities.

## Trade-offs and Alternatives
- **Dynamic Creation vs. Static Thread Pool:** Spawning on-demand causes allocation latency; thread pools with work queues provide deterministic execution and bounded memory usage.
- **Cooperative Coroutines / Protothreads:** For resource-constrained MCUs, state-machine event loops or cooperative coroutines require far less memory than preemptive `thrd_t`.

## Staff-Level Takeaway
`thrd_create` establishes an ownership and synchronization boundary. Treat thread creation as an expensive architectural allocation, not an inline task primitive. Every spawned thread must have a strictly proven lifecycle contract: clear ownership of input parameters, bounded stack consumption, and a guaranteed reclamation pathway via join or detach.

## Related Concepts
- [[00_Chapter_Index]]
- [[02_thrd_join]]
- [[03_thrd_detach]]
- [[10_C11_thread_portability]]
- [[12_Thread_safe_module_design]]
