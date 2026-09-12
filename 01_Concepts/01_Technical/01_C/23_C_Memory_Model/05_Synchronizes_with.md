# 05: The `synchronizes-with` Relationship

## Definition
The "synchronizes-with" relationship is the formal inter-thread synchronization mechanism defined in ISO C11 §5.1.2.4. It acts as the bridge connecting two distinct threads of execution: an atomic release operation in one thread synchronizes-with an atomic acquire operation in another thread that reads the written value (or reads from its release sequence).

## Scope and Boundaries
Covers: Release stores, acquire loads, release sequences, consume operations, and thread bridge mechanics.
Does not cover: Intra-thread sequenced-before relationships (see `03_Happens_before`).

## Why Does It Exist
Threads execute concurrently on independent CPU cores with separate hardware store buffers and registers. The `synchronizes-with` relationship is the exact linguistic and architectural protocol that forces memory side effects produced by one core to become visible to another core.

## Mechanism and Language Rules
1. **The Core Rule:** An atomic operation $A$ that performs a release store on object $M$ *synchronizes-with* an atomic operation $B$ that performs an acquire load on object $M$, IF AND ONLY IF $B$ reads the value stored by $A$ (or by a subsequent operation in $A$'s release sequence).
2. **Release Sequence:** Once an atomic release store is performed, any subsequent atomic Read-Modify-Write (RMW) operations performed by any thread on that object continue the release sequence, allowing subsequent acquire loads to synchronize with the original release store.

## Diagram
$$\begin{array}{ccc}
\textbf{Thread 1} & & \textbf{Thread 2} \\[4pt]
\text{write}(x = 42) & & \\[2pt]
\downarrow \text{ (sequenced-before)} & & \\[2pt]
\text{atomic\_store(}flag, \text{release)} & \xrightarrow{\text{synchronizes-with}} & \text{atomic\_load(}flag, \text{acquire)} \\[2pt]
& & \downarrow \text{ (sequenced-before)} \\[2pt]
& & \text{read}(x) \implies 42
\end{array}$$

## Examples
```c
#include <stdatomic.h>
#include <stdint.h>
#include <stdbool.h>
#include <assert.h>

static int         g_dma_buffer[128];
static atomic_bool g_dma_complete;

/* DMA Interrupt Service Routine (Producer) */
void dma_isr_handler(void) {
    /* 1. Hardware populated g_dma_buffer */
    g_dma_buffer[0] = 0xAA;
    g_dma_buffer[127] = 0x55;

    /* 2. Release store: establishes the synchronizes-with anchor */
    atomic_store_explicit(&g_dma_complete, true, memory_order_release);
}

/* Worker Thread (Consumer) */
void worker_thread(void) {
    /* 3. Acquire load: completes the synchronizes-with bridge */
    if (atomic_load_explicit(&g_dma_complete, memory_order_acquire)) {
        /* 4. Guaranteed: Synchronizes-with bridge makes all buffer writes visible! */
        assert(g_dma_buffer[0] == 0xAA);
        assert(g_dma_buffer[127] == 0x55);
    }
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- If the acquire load reads a value written by a *different* operation that was not part of the release sequence, the synchronizes-with relationship is NOT established, and reading companion data invokes Undefined Behavior (Data Race).

## Edge Cases and Failure Modes
- **Reading False in a Polling Loop:** In `while (!atomic_load_explicit(&flag, acquire))`, the iterations that read `false` do NOT synchronize with the release store. ONLY the final iteration that reads `true` establishes the synchronizes-with bridge.

## Embedded Implications
- **Memory Barrier Synthesis:** On ARMv7-M / ARMv8-M, `synchronizes-with` compels the compiler to place a `DMB` barrier before the release store and after the acquire load, forcing hardware bus buffers to flush.

## Firmware Review Angle
- Confirm that every release store is explicitly read by an acquire load before dependent shared variables are accessed.
- Ensure flag resets use appropriate ordering so that subsequent cycles re-establish synchronization cleanly.

## Compiler, ABI, and Toolchain Implications
- In LLVM and GCC, `synchronizes-with` prevents optimization passes from floating non-atomic memory accesses across the atomic synchronization boundary.

## Performance, Memory, Timing, and Power
- Provides maximum execution speed for multi-threaded handoffs by using directed one-way barriers instead of full bidirectional bus stalls.

## Verification / Debugging
- ThreadSanitizer uses synchronizes-with tracking to compute vector clocks and prove race-freedom.

## Safety, Security, and Reliability
- Forms the core requirement for proving deterministic inter-task synchronization in safety-critical firmware architectures.

## Trade-offs and Alternatives
- **Synchronizes-With vs Mutex Lock:** Mutexes establish synchronizes-with automatically upon `unlock` -> `lock`, but atomics establish it with zero OS context switching.

## Staff-Level Takeaway
`synchronizes-with` is the inter-thread bridge of the C memory model. An atomic release store does nothing on its own; it becomes effective only when paired with an acquire load that reads the stored value. Master this pairing to safely pass data across threads and interrupts.

## Related Concepts
- `03_Happens_before`
- `06_Visible_side_effects`
- `../22_C_Concurrency_Atomics/06_acquire_release`
