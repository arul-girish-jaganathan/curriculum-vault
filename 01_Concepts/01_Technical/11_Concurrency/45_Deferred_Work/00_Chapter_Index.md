# 45 Deferred Work

## Chapter map

- [[Why_Defer|01. Why Defer]]
- [[Bottom_Halves|02. Bottom Halves]]
- [[Tasklets|03. Tasklets]]
- [[Workqueues|04. Workqueues]]
- [[Worker_Threads|05. Worker Threads]]
- [[DPC_Analogy|06. DPC Analogy]]
- [[RTOS_Deferred_Work|07. RTOS Deferred Work]]
- [[Latency|08. Latency]]
- [[Context_Constraints|09. Context Constraints]]
- [[Coalescing|10. Coalescing]]
- [[Cancellation|11. Cancellation]]
- [[Shutdown|12. Shutdown]]

## Chapter purpose
This chapter builds a reusable mental model for **Deferred Work**, with emphasis on correctness, timing, memory ordering, lifecycle, debugging, and embedded-system consequences.

## Cross-chapter reasoning
- Start with state ownership.
- Identify execution contexts and possible interleavings.
- State the synchronization edge or ownership transfer.
- Prove safety and liveness separately.
- Then evaluate latency, throughput, power, and maintainability.
