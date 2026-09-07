# 01 Concurrency Foundations

## Chapter map

- [[Definition_and_Mental_Model|01. Definition and Mental Model]]
- [[Safety_vs_Liveness|02. Safety vs Liveness]]
- [[Shared_State_and_Ownership|03. Shared State and Ownership]]
- [[Interleavings|04. Interleavings]]
- [[Atomicity|05. Atomicity]]
- [[Visibility|06. Visibility]]
- [[Ordering|07. Ordering]]
- [[Progress_Guarantees|08. Progress Guarantees]]
- [[Determinism|09. Determinism]]
- [[Concurrency_Boundaries|10. Concurrency Boundaries]]
- [[Typical_Failure_Modes|11. Typical Failure Modes]]
- [[Staff_Level_Review_Questions|12. Staff-Level Review Questions]]

## Chapter purpose
This chapter builds a reusable mental model for **Concurrency Foundations**, with emphasis on correctness, timing, memory ordering, lifecycle, debugging, and embedded-system consequences.

## Cross-chapter reasoning
- Start with state ownership.
- Identify execution contexts and possible interleavings.
- State the synchronization edge or ownership transfer.
- Prove safety and liveness separately.
- Then evaluate latency, throughput, power, and maintainability.
