# 51 Lock Granularity

## Chapter map

- [[Coarse_Locks|01. Coarse Locks]]
- [[Fine_Grained_Locks|02. Fine-Grained Locks]]
- [[Lock_Contention|03. Lock Contention]]
- [[Critical_Section_Size|04. Critical Section Size]]
- [[Data_Partitioning|05. Data Partitioning]]
- [[Per_Object_Locks|06. Per-Object Locks]]
- [[Per_Bucket_Locks|07. Per-Bucket Locks]]
- [[Lock_Striping|08. Lock Striping]]
- [[Cache_Locality|09. Cache Locality]]
- [[Deadlock_Complexity|10. Deadlock Complexity]]
- [[Scalability|11. Scalability]]
- [[Selection_Heuristics|12. Selection Heuristics]]

## Chapter purpose
This chapter builds a reusable mental model for **Lock Granularity**, with emphasis on correctness, timing, memory ordering, lifecycle, debugging, and embedded-system consequences.

## Cross-chapter reasoning
- Start with state ownership.
- Identify execution contexts and possible interleavings.
- State the synchronization edge or ownership transfer.
- Prove safety and liveness separately.
- Then evaluate latency, throughput, power, and maintainability.
