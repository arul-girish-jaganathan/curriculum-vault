# 12: Thread-Safe Module Design

## Definition
Thread-Safe Module Design represents the architectural discipline of engineering C modules, libraries, and hardware drivers that behave correctly and predictably when invoked concurrently by multiple threads. It encompasses state encapsulation, reentrancy, lock ordering protocols, fine-grained vs. coarse-grained synchronization, and deadlock prevention strategies.

## Scope and Boundaries
- **Covers:** Reentrant API design, opaque context handles, lock hierarchies, race condition elimination, and shared-state encapsulation.
- **Does not cover:** Specific OS kernel scheduling algorithms, network protocols, or single-threaded optimization techniques.

## Why Does It Exist
Writing multithreaded code is easy; writing thread-safe, deadlock-free, maintainable modules in C is difficult:
- **Absence of Language Protections:** C does not have compiler-enforced data race detection, borrow checkers, or synchronized object classes.
- **Hidden Global State Hazards:** Standard C idioms historically relied on static internal buffers (e.g., `strtok`, `asctime`), which break catastrophically in multithreaded systems.
- **Systemic Deadlocks:** Poorly structured modules that acquire locks in arbitrary order cause intermittent, hard-to-reproduce deadlocks in production environments.

## Mechanism and Language Rules
1. **Eliminate Mutable Global / Static State:**
   - Modules must never store mutable state in static variables.
   - All state must reside in an opaque, caller-allocated context structure passed via pointer (`module_ctx_t *ctx`).
2. **Reentrancy:**
   - A function is reentrant if it can be interrupted in the middle of execution and safely called again by another thread or interrupt before its previous invocation completes.
   - Pure functions relying exclusively on caller-provided arguments and local stack variables are inherently thread-safe and reentrant.
3. **Strict Lock Hierarchies:**
   - Assign a global integer rank to every mutex in the system.
   - A thread holding Mutex of rank $N$ is only permitted to acquire Mutex of rank $M$ if $M > N$.
   - Never acquire locks in reverse order.
4. **Encapsulate Locking Boundaries:**
   - Clients of a module should not need to manage the module's internal locks manually. The module's public API must handle locking internally, or clearly document external locking contracts.

