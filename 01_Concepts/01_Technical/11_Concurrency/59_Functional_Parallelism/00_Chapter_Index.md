# 59 Functional Parallelism

## Chapter map

- [[Pure_Functions|01. Pure Functions]]
- [[Map|02. Map]]
- [[Reduce|03. Reduce]]
- [[Fork_Join|04. Fork Join]]
- [[Pipeline|05. Pipeline]]
- [[Determinism|06. Determinism]]
- [[Data_Partitioning|07. Data Partitioning]]
- [[Reduction_Contention|08. Reduction Contention]]
- [[Scheduling|09. Scheduling]]
- [[Error_Propagation|10. Error Propagation]]
- [[Embedded_Use|11. Embedded Use]]
- [[Trade_offs|12. Trade-offs]]

## Chapter purpose
This chapter builds a reusable mental model for **Functional Parallelism**, with emphasis on correctness, timing, memory ordering, lifecycle, debugging, and embedded-system consequences.

## Cross-chapter reasoning
- Start with state ownership.
- Identify execution contexts and possible interleavings.
- State the synchronization edge or ownership transfer.
- Prove safety and liveness separately.
- Then evaluate latency, throughput, power, and maintainability.
