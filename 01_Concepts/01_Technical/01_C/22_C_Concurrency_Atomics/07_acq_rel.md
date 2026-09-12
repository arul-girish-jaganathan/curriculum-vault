# 07: `memory_order_acq_rel`

## Definition
`memory_order_acq_rel` combines both `acquire` and `release` semantics into a single atomic operation. It can ONLY be applied to Read-Modify-Write (RMW) operations (such as `atomic_fetch_add` or `atomic_compare_exchange`). It ensures that the load component of the RMW acts as an `acquire` barrier, while the store component acts as a `release` barrier.

## Scope and Boundaries
Covers: Bidirectional RMW synchronization, read-modify-write barriers, atomic reference counting, and barrier rendezvous patterns.
Does not cover: Pure load or pure store operations (which cannot accept `acq_rel`).

## Why Does It Exist
Certain synchronization patterns require both reading prior state and publishing new state simultaneously. For example, when updating a shared reference counter or passing an ownership token through a chain of threads, each thread must observe all prior work (acquire) and publish its own work to subsequent threads (release) in a single atomic instruction.

## Mechanism and Language Rules
1. **RMW Exclusive:** `memory_order_acq_rel` can ONLY be used with RMW operations. Using it on `atomic_load` or `atomic_store` is a constraint violation.
2. **Dual Barrier Action:**
   - Preceding reads/writes cannot be reordered *after* the store.
   - Subsequent reads/writes cannot be reordered *before* the load.
3. **Synchronization Chain:** Forms a continuous acquire-release release sequence across multiple participating threads.

## Examples
```c
#include <stdatomic.h>
#include <stdint.h>
#include <stdbool.h>

typedef struct {
    atomic_uint_fast32_t ref_count;
    uint8_t              data_buffer[256];
} SharedResource_t;

void resource_retain(SharedResource_t *res) {
    /* Relaxed is sufficient when simply acquiring a new reference */
    atomic_fetch_add_explicit(&res->ref_count, 1U, memory_order_relaxed);
}

void resource_release(SharedResource_t *res) {
    /* 
     * acq_rel ensures that:
     * 1. All writes to data_buffer happen-before the decrement (release).
     * 2. If this is the final drop, we observe all prior writes from other threads (acquire).
     */
    if (atomic_fetch_sub_explicit(&res->ref_count, 1U, memory_order_acq_rel) == 1U) {
        /* Last reference dropped: safely destroy/recycle resource */
        res->data_buffer[0] = 0; /* No race: all other threads have released */
    }
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- Passing `memory_order_acq_rel` to `atomic_load_explicit` or `atomic_store_explicit` invokes Undefined Behavior (§7.17.7.2).

## Edge Cases and Failure Modes
- **Over-Synchronization Overhead:** Using `acq_rel` where `release` alone is sufficient (e.g., on a simple write-only flag) emits unnecessary memory fences on weakly ordered hardware.

## Embedded Implications
- **Token Passing in Dual-Core MCUs:** When passing an atomic token between Core 0 and Core 1 on asymmetric multi-core processors (e.g., LPC55S69, STM32H7), `acq_rel` guarantees bidirectional cache coherency across both cores.

## Firmware Review Angle
- Verify that `memory_order_acq_rel` is applied strictly to RMW functions (`atomic_fetch_*`, `atomic_compare_exchange_*`).
- Audit reference count decrement implementations to ensure proper teardown synchronization.

## Compiler, ABI, and Toolchain Implications
- On ARM processors, `acq_rel` generates both load-acquire and store-release instructions (or standard `LDREX`/`STREX` enclosed by full `DMB` data memory barriers).

## Performance, Memory, Timing, and Power
- Incurs greater pipeline stall overhead than pure acquire or pure release, but remains significantly faster than full sequential consistency (`seq_cst`).

## Verification / Debugging
- ThreadSanitizer mathematically models bidirectional RMW fences to verify absence of data races.

## Safety, Security, and Reliability
- Crucial for deterministic object lifetime management and preventing use-after-free vulnerabilities in shared embedded memory blocks.

## Trade-offs and Alternatives
- **`acq_rel` vs Split Acquire & Release:** Using `acq_rel` executes an atomic bidirectional synchronization in a single cycle, which cannot be achieved using separate loads and stores.

## Staff-Level Takeaway
Reserve `memory_order_acq_rel` for Read-Modify-Write operations that simultaneously conclude one phase of execution and inaugurate another—such as reference-counted teardowns, lock-free queue dequeue operations, and inter-thread token handoffs.

## Related Concepts
- `03_Read_modify_write`
- `06_acquire_release`
- `08_seq_cst`
