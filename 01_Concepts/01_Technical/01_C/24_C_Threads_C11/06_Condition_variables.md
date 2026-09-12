# 06: Condition Variables

## Definition
A condition variable in C11 (`cnd_t`) is a synchronization primitive that enables threads to block execution until a specific application-defined boolean predicate becomes true. It works in strict pairing with an associated mutex (`mtx_t`), allowing threads to atomically release the mutex and sleep, and to re-acquire the mutex upon waking up.

## Scope and Boundaries
- **Covers:** `cnd_t` lifecycle, `cnd_wait`, `cnd_timedwait`, `cnd_signal`, `cnd_broadcast`, spurious wakeups, and predicate verification loops.
- **Does not cover:** Semaphore primitives, atomic flags, or direct thread-to-thread message queues.

## Why Does It Exist
Without condition variables, a thread waiting for a specific condition (e.g., buffer has data) would have to repeatedly poll the shared state in a spin-loop with a mutex:
- **Eliminates Busy-Waiting:** Eliminates 100% CPU spinning and cache thrashing while waiting for state transitions.
- **Atomicity of Sleep and Release:** Solves the classic race condition where an event notification arrives between releasing the mutex and going to sleep.

## Mechanism and Language Rules
- **Lifecycle Functions:**
  - `int cnd_init(cnd_t *cond);`
  - `void cnd_destroy(cnd_t *cond);`
  - `int cnd_wait(cnd_t *cond, mtx_t *mutex);`
  - `int cnd_timedwait(cnd_t *restrict cond, mtx_t *restrict mutex, const struct timespec *restrict time_point);`
  - `int cnd_signal(cnd_t *cond);` — wakes at least one waiting thread.
  - `int cnd_broadcast(cnd_t *cond);` — wakes all waiting threads.
- **Atomicity Rule:** `cnd_wait` atomically unlocks the specified mutex and places the calling thread on the condition variable's wait queue.
- **Re-acquisition Rule:** When awakened (via signal, broadcast, or spuriously), the thread re-acquires the mutex before `cnd_wait` returns.
- **Spurious Wakeup Rule:** `cnd_wait` can return even if no thread signaled the condition variable. Therefore, `cnd_wait` **must always** be invoked inside a `while (!predicate)` loop.

