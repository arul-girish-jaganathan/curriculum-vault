# 09: Thread Cancellation Boundaries

## Definition
Thread cancellation boundaries define points during execution where a thread checks whether a cancellation request has been submitted, allowing it to terminate cooperatively and release acquired resources cleanly. Unlike POSIX (`pthread_cancel`), standard ISO C11 threads do not provide asynchronous cancellation primitives; cancellation must be implemented cooperatively via atomic flags, condition variables, or status checks.

## Scope and Boundaries
- **Covers:** Cooperative cancellation idioms, C11 cancellation boundaries, cleanup guarantees, resource reclamation, and timeout interruption.
- **Does not cover:** POSIX asynchronous cancellation (`PTHREAD_CANCEL_ASYNCHRONOUS`), hardware signal interrupts (`sigaction`), or process killing (`kill`).

## Why Does It Exist
Abruptly killing a thread from the outside (asynchronous termination) is dangerous:
- **Corrupted Invariants:** Terminating a thread while it is halfway through updating a linked list or writing to a hardware register leaves the system in an unrecoverable corrupted state.
- **Orphaned Mutexes:** If a thread dies while holding a mutex, that mutex remains locked forever, deadlocking all other threads.
- **ISO C Decision:** C11 deliberately omitted asynchronous cancellation because it cannot be implemented safely and portably across diverse operating systems and microcontrollers.

## Mechanism and Language Rules
- **No `thrd_cancel` in ISO C:** ISO C11 provides no `thrd_cancel()` function. Cooperative cancellation is the only standard-compliant mechanism.
- **Cooperative Cancellation Pattern:**
  1. A cancellation flag (typically `atomic_bool` from `<stdatomic.h>`) is shared between the controller and worker thread.
  2. The controller sets the flag: `atomic_store_explicit(&stop_flag, true, memory_order_release);`
  3. The worker periodically checks the flag at defined **cancellation boundaries** (e.g., loop iterations, after waking from sleeps).
  4. If cancelled, the worker cleanly frees its resources and returns or calls `thrd_exit()`.
- **Waking Blocked Threads:** If a worker is blocked on a condition variable, setting an atomic flag alone will not wake it. The controller must signal or broadcast on the condition variable after setting the flag.

