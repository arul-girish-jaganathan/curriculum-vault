# 55 Livelock and Progress

## Chapter map

- [[Livelock|01. Livelock]]
- [[Busy_Retry|02. Busy Retry]]
- [[Collision_Avoidance|03. Collision Avoidance]]
- [[CAS_Storms|04. CAS Storms]]
- [[Backoff|05. Backoff]]
- [[Randomized_Backoff|06. Randomized Backoff]]
- [[Progress_Conditions|07. Progress Conditions]]
- [[Lock_Free_vs_Wait_Free|08. Lock-Free vs Wait-Free]]
- [[Deadlock_Comparison|09. Deadlock Comparison]]
- [[Detection|10. Detection]]
- [[Mitigation|11. Mitigation]]
- [[Review|12. Review]]

## Chapter purpose
This chapter builds a reusable mental model for **Livelock and Progress**, with emphasis on correctness, timing, memory ordering, lifecycle, debugging, and embedded-system consequences.

## Cross-chapter reasoning
- Start with state ownership.
- Identify execution contexts and possible interleavings.
- State the synchronization edge or ownership transfer.
- Prove safety and liveness separately.
- Then evaluate latency, throughput, power, and maintainability.
