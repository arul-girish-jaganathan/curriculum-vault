# 05: Mutexes

## Definition
A mutex (mutual exclusion primitive) in C11 (`mtx_t`) is a synchronization object used to protect shared resources from concurrent access by multiple threads. It guarantees that only one thread can hold ownership of the critical section at any given instant, establishing serialized access and memory visibility barriers.

## Scope and Boundaries
- **Covers:** `mtx_t` initialization, types (`mtx_plain`, `mtx_recursive`, `mtx_timed`), locking (`mtx_lock`, `mtx_trylock`, `mtx_timedlock`), unlocking (`mtx_unlock`), and destruction (`mtx_destroy`).
- **Does not cover:** Condition variables ([[06_Condition_variables]]), atomics (`<stdatomic.h>`), or read-write locks (not standardized in C11).

## Why Does It Exist
When multiple threads read and write shared memory concurrently without synchronization, data races occur, resulting in memory corruption and undefined behavior:
- **Mutual Exclusion:** Prevents concurrent execution of conflicting critical sections.
- **Memory Visibility / Ordering:** Unlocking a mutex synchronizes-with the subsequent lock acquisition of that mutex by any thread, ensuring that all writes inside the critical section become visible to the next owner.
- **Portability:** Replaces POSIX `pthread_mutex_t` and Windows `CRITICAL_SECTION` with an ISO C standardized abstraction.

## Mechanism and Language Rules
- **Mutex Types:**
  - `mtx_plain`: Simple, non-recursive mutex.
  - `mtx_recursive`: Allows the owning thread to acquire the lock multiple times without deadlocking itself.
  - `mtx_timed`: Supports time-bounded locking attempts (`mtx_timedlock`).
  - Bitwise combinations: `mtx_plain | mtx_recursive` or `mtx_timed | mtx_recursive`.
- **Lifecycle Functions:**
  - `int mtx_init(mtx_t *mutex, int type);` — returns `thrd_success` or `thrd_error`.
  - `void mtx_destroy(mtx_t *mutex);` — releases OS mutex resources.
  - `int mtx_lock(mtx_t *mutex);` — blocks until acquired.
  - `int mtx_trylock(mtx_t *mutex);` — non-blocking; returns `thrd_busy` if locked.
  - `int mtx_timedlock(mtx_t *restrict mutex, const struct timespec *restrict time_point);`
  - `int mtx_unlock(mtx_t *mutex);` — releases lock.

