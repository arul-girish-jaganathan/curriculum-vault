# 06: Visible Side Effects

## Definition
A visible side effect (ISO C11 §5.1.2.4) is the formal rule determining whether a write to a memory location is visible to a subsequent read. A side effect (write) $A$ on a scalar object is visible to a value computation (read) $B$ if and only if $A$ happens-before $B$, and there exists no intervening side effect $C$ that happens-after $A$ and happens-before $B$.

## Scope and Boundaries
Covers: Memory freshness, visibility rules, intervening writes, and multiple conflicting side effects.
Does not cover: Physical hardware bus snooping mechanics.

## Why Does It Exist
Compilers and processors may buffer or reorder writes. Just because a write occurred somewhere in the program does not mean a reader is legally entitled to see it. The visible side effect rule dictates the exact mathematical criteria under which a read is guaranteed to observe a specific write.

## Mechanism and Language Rules
1. **Visibility Criteria:** Write $A$ is visible to read $B$ if:
   - $A$ happens-before $B$ ($A \prec B$).
   - There is no other write $C$ such that $A \prec C \prec B$.
2. **Conflicting Invisible Writes:** If write $A$ does NOT happen-before read $B$, the value read is undefined or forms a Data Race.
3. **Atomic Object Visibility:** For atomic objects, the read observes either the latest write in the happens-before tree or a write in the object's modification order.

## Mathematical Formulation
$$\text{Side Effect } A \text{ is visible to } B \iff (A \prec B) \land \neg \exists C : (A \prec C \prec B)$$

## Examples
```c
#include <stdatomic.h>
#include <stdint.h>
#include <assert.h>

static int         g_data = 0;
static atomic_bool g_sync = false;

/* Thread 1 */
void writer_thread(void) {
    g_data = 10; /* Write A */
    g_data = 20; /* Write C: Intervening write! */

    /* Release store ensures Write C happens-before anything acquiring g_sync */
    atomic_store_explicit(&g_sync, true, memory_order_release);
}

/* Thread 2 */
void reader_thread(void) {
    while (!atomic_load_explicit(&g_sync, memory_order_acquire)) {
        /* Wait */
    }

    /* 
     * Read B:
     * Write A happens-before Read B.
     * BUT Write C also happens-before Read B, and Write C happens-after Write A.
     * Therefore, Write A is NOT visible; ONLY Write C is visible!
     */
    int result = g_data; /* Guaranteed to read 20, NEVER 10! */
    assert(result == 20);
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- If a read has multiple visible side effects that are not ordered by happens-before, the program has a Data Race, provoking Undefined Behavior.

## Edge Cases and Failure Modes
- **Stale Cache Line Reads:** On systems without cache coherency, failure to issue software cache invalidate instructions means a core reads stale SRAM data, violating the visibility model.

## Embedded Implications
- **DMA Buffer Visibility:** Non-coherent DMA requires explicit cache cleaning (`SCB_CleanDCache`) before starting DMA transmission and cache invalidation (`SCB_InvalidateDCache`) before reading DMA receive buffers to ensure side effects are physically visible in RAM.

## Firmware Review Angle
- When inspecting concurrency paths, verify that no intermediate writes unexpectedly overwrite the intended payload before the release synchronization occurs.

## Compiler, ABI, and Toolchain Implications
- The compiler optimizer analyzes visible side effects to eliminate dead stores (e.g., removing `g_data = 10` above if it can prove no thread can read it before it is overwritten by `g_data = 20`).

## Performance, Memory, Timing, and Power
- Clean visibility tracking enables aggressive compiler dead-store elimination, reducing unnecessary memory traffic.

## Verification / Debugging
- ThreadSanitizer flags reads that lack an unambiguous visible side effect.

## Safety, Security, and Reliability
- Critical for verifying that sensor readings and fault flags read by safety monitors reflect the freshest system state.

## Trade-offs and Alternatives
- **Synchronized Visibility vs Frequent Polling:** Polling without synchronization leads to stale reads; acquire-release guarantees immediate visibility upon signal arrival.

## Staff-Level Takeaway
A write is visible to a read if and only if it happens-before the read and no intervening write overwrites it. Guarantee visibility by routing shared data through clean happens-before chains anchored by atomic synchronization.

## Related Concepts
- `03_Happens_before`
- `05_Synchronizes_with`
- `07_Atomic_vs_non_atomic_access`
