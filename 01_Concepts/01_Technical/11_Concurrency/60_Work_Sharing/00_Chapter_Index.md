# 60 Work Sharing

## Chapter map

- [[Static_Partitioning|01. Static Partitioning]]
- [[Dynamic_Partitioning|02. Dynamic Partitioning]]
- [[Chunking|03. Chunking]]
- [[Load_Imbalance|04. Load Imbalance]]
- [[Scheduling_Overhead|05. Scheduling Overhead]]
- [[Affinity|06. Affinity]]
- [[NUMA|07. NUMA]]
- [[Work_Queues|08. Work Queues]]
- [[Bounded_Workers|09. Bounded Workers]]
- [[Priority|10. Priority]]
- [[Cancellation|11. Cancellation]]
- [[Performance|12. Performance]]

## Chapter purpose
This chapter builds a reusable mental model for **Work Sharing**, with emphasis on correctness, timing, memory ordering, lifecycle, debugging, and embedded-system consequences.

## Cross-chapter reasoning
- Start with state ownership.
- Identify execution contexts and possible interleavings.
- State the synchronization edge or ownership transfer.
- Prove safety and liveness separately.
- Then evaluate latency, throughput, power, and maintainability.
