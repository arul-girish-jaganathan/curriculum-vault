# 03 Parallelism vs Concurrency

## Chapter map

- [[Concurrency_Without_Parallelism|01. Concurrency Without Parallelism]]
- [[True_Parallel_Execution|02. True Parallel Execution]]
- [[Instruction_Level_Parallelism|03. Instruction-Level Parallelism]]
- [[Task_Level_Parallelism|04. Task-Level Parallelism]]
- [[CPU_Topology|05. CPU Topology]]
- [[Core_Affinity|06. Core Affinity]]
- [[Scalability|07. Scalability]]
- [[Amdahl_s_Law|08. Amdahl’s Law]]
- [[Throughput_vs_Latency|09. Throughput vs Latency]]
- [[Contention_Effects|10. Contention Effects]]
- [[Oversubscription|11. Oversubscription]]
- [[Embedded_Consequences|12. Embedded Consequences]]

## Chapter purpose
This chapter builds a reusable mental model for **Parallelism vs Concurrency**, with emphasis on correctness, timing, memory ordering, lifecycle, debugging, and embedded-system consequences.

## Cross-chapter reasoning
- Start with state ownership.
- Identify execution contexts and possible interleavings.
- State the synchronization edge or ownership transfer.
- Prove safety and liveness separately.
- Then evaluate latency, throughput, power, and maintainability.
