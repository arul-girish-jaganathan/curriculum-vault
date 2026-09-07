# 53 Deadlocks

## Chapter map

- [[Necessary_Conditions|01. Necessary Conditions]]
- [[Wait_For_Graph|02. Wait-For Graph]]
- [[Mutual_Exclusion|03. Mutual Exclusion]]
- [[Hold_and_Wait|04. Hold and Wait]]
- [[No_Preemption|05. No Preemption]]
- [[Circular_Wait|06. Circular Wait]]
- [[ABBA|07. ABBA]]
- [[Self_Deadlock|08. Self Deadlock]]
- [[Lock_Callback|09. Lock + Callback]]
- [[I_O_While_Locked|10. I/O While Locked]]
- [[Detection|11. Detection]]
- [[Recovery|12. Recovery]]

## Chapter purpose
This chapter builds a reusable mental model for **Deadlocks**, with emphasis on correctness, timing, memory ordering, lifecycle, debugging, and embedded-system consequences.

## Cross-chapter reasoning
- Start with state ownership.
- Identify execution contexts and possible interleavings.
- State the synchronization edge or ownership transfer.
- Prove safety and liveness separately.
- Then evaluate latency, throughput, power, and maintainability.
