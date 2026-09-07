# 30 Sequential Consistency

## Chapter map

- [[SC_Intuition|01. SC Intuition]]
- [[Total_Order|02. Total Order]]
- [[SC_Atomics|03. SC Atomics]]
- [[SC_vs_Weak_Orders|04. SC vs Weak Orders]]
- [[SC_DRF|05. SC-DRF]]
- [[Global_Ordering|06. Global Ordering]]
- [[Litmus_Example|07. Litmus Example]]
- [[Performance_Cost|08. Performance Cost]]
- [[Debugging_Value|09. Debugging Value]]
- [[Hybrid_Ordering|10. Hybrid Ordering]]
- [[When_SC_Is_Best|11. When SC Is Best]]
- [[When_SC_Is_Overkill|12. When SC Is Overkill]]

## Chapter purpose
This chapter builds a reusable mental model for **Sequential Consistency**, with emphasis on correctness, timing, memory ordering, lifecycle, debugging, and embedded-system consequences.

## Cross-chapter reasoning
- Start with state ownership.
- Identify execution contexts and possible interleavings.
- State the synchronization edge or ownership transfer.
- Prove safety and liveness separately.
- Then evaluate latency, throughput, power, and maintainability.
