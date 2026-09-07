# 15 Lock-Free vs Locked

## Chapter map

- [[Terminology|01. Terminology]]
- [[Lock_Free_Property|02. Lock-Free Property]]
- [[Wait_Free_Property|03. Wait-Free Property]]
- [[Obstruction_Free|04. Obstruction-Free]]
- [[Mutex_Based_Design|05. Mutex-Based Design]]
- [[CAS_Loops|06. CAS Loops]]
- [[Retry_Costs|07. Retry Costs]]
- [[Progress_Under_Contention|08. Progress Under Contention]]
- [[Memory_Reclamation|09. Memory Reclamation]]
- [[ABA|10. ABA]]
- [[When_Lock_Free_Hurts|11. When Lock-Free Hurts]]
- [[Selection_Guide|12. Selection Guide]]

## Chapter purpose
This chapter builds a reusable mental model for **Lock-Free vs Locked**, with emphasis on correctness, timing, memory ordering, lifecycle, debugging, and embedded-system consequences.

## Cross-chapter reasoning
- Start with state ownership.
- Identify execution contexts and possible interleavings.
- State the synchronization edge or ownership transfer.
- Prove safety and liveness separately.
- Then evaluate latency, throughput, power, and maintainability.
