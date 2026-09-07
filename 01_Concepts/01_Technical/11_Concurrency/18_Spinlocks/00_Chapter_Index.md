# 18 Spinlocks

## Chapter map

- [[Spin_Waiting|01. Spin Waiting]]
- [[CPU_Cost|02. CPU Cost]]
- [[Preemption_Constraints|03. Preemption Constraints]]
- [[IRQ_Context|04. IRQ Context]]
- [[Raw_Spinlocks|05. Raw Spinlocks]]
- [[Nested_Spinlocks|06. Nested Spinlocks]]
- [[Contention|07. Contention]]
- [[Lock_Hold_Time|08. Lock Hold Time]]
- [[NUMA_and_Cache_Effects|09. NUMA and Cache Effects]]
- [[Sleep_vs_Spin|10. Sleep vs Spin]]
- [[RTOS_Spinlocks|11. RTOS Spinlocks]]
- [[Choosing_Spinlocks|12. Choosing Spinlocks]]

## Chapter purpose
This chapter builds a reusable mental model for **Spinlocks**, with emphasis on correctness, timing, memory ordering, lifecycle, debugging, and embedded-system consequences.

## Cross-chapter reasoning
- Start with state ownership.
- Identify execution contexts and possible interleavings.
- State the synchronization edge or ownership transfer.
- Prove safety and liveness separately.
- Then evaluate latency, throughput, power, and maintainability.
