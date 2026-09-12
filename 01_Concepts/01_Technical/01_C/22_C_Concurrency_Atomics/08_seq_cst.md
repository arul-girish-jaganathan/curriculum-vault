# 08: `memory_order_seq_cst`

## Definition
`memory_order_seq_cst` (Sequential Consistency) is the strongest memory ordering model in ISO C11 and the default ordering applied when using bare C operators on atomic types. It guarantees that all threads observe all `seq_cst` operations in a single, globally uniform total order, matching the intuitive model of interleaving sequential executions.

## Scope and Boundaries
Covers: Total store ordering, global sequential consistency, default C atomic operators, and hardware fence overhead.
Does not cover: Relaxed or one-way synchronization models.

## Why Does It Exist
Humans intuitively reason about concurrent systems sequentially: if event $A$ happens, then event $B$ happens, everyone must see $A$ before $B$. Weak memory models allow different CPU cores to observe stores in different orders. `seq_cst` eliminates these complex edge cases by forcing hardware to establish a globally agreed-upon sequence of events.

## Mechanism and Language Rules
1. **Total Global Order:** There exists a single, global program order that is consistent with the sequenced-before order of every thread.
2. **Default in C11:** Using built-in operators on atomic types (`atomic_var++`, `atomic_var = 1`) defaults to `memory_order_seq_cst`.
3. **Heavyweight Synchronization:** Enforces bidirectional barriers and drains hardware write buffers globally across all cores.

## Examples
```c
#include <stdatomic.h>
#include <stdint.h>
#include <stdbool.h>
#include <assert.h>

/* Dekker's / Peterson's Algorithm Core Synchronization */
static atomic_bool g_flag_a = false;
static atomic_bool g_flag_b = false;
static int g_winner = 0;

/* Thread A */
void thread_a(void) {
    atomic_store_explicit(&g_flag_a, true, memory_order_seq_cst);
    if (!atomic_load_explicit(&g_flag_b, memory_order_seq_cst)) {
        g_winner = 1; /* Guaranteed that either Thread A or B wins */
    }
}

/* Thread B */
void thread_b(void) {
    atomic_store_explicit(&g_flag_b, true, memory_order_seq_cst);
    if (!atomic_load_explicit(&g_flag_a, memory_order_seq_cst)) {
        g_winner = 2;
    }
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- While `seq_cst` prevents data races on atomic variables, mixing `seq_cst` atomics with non-atomic operations without proper synchronization still invokes Undefined Behavior.

## Edge Cases and Failure Modes
- **The Accidental Barrier Performance Trap:**
  ```c
  /* Naive loop */
  for (int i = 0; i < 1000; ++i) {
      g_atomic_counter++; /* Implicit seq_cst! Emits DMB on every single iteration! */
  }
  ```
  On ARM and RISC-V, this emits hundreds of expensive bus-draining memory barrier instructions, stalling the CPU.

## Embedded Implications
- **Cortex-M Barrier Costs:** On Cortex-M7 with write-back caches, `seq_cst` generates `DMB ISH` (Data Memory Barrier Inner Shareable), draining write buffers and stalling execution pipelines for multiple bus cycles.

## Firmware Review Angle
- Flag any bare assignment or increment operators on atomic types (`val++`); mandate explicit ordering (`atomic_fetch_add_explicit`).
- Verify whether full sequential consistency is genuinely required, or if acquire-release semantics suffice.

## Compiler, ABI, and Toolchain Implications
- On x86 (strongly ordered), `seq_cst` loads are free (`MOV`), but stores require an expensive `MFENCE` or `XCHG`. On ARM (weakly ordered), both loads and stores require memory barriers (`DMB`).

## Performance, Memory, Timing, and Power
- Slowest atomic ordering model. Heavy use of `seq_cst` increases CPU power draw and degrades multi-core throughput due to bus serialization.

## Verification / Debugging
- Sanitizers and formal verification tools easily verify `seq_cst` code due to its mathematically strict total ordering.

## Safety, Security, and Reliability
- Safest and least error-prone model for developers conceptually, but carries the highest runtime performance cost.

## Trade-offs and Alternatives
- **`seq_cst` vs Acquire-Release:** Acquire-release is sufficient for 95% of real-world concurrent patterns (queues, flags, state machines) and runs substantially faster on embedded processors.

## Staff-Level Takeaway
`memory_order_seq_cst` is the safest mental model but the most expensive hardware contract. Never let implicit `seq_cst` slip into performance-critical embedded loops via raw `++` or `=` operators. Profile barrier costs, and default to acquire-release semantics whenever full total store ordering is not strictly required.

## Related Concepts
- `05_memory_order_relaxed`
- `06_acquire_release`
- `07_acq_rel`
- `../23_C_Memory_Model/04_Modification_order`