## Examples
```c
#include <threads.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    mtx_t lock;
    int counter;
    int is_initialized;
} safe_counter_t;

static safe_counter_t g_counter;

int counter_init(void) 
{
    if (mtx_init(&g_counter.lock, mtx_plain) != thrd_success) {
        return -1;
    }
    g_counter.counter = 0;
    g_counter.is_initialized = 1;
    return 0;
}

void counter_increment(void) 
{
    if (mtx_lock(&g_counter.lock) == thrd_success) {
        /* Critical Section */
        g_counter.counter++;
        mtx_unlock(&g_counter.lock);
    }
}

int counter_get(void) 
{
    int val = 0;
    if (mtx_lock(&g_counter.lock) == thrd_success) {
        val = g_counter.counter;
        mtx_unlock(&g_counter.lock);
    }
    return val;
}

void counter_destroy(void) 
{
    mtx_destroy(&g_counter.lock);
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- **Undefined Behavior (Double Lock on Plain):** Calling `mtx_lock` twice on an `mtx_plain` mutex from the same thread causes deadlock or undefined behavior.
- **Undefined Behavior (Unlock Unowned):** Calling `mtx_unlock` on a mutex that is not owned by the calling thread causes undefined behavior.
- **Undefined Behavior (Destroy Locked):** Calling `mtx_destroy` on a mutex that is currently locked or has threads waiting on it is undefined behavior.
- **Undefined Behavior (Copying Mutex):** Mutex objects cannot be copied; `mtx_t copy = g_counter.lock;` invokes undefined behavior if the copy is manipulated.

## Edge Cases and Failure Modes
- **Deadlocks from Inconsistent Lock Ordering:** Thread 1 acquires Mutex A then Mutex B; Thread 2 acquires Mutex B then Mutex A. Both block indefinitely.
- **Priority Inversion:** A low-priority thread holds a mutex; a medium-priority thread preempts it; a high-priority thread blocks on the mutex, effectively delayed by the medium thread.
- **Exception / Early Exit Leak:** Returning from an error branch inside a critical section without calling `mtx_unlock` permanently starves all other threads.

## Embedded Implications
- **Priority Inheritance:** C11 does not specify priority inheritance protocols. On RTOS targets, verify whether the underlying OS mutex implementation defaults to priority inheritance (e.g., `PTHREAD_PRIO_INHERIT` under POSIX).
- **ISR Restrictions:** Mutexes must **never** be locked or unlocked inside Interrupt Service Routines (ISRs) because ISRs cannot block and do not possess thread context.

## Firmware Review Angle
- **RAII / Cleanup Patterns:** In C, emulate cleanup guards using `__attribute__((cleanup))` or strictly enforce single-point-of-exit (`goto unlock;`) idioms.
- **Audit Lock Hierarchy:** Ensure a globally documented, monotonically increasing lock acquisition order across all modules.
- **Minimize Scope:** Critical sections must be as short as possible; never perform blocking I/O, flash writes, or unbounded loops while holding a mutex.

## Compiler, ABI, and Toolchain Implications
- **Hardware Primitives:** Mutex operations lower to atomic compare-and-swap (`CAS`, `LDREX`/`STREX`, `lock cmpxchg`) and OS futex system calls (`futex` on Linux, `WaitOnAddress` on Windows).
- **Compiler Optimization Barrier:** The compiler treats `mtx_lock` and `mtx_unlock` as full optimization barriers; local reads/writes cannot be reordered across the lock boundary.

## Performance, Memory, Timing, and Power
- **Fast Path:** Uncontended mutex lock/unlock executes in user-space via atomic instructions (~10–25 ns).
- **Slow Path:** Contended locks trigger OS context switches, putting threads to sleep and burning CPU cycles during thread rescheduling.
- **Power:** Mutex sleep puts the core into lower power compared to spinlocks, but frequent context switching increases dynamic power draw.

## Verification / Debugging
- **ThreadSanitizer (TSan):** Automatically identifies data races resulting from missing mutex protection.
- **Valgrind Helgrind:** Detects lock hierarchy violations, inconsistent lock ordering, and destruction of locked mutexes.

## Safety, Security, and Reliability
- **Denial of Service (DoS):** Unhandled crashes while holding a mutex render shared resources permanently inaccessible.
- **Recursive Mutex Hazards:** Recursive mutexes mask bad architectural design, making it difficult to reason about invariants at function entry. Avoid `mtx_recursive` unless designing reentrant legacy wrappers.

## Trade-offs and Alternatives
- **Mutex vs. C11 Atomics:** For single variables, atomic operations (`atomic_fetch_add`, `atomic_store`) are lock-free, faster, and immune to deadlocks.
- **Mutex vs. Spinlock:** Spinlocks waste CPU cycles spinning; mutexes deschedule. Spinlocks are only appropriate for ultra-low latency, sub-microsecond sections in kernel/embedded drivers.

## Staff-Level Takeaway
A mutex protects an *invariant*, not just a variable. Every mutex must be explicitly bound to the shared state and invariants it guards. Always prefer coarse-grained, provably correct locking hierarchies over micro-mutex architectures that complicate lock graphs and invite deadlocks.

## Related Concepts
- [[00_Chapter_Index]]
- [[06_Condition_variables]]
- [[08_Call_once]]
- [[12_Thread_safe_module_design]]
