# 69 C++ Parallel Algorithms

## Chapter map

- [[Execution_Policies|01. Execution Policies]]
- [[seq|02. seq]]
- [[par|03. par]]
- [[par_unseq|04. par_unseq]]
- [[Iterator_Safety|05. Iterator Safety]]
- [[Side_Effects|06. Side Effects]]
- [[Reduction|07. Reduction]]
- [[Transform_Reduce|08. Transform Reduce]]
- [[Exceptions|09. Exceptions]]
- [[Vectorization|10. Vectorization]]
- [[Thread_Pools|11. Thread Pools]]
- [[Embedded_Limits|12. Embedded Limits]]

## Chapter purpose
This chapter builds a reusable mental model for **C++ Parallel Algorithms**, with emphasis on correctness, timing, memory ordering, lifecycle, debugging, and embedded-system consequences.

## Cross-chapter reasoning
- Start with state ownership.
- Identify execution contexts and possible interleavings.
- State the synchronization edge or ownership transfer.
- Prove safety and liveness separately.
- Then evaluate latency, throughput, power, and maintainability.