## Examples
```c
#include <threads.h>
#include <stdatomic.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    atomic_bool cancel_requested;
    mtx_t lock;
    cnd_t cond;
    bool has_work;
} worker_channel_t;

static int cooperative_worker(void *arg) 
{
    worker_channel_t *chan = (worker_channel_t *)arg;

    printf("Worker started...\n");
    while (1) {
        mtx_lock(&chan->lock);

        /* Cancellation Boundary 1: Before sleeping */
        while (!chan->has_work && !atomic_load_explicit(&chan->cancel_requested, memory_order_acquire)) {
            cnd_wait(&chan->cond, &chan->lock);
        }

        /* Cancellation Boundary 2: Immediately upon waking */
        if (atomic_load_explicit(&chan->cancel_requested, memory_order_acquire)) {
            printf("Worker detected cancellation. Cleaning up resources...\n");
            mtx_unlock(&chan->lock);
            break; /* Exit loop for graceful cleanup */
        }

        /* Perform work */
        printf("Worker processing task...\n");
        chan->has_work = false;
        mtx_unlock(&chan->lock);

        /* Cancellation Boundary 3: Between pipeline stages */
        if (atomic_load_explicit(&chan->cancel_requested, memory_order_acquire)) {
            break;
        }
    }

    /* Guaranteed Clean Resource Reclamation */
    printf("Worker shutdown complete.\n");
    return thrd_success;
}

int main(void) 
{
    worker_channel_t chan;
    atomic_init(&chan.cancel_requested, false);
    mtx_init(&chan.lock, mtx_plain);
    cnd_init(&chan.cond);
    chan.has_work = false;

    thrd_t worker;
    thrd_create(&worker, cooperative_worker, &chan);

    /* Let worker run briefly */
    struct timespec ts = { .tv_sec = 0, .tv_nsec = 50000000 };
    thrd_sleep(&ts, NULL);

    /* Request Cancellation */
    printf("Main thread requesting worker cancellation...\n");
    atomic_store_explicit(&chan.cancel_requested, true, memory_order_release);

    /* Wake worker if blocked on condition variable */
    mtx_lock(&chan.lock);
    cnd_broadcast(&chan.cond);
    mtx_unlock(&chan.lock);

    /* Synchronize termination */
    thrd_join(worker, NULL);

    mtx_destroy(&chan.lock);
    cnd_destroy(&chan.cond);
    printf("Application finished cleanly.\n");
    return EXIT_SUCCESS;
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- **POSIX Interop Hazard:** Calling POSIX `pthread_cancel()` on a thread created by C11 `thrd_create()` is implementation-defined or undefined depending on the C runtime's mapping of `thrd_t` to `pthread_t`.
- **Dangling Resources:** If a thread terminates via `thrd_exit()` or `return` without unwinding allocated memory, open files, or mutexes, those resources remain orphaned.

## Edge Cases and Failure Modes
- **Unbounded Blocking in I/O:** If a worker thread is blocked on a synchronous blocking OS socket read or UART driver read, it cannot reach a cancellation boundary. In such cases, the controller must close the underlying file descriptor or use non-blocking I/O with timeouts.
- **Forgotten Wakeup:** Setting the cancel flag while the worker is asleep on `cnd_wait` without calling `cnd_broadcast` results in a deadlock where the worker sleeps forever and the joiner blocks forever.

## Embedded Implications
- **Safety Critical Requirement:** In automotive (AUTOSAR) and aerospace software, threads are never asynchronously killed; cooperative cancellation is mandatory to ensure actuators are placed in a fail-safe state before task exit.
- **Watchdog Servicing:** During protracted cancellation unwinding, ensure the watchdog timer is serviced or shutdown happens within the watchdog timeout window.

## Firmware Review Angle
- **No Asynchronous Kill APIs:** Flag any non-portable calls like `pthread_kill`, `TerminateThread`, or `vTaskDelete(other_task)`.
- **Cancellation Latency:** Evaluate the maximum time between two cancellation boundaries. Long computations must interleave periodic checks to guarantee responsive shutdown.
- **Cleanup Guarantee:** Ensure all local buffers, mutex locks, and peripheral states are reverted in the exit path.

## Compiler, ABI, and Toolchain Implications
- **Memory Ordering:** Cancellation flags must use `memory_order_release` when setting and `memory_order_acquire` when loading to ensure all prior updates and shutdown commands are visible.
- **Volatile Is Not Enough:** Do not use plain `volatile bool` for cancellation flags across threads; use C11 `atomic_bool` to prevent memory reordering.

## Performance, Memory, Timing, and Power
- **Overhead of Checking:** Checking an `atomic_bool` via an acquire load takes ~1 nanosecond on modern CPUs. Placing checks in loop headers introduces negligible overhead.
- **Deterministic Latency:** Cooperative cancellation guarantees bounded, deterministic cleanup latency without scheduler thrashing.

## Verification / Debugging
- **Fuzzing Cancellation Points:** Introduce random cancellation delays during stress tests to ensure the thread exits cleanly from every possible boundary without memory leaks.
- **Leak Sanitizer (LSan):** Confirms that dynamic allocations are completely freed when cancellation paths are taken.

## Safety, Security, and Reliability
- **Guaranteed Consistency:** Ensures database files, flash sectors, and hardware registers are never left in partially written, corrupted states.
- **Deadlock Immunity:** Cooperative cancellation prevents orphaned locks, eliminating the primary cause of system-wide lockup during service shutdowns.

## Trade-offs and Alternatives
- **Cooperative vs. Asynchronous Cancellation:**
  - *Cooperative:* 100% safe, portable, deterministic, resource-clean; requires programmer discipline to insert check points.
  - *Asynchronous:* Terminates instantly; causes resource leaks, mutex deadlocks, and corrupted memory invariants. Banned in high-reliability engineering.

## Staff-Level Takeaway
Asynchronous thread termination is an anti-pattern. Reliable systems are built on cooperative cancellation boundaries. Every long-running worker loop must have defined cancellation checkpoints, and every blocking wait must have a corresponding wakeup pathway to guarantee responsive, clean termination.

## Related Concepts
- [[00_Chapter_Index]]
- [[02_thrd_join]]
- [[06_Condition_variables]]
- [[10_C11_thread_portability]]
- [[12_Thread_safe_module_design]]
