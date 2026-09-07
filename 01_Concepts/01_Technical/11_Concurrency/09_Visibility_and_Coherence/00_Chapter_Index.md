# 09 Visibility and Coherence

## Chapter map

- [[Visibility_Problem|01. Visibility Problem]]
- [[Cache_Coherence|02. Cache Coherence]]
- [[Compiler_Visibility|03. Compiler Visibility]]
- [[CPU_Visibility|04. CPU Visibility]]
- [[Stale_Reads|05. Stale Reads]]
- [[Write_Propagation|06. Write Propagation]]
- [[Coherence_vs_Ordering|07. Coherence vs Ordering]]
- [[Volatile_Limitations|08. Volatile Limitations]]
- [[Atomics_for_Visibility|09. Atomics for Visibility]]
- [[Locks_for_Visibility|10. Locks for Visibility]]
- [[MMIO_Visibility|11. MMIO Visibility]]
- [[Debugging_Visibility_Bugs|12. Debugging Visibility Bugs]]

## Chapter purpose
This chapter builds a reusable mental model for **Visibility and Coherence**, with emphasis on correctness, timing, memory ordering, lifecycle, debugging, and embedded-system consequences.

## Cross-chapter reasoning
- Start with state ownership.
- Identify execution contexts and possible interleavings.
- State the synchronization edge or ownership transfer.
- Prove safety and liveness separately.
- Then evaluate latency, throughput, power, and maintainability.
