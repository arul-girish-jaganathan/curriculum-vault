# 02: thrd_join

## Definition
`thrd_join` is the C11 thread management function that suspends the execution of the calling thread until the target thread terminates. If the target thread has already terminated, `thrd_join` returns immediately. It reclaims system resources associated with the finished thread and optionally captures its integer exit code.

## Scope and Boundaries
- **Covers:** Synchronous rendezvous, thread resource deallocation, return code harvesting, and thread barrier synchronization.
- **Does not cover:** Asynchronous detached execution ([[03_thrd_detach]]), thread creation ([[01_thrd_create]]), or conditional signaling ([[06_Condition_variables]]).

## Why Does It Exist
Threads occupy OS resources beyond their execution runtime:
- **Resource Reclamation:** Without joining, terminated threads remain in a "zombie" state, preserving their stack, TCB, and kernel handle allocations until the entire process exits.
- **Synchronization Rendezvous:** Guarantees that asynchronous parallel tasks have completed their work before the consumer thread reads the produced output.
- **Memory Visibility Barrier:** Creates a formalized "happens-before" edge under the C11 memory model, ensuring all writes made by the terminating thread become visible to the joining thread.

## Mechanism and Language Rules
- **Function Signature:** `int thrd_join(thrd_t thr, int *res);`
- **Parameters:**
  - `thr`: The target thread handle to await.
  - `res`: Pointer to an `int` variable where the target thread's return code or `thrd_exit` status will be stored. May be `NULL` if the caller ignores the return value.
- **Return Values:** Returns `thrd_success` upon successful join, or `thrd_error` if an error occurs (such as invalid handle or deadlock condition).
- **Single-Join Rule:** Only one thread can join a target thread. Attempting to call `thrd_join` multiple times on the same `thrd_t` handle triggers undefined behavior.
- **Mutual Exclusivity with Detach:** A thread cannot be joined if it has already been detached via `thrd_detach`.

## Examples
```c
#include <threads.h>
#include <stdio.h>
#include <stdlib.h>

#define ARRAY_SIZE 100000

typedef struct {
    const int *data;
    size_t start;
    size_t end;
    int partial_sum;
} sum_task_t;

static int sum_worker(void *arg) 
{
    sum_task_t *task = (sum_task_t *)arg;
    int acc = 0;
    for (size_t i = task->start; i < task->end; ++i) {
        acc += task->data[i];
    }
    task->partial_sum = acc;
    return thrd_success;
}

int main(void) 
{
    int numbers[ARRAY_SIZE];
    for (int i = 0; i < ARRAY_SIZE; ++i) numbers[i] = 1;

    thrd_t worker;
    sum_task_t task1 = { .data = numbers, .start = 0, .end = ARRAY_SIZE / 2, .partial_sum = 0 };

    if (thrd_create(&worker, sum_worker, &task1) != thrd_success) {
        return EXIT_FAILURE;
    }

    /* Compute second half in main thread */
    int main_sum = 0;
    for (size_t i = ARRAY_SIZE / 2; i < ARRAY_SIZE; ++i) {
        main_sum += numbers[i];
    }

    /* Synchronize and reclaim worker */
    int worker_res = 0;
    if (thrd_join(worker, &worker_res) != thrd_success || worker_res != thrd_success) {
        fprintf(stderr, "Worker join error\n");
        return EXIT_FAILURE;
    }

    int total_sum = main_sum + task1.partial_sum;
    printf("Total Computed Sum: %d\n", total_sum);
    return EXIT_SUCCESS;
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- **Undefined Behavior (Self-Join):** A thread calling `thrd_join(thrd_current(), ...)` attempts to join itself, causing immediate deadlock and undefined behavior.
- **Undefined Behavior (Multiple Joins):** Invoking `thrd_join` concurrently or sequentially more than once on the same `thrd_t` is undefined behavior.
- **Undefined Behavior (Detached Join):** Calling `thrd_join` on a thread handle that was previously detached via `thrd_detach`.

## Edge Cases and Failure Modes
- **Deadlocks from Circular Joins:** Thread A joins Thread B while Thread B is waiting to join Thread A.
- **Permanent Suspension:** If the child thread enters an infinite loop, blocks indefinitely on a deadlocked mutex, or experiences an unhandled hardware exception, the joining thread remains blocked forever.
- **Passing Stack Pointers Across Scopes:** If `task1` in the example were destroyed before `thrd_join` returned, undefined behavior would occur.

## Embedded Implications
- **Lack of Timeouts:** Unlike POSIX (`pthread_timedjoin_np`), ISO C11 `thrd_join` provides no timeout parameter. If a worker hangs, the calling thread hangs indefinitely.
- **Watchdog Triggers:** Blocking on `thrd_join` in the main loop of an embedded system without servicing hardware watchdogs will induce unintended microcontroller hardware resets.

## Firmware Review Angle
- **Inspect Lifecycle Termination:** Ensure every non-detached thread has exactly one deterministic call site to `thrd_join`.
- **Review Preemption Hazards:** Verify that tasks executing `thrd_join` do not hold critical locks or peripheral mutexes required by the child thread to finish.
- **Audit Join Order:** Ensure hierarchical join ordering to prevent cyclic wait conditions across thread trees.

## Compiler, ABI, and Toolchain Implications
- **Memory Fences:** `thrd_join` acts as an acquire memory fence. Compilers cannot hoist memory reads in the parent thread above the `thrd_join` call site.
- **Handle Invalidation:** Once joined, the `thrd_t` handle is invalidated. Reusing the variable without reassignment from `thrd_create` is an immediate defect.

## Performance, Memory, Timing, and Power
- **Latency Cost:** Blocking inside `thrd_join` triggers OS scheduler context switches, descheduling the calling thread and putting it into an unrunnable wait queue.
- **Zero Heap Overhead:** Unlike channel communication, joining transfers completion status purely through stack/register passing.

## Verification / Debugging
- **ThreadSanitizer (TSan):** Automatically traces happens-before edges between `thrd_exit`/return and `thrd_join`, verifying memory access safety on shared context structs.
- **Deadlock Detection:** Valgrind (`drd` or `helgrind`) flags join cycles and missing joins.

## Safety, Security, and Reliability
- **Resource Exhaustion Attacks:** Failing to join threads allows uncollected metadata and stacks to consume the process address space, precipitating Denial-of-Service (DoS).
- **Deterministic Shutdown:** Graceful shutdown procedures must sequentially join all active workers before unmapping memory buffers, unloading dynamic libraries, or powering down peripherals.

## Trade-offs and Alternatives
- **`thrd_join` vs. Detached Event Flags:** Joining requires dedicated caller suspension. If the caller must remain responsive, use a detached worker that signals an atomic flag or condition variable upon exit.
- **Thread Pools:** Instead of joining individual short-lived threads, submit tasks to a persistent worker pool and wait on a completion barrier or countdown latch.

## Staff-Level Takeaway
`thrd_join` is the bedrock of fork-join parallelism and structured concurrency in C. It is both a lifecycle cleanup call and a hard memory synchronization boundary. In embedded and mission-critical software, design systems so that joining is never indefinite: guarantee that target threads have deterministic, bounded execution paths that cannot deadlock.

## Related Concepts
- [[00_Chapter_Index]]
- [[01_thrd_create]]
- [[03_thrd_detach]]
- [[04_Thread_return_values]]
- [[12_Thread_safe_module_design]]
