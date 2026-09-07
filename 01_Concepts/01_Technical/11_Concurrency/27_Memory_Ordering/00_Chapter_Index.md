# 27 Memory Ordering

## Chapter map

- [[Relaxed|01. Relaxed]]
- [[Acquire|02. Acquire]]
- [[Release|03. Release]]
- [[Acq_Rel|04. Acq Rel]]
- [[Seq_Cst|05. Seq Cst]]
- [[Consume_Concept|06. Consume Concept]]
- [[Fence_Orders|07. Fence Orders]]
- [[Failure_Order|08. Failure Order]]
- [[Operation_Order|09. Operation Order]]
- [[Formal_Reasoning|10. Formal Reasoning]]
- [[Performance_Trade_offs|11. Performance Trade-offs]]
- [[Choosing_the_Weakest_Correct_Order|12. Choosing the Weakest Correct Order]]

## Chapter purpose
This chapter builds a reusable mental model for **Memory Ordering**, with emphasis on correctness, timing, memory ordering, lifecycle, debugging, and embedded-system consequences.

## Cross-chapter reasoning
- Start with state ownership.
- Identify execution contexts and possible interleavings.
- State the synchronization edge or ownership transfer.
- Prove safety and liveness separately.
- Then evaluate latency, throughput, power, and maintainability.