## Examples
```c
/* ==================== safe_ring_buffer.h ==================== */
#ifndef SAFE_RING_BUFFER_H
#define SAFE_RING_BUFFER_H

#include <threads.h>
#include <stdbool.h>
#include <stddef.h>

typedef struct safe_ring_buffer safe_ring_buffer_t;

safe_ring_buffer_t *ring_buffer_create(size_t capacity);
void ring_buffer_destroy(safe_ring_buffer_t *rb);

bool ring_buffer_push(safe_ring_buffer_t *rb, int value);
bool ring_buffer_pop(safe_ring_buffer_t *rb, int *out_value);

#endif

/* ==================== safe_ring_buffer.c ==================== */
#include <stdlib.h>

struct safe_ring_buffer {
    mtx_t lock;
    int *data;
    size_t capacity;
    size_t head;
    size_t tail;
    size_t count;
};

safe_ring_buffer_t *ring_buffer_create(size_t capacity) 
{
    if (capacity == 0) return NULL;

    safe_ring_buffer_t *rb = malloc(sizeof(safe_ring_buffer_t));
    if (!rb) return NULL;

    rb->data = malloc(sizeof(int) * capacity);
    if (!rb->data) {
        free(rb);
        return NULL;
    }

    if (mtx_init(&rb->lock, mtx_plain) != thrd_success) {
        free(rb->data);
        free(rb);
        return NULL;
    }

    rb->capacity = capacity;
    rb->head = rb->tail = rb->count = 0;
    return rb;
}

void ring_buffer_destroy(safe_ring_buffer_t *rb) 
{
    if (!rb) return;
    mtx_destroy(&rb->lock);
    free(rb->data);
    free(rb);
}

bool ring_buffer_push(safe_ring_buffer_t *rb, int value) 
{
    if (!rb) return false;

    mtx_lock(&rb->lock);
    if (rb->count == rb->capacity) {
        mtx_unlock(&rb->lock);
        return false; /* Buffer full */
    }

    rb->data[rb->tail] = value;
    rb->tail = (rb->tail + 1) % rb->capacity;
    rb->count++;

    mtx_unlock(&rb->lock);
    return true;
}

bool ring_buffer_pop(safe_ring_buffer_t *rb, int *out_value) 
{
    if (!rb || !out_value) return false;

    mtx_lock(&rb->lock);
    if (rb->count == 0) {
        mtx_unlock(&rb->lock);
        return false; /* Buffer empty */
    }

    *out_value = rb->data[rb->head];
    rb->head = (rb->head + 1) % rb->capacity;
    rb->count--;

    mtx_unlock(&rb->lock);
    return true;
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- **Undefined Behavior (Dangling Context):** Passing a destroyed context pointer to a module function causes memory corruption and crashes.
- **Undefined Behavior (External Lock Bypassing):** If an API requires external caller-side locking and a thread accesses the object unassisted, data races result in undefined behavior.

## Edge Cases and Failure Modes
- **Callback Deadlocks:** If a module calls an external user-registered callback while holding its internal mutex, and that callback attempts to invoke another function in the same module, immediate deadlock occurs. **Rule:** Never invoke unknown external code while holding an internal lock.
- **Lock Contention Bottlenecks:** Placing an entire module behind a single coarse-grained mutex can serialize application execution, turning multi-core CPUs into single-core bottlenecks.
- **ABA Problem in Lock-Free Modules:** Advanced lock-free modules using atomic compare-and-swap can suffer from the ABA problem if node pointers are recycled without versioning or hazard pointers.

## Embedded Implications
- **Shared Peripheral Access:** Hardware peripherals (SPI bus, I2C bus, UART) are shared resources. Thread-safe driver modules must serialize bus transactions using mutexes or arbiter tasks.
- **Static Instantiation Support:** In embedded systems where dynamic allocation is forbidden, provide static initialization functions (`module_init_static(module_ctx_t *ctx, uint8_t *buffer, size_t size)`).

## Firmware Review Angle
- **Search for `static` Variables:** Grep codebase for `static` variables inside function bodies or file scopes. Every mutable static variable is an immediate concurrency red flag.
- **Inspect Callback Sites:** Ensure module locks are released *before* calling user callback functions.
- **Audit Error Exits:** Ensure every error return branch (`if (err) return -1;`) unlocks any acquired mutexes before returning.

## Compiler, ABI, and Toolchain Implications
- **Opaque Pointers (Pimpl Idiom):** Exposing module structs only as incomplete forward declarations (`typedef struct safe_ring_buffer safe_ring_buffer_t;`) in header files prevents clients from accessing struct fields directly or bypassing mutex locks.
- **Link-Time Optimization (LTO):** LTO can optimize internal helper functions while maintaining strict encapsulation boundaries across modules.

## Performance, Memory, Timing, and Power
- **Granularity Trade-off:**
  - *Coarse-Grained Locking:* Simple, easy to verify, low memory overhead; high contention under load.
  - *Fine-Grained Locking:* High concurrency, scalable; high memory overhead (many mutexes), complex lock ordering, high risk of deadlocks.
- **Cache Line Bouncing:** High lock contention causes cache line invalidation across CPU core caches, degrading overall memory bandwidth.

## Verification / Debugging
- **ThreadSanitizer (TSan):** Essential for verifying that module APIs are free of data races during concurrent integration tests.
- **Static Analysis:** Tools like Coverity, Polyspace, and clang-tidy enforce reentrancy rules and check for unreleased locks.

## Safety, Security, and Reliability
- **Defensive Programming:** Always validate context pointers (`if (!ctx) return ERR_NULL_PTR;`) at public module API boundaries.
- **Fail-Safe State:** Ensure that if an error occurs inside a critical section, the module state remains consistent before releasing the lock and reporting the failure.

## Trade-offs and Alternatives
- **Internal vs External Synchronization:**
  - *Internal Locking:* Caller does not worry about locks; every call incurs lock overhead, even in single-threaded environments.
  - *External Locking:* Module is pure/unlocked; single-threaded users pay zero lock cost, but multithreaded callers assume full liability for synchronization.
- **Actor Model / Message Passing:** Instead of sharing module state behind locks, run the module in its own dedicated worker thread and communicate exclusively via message queues.

## Staff-Level Takeaway
True thread safety is an architectural attribute, not an afterthought achieved by wrapping mutexes around random functions. Design modules around reentrancy, complete encapsulation of mutable state within opaque context handles, strict lock hierarchies, and zero locks held during external callbacks.

## Related Concepts
- [[00_Chapter_Index]]
- [[05_Mutexes]]
- [[06_Condition_variables]]
- [[07_Thread_local_storage]]
- [[08_Call_once]]
- [[10_C11_thread_portability]]
