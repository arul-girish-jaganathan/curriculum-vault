# 23 Barriers Latches and Once

## Chapter map

- [[Barrier_Semantics|01. Barrier Semantics]]
- [[Reusable_Barriers|02. Reusable Barriers]]
- [[One_Time_Barriers|03. One-Time Barriers]]
- [[Latch_Semantics|04. Latch Semantics]]
- [[Countdown_Coordination|05. Countdown Coordination]]
- [[std_barrier|06. std::barrier]]
- [[std_latch|07. std::latch]]
- [[call_once|08. call_once]]
- [[Initialization_Once|09. Initialization Once]]
- [[Phase_Completion|10. Phase Completion]]
- [[Deadlock_Hazards|11. Deadlock Hazards]]
- [[Use_Cases|12. Use Cases]]

## Chapter purpose
This chapter builds a reusable mental model for **Barriers Latches and Once**, with emphasis on correctness, timing, memory ordering, lifecycle, debugging, and embedded-system consequences.

## Cross-chapter reasoning
- Start with state ownership.
- Identify execution contexts and possible interleavings.
- State the synchronization edge or ownership transfer.
- Prove safety and liveness separately.
- Then evaluate latency, throughput, power, and maintainability.
