# 03: The `happens-before` Relationship

## Definition
The "happens-before" relationship (ISO C11 §5.1.2.4) is the central formal mathematical partial order defining memory visibility and execution ordering in C. If event $A$ happens-before event $B$ ($A \to B$), then the memory state and side effects produced by $A$ are guaranteed to be visible to, and precede, event $B$.

## Scope and Boundaries
Covers: Program order (sequenced-before), inter-thread ordering (synchronizes-with), transitive closure, and visibility guarantees.
Does not cover: Physical wall-clock time (which does not dictate memory ordering).

## Why Does It Exist
Due to CPU instruction pipelines, out-of-order execution, and compiler optimizations, the fact that instruction $A$ executed before instruction $B$ in physical wall-clock time does NOT mean its memory writes are visible to instruction $B$. The happens-before relation establishes the formal mathematical contract for true memory visibility.

## Mechanism and Language Rules
1. **Sequenced-Before (Single Thread):** Within a single thread of execution, evaluation $A$ is sequenced-before evaluation $B$ if it precedes it in program order. Sequenced-before implies happens-before.
2. **Synchronizes-With (Inter-Thread):** An atomic release store in Thread 1 that synchronizes-with an atomic acquire load in Thread 2 establishes an inter-thread happens-before edge.
3. **Transitivity:** If $A$ happens-before $B$ ($A \to B$) and $B$ happens-before $C$ ($B \to C$), then $A$ happens-before $C$ ($A \to C$).

## Mathematical Formulation
$$\text{Sequenced-Before } (A \to B) \quad \lor \quad \text{Synchronizes-With } (A \to B) \implies A \prec B$$
$$\text{Transitivity: } (A \prec B) \land (B \prec C) \implies A \prec C$$

## Examples
```c
#include <stdatomic.h>
#include <stdbool.h>
#include <assert.h>

static int         g_payload = 0;
static atomic_bool g_guard = false;

/* Thread 1 */
void thread_1_producer(void) {
    g_payload = 42; /* Operation A */
    /* Operation A is sequenced-before Operation B */
    atomic_store_explicit(&g_guard, true, memory_order_release); /* Operation B */
}

/* Thread 2 */
void thread_2_consumer(void) {
    /* Operation C */
    while (!atomic_load_explicit(&g_guard, memory_order_acquire)) {
        /* Busy wait */
    }
    /* Operation C is sequenced-before Operation D */
    int val = g_payload; /* Operation D */
    
    /* 
     * FORMAL PROOF OF HAPPENS-BEFORE:
     * A is sequenced-before B (A -> B)
     * B synchronizes-with C   (B -> C)
     * C is sequenced-before D (C -> D)
     * By Transitivity: A happens-before D (A -> D)
     * Result: val is GUARANTEED to be 42!
     */
    assert(val == 42);
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- If two memory operations access the same location and are NOT ordered by a happens-before relationship, and at least one is a write, they form a Data Race (Undefined Behavior).

## Edge Cases and Failure Modes
- **Broken Transitivity Chains:** If any link in the chain uses `memory_order_relaxed` instead of acquire-release, the synchronizes-with edge is broken, destroying the happens-before relationship and re-introducing data races.

## Embedded Implications
- **DMA Completion Synchronization:** When a DMA engine finishes filling a buffer, a hardware interrupt fires. The ISR must establish a happens-before relationship (using a release barrier) before setting an event flag for the processing thread.

## Firmware Review Angle
- Trace the chain of operations between producer and consumer: verify that a rigorous happens-before relationship connects the write to the read.

## Compiler, ABI, and Toolchain Implications
- Compilers respect the happens-before relationship: optimization passes are mathematically forbidden from moving memory reads before an acquire operation or writes after a release operation.

## Performance, Memory, Timing, and Power
- Establishing happens-before edges using acquire-release atomics minimizes memory fence instructions, delivering optimal execution speed.

## Verification / Debugging
- Formal verification tools (such as TSan and Herd7) analyze memory model graphs using happens-before axioms to detect concurrency defects.

## Safety, Security, and Reliability
- The foundational theorem of modern concurrent software verification in ISO 26262 and DO-178C.

## Trade-offs and Alternatives
- **Happens-Before via Mutex vs Atomics:** Acquiring and releasing an OS mutex automatically establishes a happens-before edge, but costs hundreds of clock cycles compared to single-cycle atomic operations.

## Staff-Level Takeaway
Never assume physical execution order equals visibility. Memory visibility exists if and only if a formal happens-before relationship links the operations. Build happens-before chains using program order and acquire-release synchronization to guarantee determinism.

## Related Concepts
- `02_Data_races`
- `05_Synchronizes_with`
- `06_Visible_side_effects`
