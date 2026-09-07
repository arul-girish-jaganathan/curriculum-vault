# 77 Linux Workqueues

## Chapter map

- [[Work_Struct|01. Work Struct]]
- [[Worker_Pool|02. Worker Pool]]
- [[Bounded_Workers|03. Bounded Workers]]
- [[Ordered_Workqueue|04. Ordered Workqueue]]
- [[Delayed_Work|05. Delayed Work]]
- [[Flush|06. Flush]]
- [[Cancel|07. Cancel]]
- [[CPU_Affinity|08. CPU Affinity]]
- [[Power_Efficient_Workqueues|09. Power Efficient Workqueues]]
- [[Concurrency_Limits|10. Concurrency Limits]]
- [[Teardown|11. Teardown]]
- [[Driver_Patterns|12. Driver Patterns]]

## Chapter purpose
This chapter builds a reusable mental model for **Linux Workqueues**, with emphasis on correctness, timing, memory ordering, lifecycle, debugging, and embedded-system consequences.

## Cross-chapter reasoning
- Start with state ownership.
- Identify execution contexts and possible interleavings.
- State the synchronization edge or ownership transfer.
- Prove safety and liveness separately.
- Then evaluate latency, throughput, power, and maintainability.
