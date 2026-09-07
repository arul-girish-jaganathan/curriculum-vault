# 61 Task Pools

## Chapter map

- [[Worker_Threads|01. Worker Threads]]
- [[Queue_Ownership|02. Queue Ownership]]
- [[Worker_Lifecycle|03. Worker Lifecycle]]
- [[Pool_Sizing|04. Pool Sizing]]
- [[Idle_Workers|05. Idle Workers]]
- [[Shutdown|06. Shutdown]]
- [[Backpressure|07. Backpressure]]
- [[Priority|08. Priority]]
- [[Work_Stealing_Integration|09. Work Stealing Integration]]
- [[Memory_Footprint|10. Memory Footprint]]
- [[Failure_Isolation|11. Failure Isolation]]
- [[Metrics|12. Metrics]]

## Chapter purpose
This chapter builds a reusable mental model for **Task Pools**, with emphasis on correctness, timing, memory ordering, lifecycle, debugging, and embedded-system consequences.

## Cross-chapter reasoning
- Start with state ownership.
- Identify execution contexts and possible interleavings.
- State the synchronization edge or ownership transfer.
- Prove safety and liveness separately.
- Then evaluate latency, throughput, power, and maintainability.
