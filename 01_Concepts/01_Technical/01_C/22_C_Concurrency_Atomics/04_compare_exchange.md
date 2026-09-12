# 04: Compare and Exchange (CAS)

## Definition
Compare-and-Exchange (CAS) is the cornerstone synchronization primitive for building lock-free data structures. It atomically compares the value of an atomic object with an expected value: if they are equal, it overwrites the object with a desired value and returns `true`; if they are not equal, it loads the actual current value of the object into the expected variable and returns `false`.

## Scope and Boundaries
Covers: `atomic_compare_exchange_weak`, `atomic_compare_exchange_strong`, memory ordering pairs (success vs failure), CAS retry loops, and spurious failures.
Does not cover: Double-wide CAS (DCAS / 128-bit CAS).

## Why Does It Exist
Atomic RMW functions (`atomic_fetch_add`) are limited to basic math and bitwise operations. Complex state transitions, lock-free stack updates, and atomic pointer swaps require conditionally updating memory only if the state has not changed since it was read. CAS enables arbitrary atomic state transitions.

## Mechanism and Language Rules
1. **Signatures:**
   ```c
   bool atomic_compare_exchange_weak(volatile _Atomic(T)* obj, T* expected, T desired);
   bool atomic_compare_exchange_strong(volatile _Atomic(T)* obj, T* expected, T desired);
   ```
2. **In-Out Parameter (`expected`):** The `expected` argument is passed as a pointer. On failure, the hardware updates `*expected` with the actual value currently in `obj`.
3. **Weak vs Strong:**
   - `atomic_compare_exchange_weak`: Allowed to fail spuriously (return `false` even if `*obj == *expected`) due to cache line eviction or hardware interrupts on LL/SC architectures. Must be used in a loop.
   - `atomic_compare_exchange_strong`: Guaranteed to fail ONLY if `*obj != *expected`. Use when branching conditionally outside of a loop.
4. **Dual Memory Ordering:** Accepts distinct memory orders for success and failure:
   `atomic_compare_exchange_weak_explicit(obj, expected, desired, success_order, failure_order)`.

## Examples
```c
#include <stdatomic.h>
#include <stdint.h>
#include <stdbool.h>

/* Lock-free atomic maximum updater */
void atomic_maximize(atomic_uint32_t *target, uint32_t val) {
    uint32_t current = atomic_load_explicit(target, memory_order_relaxed);
    
    /* CAS loop with weak compare-exchange */
    while (val > current && 
           !atomic_compare_exchange_weak_explicit(
               target,
               &current,  /* Automatically updated on failure */
               val,
               memory_order_release,
               memory_order_relaxed)) {
        /* Loop body empty: current already reloaded with actual value */
    }
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- Specifying a `failure_order` that is stronger than `success_order` or using `memory_order_release` / `memory_order_acq_rel` for `failure_order` invokes Undefined Behavior (§7.17.7.4).

## Edge Cases and Failure Modes
- **The ABA Problem:** A thread reads value $A$, is preempted, another thread changes $A 	o B 	o A$, and the first thread's CAS succeeds even though the state changed in between. Mitigate using tagged pointers or version counters.
- **Infinite Spin on High Contention:** On heavily contended shared objects, a CAS loop can starve low-priority threads.

## Embedded Implications
- On ARM Cortex-M and RISC-V, `weak` maps directly to a single `LDREX`/`STREX` pair without retry logic, making `weak` significantly faster than `strong` when used inside loops.

## Firmware Review Angle
- Confirm that `atomic_compare_exchange_weak` is ALWAYS enclosed within a `while` or `do-while` loop.
- Verify that `failure_order` is never `memory_order_release` or `memory_order_acq_rel`.

## Compiler, ABI, and Toolchain Implications
- On x86, `weak` and `strong` both compile to the `LOCK CMPXCHG` instruction. On ARM and RISC-V, `strong` emits an internal loop to retry spurious failures.

## Performance, Memory, Timing, and Power
- Lock-free CAS structures guarantee system-wide progress without operating system context switches.

## Verification / Debugging
- ThreadSanitizer flags CAS race conditions and memory ordering violations.

## Safety, Security, and Reliability
- Eliminates deadlock liabilities in safety-critical systems by eliminating blocking mutex primitives.

## Trade-offs and Alternatives
- **Weak vs Strong:** Always use `weak` in loops (optimal performance on ARM/RISC-V). Use `strong` when a single-shot CAS decision is required outside of a loop.

## Staff-Level Takeaway
Use `atomic_compare_exchange_weak` inside loops for lock-free state machines and bounded updates. Leverage the automatic update of `*expected` to eliminate redundant loads in the retry loop, and ensure the failure ordering is no stronger than the success ordering.

## Related Concepts
- `03_Read_modify_write`
- `06_acquire_release`
- `10_Atomic_pointers`