## Examples
```c
#include <threads.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

#define QUEUE_CAPACITY 16

typedef struct {
    mtx_t lock;
    cnd_t not_empty;
    cnd_t not_full;
    int buffer[QUEUE_CAPACITY];
    size_t head;
    size_t tail;
    size_t count;
    bool shutdown;
} bounded_queue_t;

int queue_init(bounded_queue_t *q) 
{
    if (mtx_init(&q->lock, mtx_plain) != thrd_success) return -1;
    if (cnd_init(&q->not_empty) != thrd_success) {
        mtx_destroy(&q->lock);
        return -1;
    }
    if (cnd_init(&q->not_full) != thrd_success) {
        cnd_destroy(&q->not_empty);
        mtx_destroy(&q->lock);
        return -1;
    }
    q->head = q->tail = q->count = 0;
    q->shutdown = false;
    return 0;
}

void queue_push(bounded_queue_t *q, int item) 
{
    mtx_lock(&q->lock);
    /* ALWAYS use a while loop to guard against spurious wakeups */
    while (q->count == QUEUE_CAPACITY && !q->shutdown) {
        cnd_wait(&q->not_full, &q->lock);
    }
    if (q->shutdown) {
        mtx_unlock(&q->lock);
        return;
    }
    q->buffer[q->tail] = item;
    q->tail = (q->tail + 1) % QUEUE_CAPACITY;
    q->count++;

    cnd_signal(&q->not_empty); /* Notify consumer */
    mtx_unlock(&q->lock);
}

int queue_pop(bounded_queue_t *q, int *out_item) 
{
    mtx_lock(&q->lock);
    while (q->count == 0 && !q->shutdown) {
        cnd_wait(&q->not_empty, &q->lock);
    }
    if (q->count == 0 && q->shutdown) {
        mtx_unlock(&q->lock);
        return -1;
    }
    *out_item = q->buffer[q->head];
    q->head = (q->head + 1) % QUEUE_CAPACITY;
    q->count--;

    cnd_signal(&q->not_full); /* Notify producer */
    mtx_unlock(&q->lock);
    return 0;
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- **Undefined Behavior (Unmatched Mutex):** Calling `cnd_wait` concurrently on the same condition variable with different mutexes produces undefined behavior.
- **Undefined Behavior (Wait Without Lock):** Calling `cnd_wait` without holding the associated mutex is undefined behavior.
- **Undefined Behavior (Destroy Waiting):** Destroying a condition variable while threads are waiting on it is undefined behavior.

## Edge Cases and Failure Modes
- **Lost Wakeups:** Signaling a condition variable when no thread is waiting causes the signal to be permanently lost (condition variables have no internal counter, unlike semaphores). If a predicate changes before the thread begins waiting and no signal follows, the thread sleeps forever.
- **Spurious Wakeups:** Kernel interrupts, context switches, or OS thread migrations can cause `cnd_wait` to return even though no signal was fired. Failing to check the condition in a `while` loop causes corruption.
- **Thundering Herd:** Using `cnd_broadcast` when only one thread can make progress causes all threads to wake up, contend fiercely for the mutex, and all but one to go back to sleep.

## Embedded Implications
- **Memory Consumption:** Each `cnd_t` consumes memory for wait queues. On microcontrollers with limited RAM, allocate condition variables statically.
- **Hard Real-Time Latency:** Signaling triggers context switches whose scheduling latency depends on OS thread priorities.

## Firmware Review Angle
- **Strictly Audit While Loops:** Never accept `if (!condition) cnd_wait(...)`. Enforce `while (!condition) cnd_wait(...)`.
- **Verify Signal Placement:** Ensure `cnd_signal` or `cnd_broadcast` is called either while holding the mutex or immediately after releasing it, ensuring no updates are lost.
- **Check Mutex Binding Consistency:** Confirm that a given `cnd_t` is always paired with the exact same `mtx_t`.

## Compiler, ABI, and Toolchain Implications
- **OS Futex Subsystem:** Under modern Linux/POSIX kernels, condition variables lower to futex sleep operations (`FUTEX_WAIT`, `FUTEX_WAKE`).
- **Timed Wait Clocks:** `cnd_timedwait` takes a `struct timespec` representing an absolute calendar/monotonic timestamp, requiring careful clock configuration (`TIME_UTC`).

## Performance, Memory, Timing, and Power
- **Power Efficiency:** Sleeping on a condition variable suspends the thread, allowing the CPU to enter low-power C-states.
- **Signaling Overhead:** `cnd_signal` unblocks one thread, avoiding the cache thrashing of `cnd_broadcast`.

## Verification / Debugging
- **ThreadSanitizer:** Validates that condition variable predicates are accessed exclusively under mutex protection.
- **Stress Testing:** Test queues with unbalanced producer/consumer speeds to flush out lost signals or deadlock bugs.

## Safety, Security, and Reliability
- **Safety Critical Systems:** In DO-178C or ISO 26262 systems, unbounded `cnd_wait` calls are prohibited; always use `cnd_timedwait` with defined timeout fallbacks.
- **Shutdown Signaling:** Always use `cnd_broadcast` when initiating subsystem shutdown so that all waiting threads unblock and exit cleanly.

## Trade-offs and Alternatives
- **Condition Variable vs. Counting Semaphore:** Semaphores retain signal state via internal counters (signals are not lost). Condition variables are preferred when complex, multi-variable boolean predicates must be satisfied.
- **Lock-Free Ring Buffers:** For single-producer single-consumer (SPSC) pipelines, lock-free ring buffers using atomic indices avoid condition variables and locks altogether.

## Staff-Level Takeaway
Condition variables are not notification flags—they are sleep mechanisms for predicate state machines. Never think of `cnd_signal` as "sending an event"; think of it as "informing sleeping threads to re-evaluate their invariant predicate." The predicate loop is non-negotiable.

## Related Concepts
- [[00_Chapter_Index]]
- [[05_Mutexes]]
- [[09_Thread_cancellation_boundaries]]
- [[12_Thread_safe_module_design]]
