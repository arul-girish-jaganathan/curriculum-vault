# 62 Work Stealing

## Chapter map

- [[Deque_Model|01. Deque Model]]
- [[Owner_Push_Pop|02. Owner Push Pop]]
- [[Thief_Steal|03. Thief Steal]]
- [[Concurrent_Deque|04. Concurrent Deque]]
- [[Load_Balancing|05. Load Balancing]]
- [[Locality|06. Locality]]
- [[False_Sharing|07. False Sharing]]
- [[Idle_Workers|08. Idle Workers]]
- [[ABA_Reclamation|09. ABA/Reclamation]]
- [[NUMA|10. NUMA]]
- [[Latency|11. Latency]]
- [[Use_Cases|12. Use Cases]]

## Chapter purpose
This chapter builds a reusable mental model for **Work Stealing**, with emphasis on correctness, timing, memory ordering, lifecycle, debugging, and embedded-system consequences.

## Cross-chapter reasoning
- Start with state ownership.
- Identify execution contexts and possible interleavings.
- State the synchronization edge or ownership transfer.
- Prove safety and liveness separately.
- Then evaluate latency, throughput, power, and maintainability.
