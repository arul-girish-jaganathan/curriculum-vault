# 83 SMP AMP and Multicore Concurrency

## Chapter map

- [[SMP|01. SMP]]
- [[AMP|02. AMP]]
- [[CPU_Affinity|03. CPU Affinity]]
- [[Intercore_Interrupts|04. Intercore Interrupts]]
- [[Shared_Memory|05. Shared Memory]]
- [[Cache_Coherency|06. Cache Coherency]]
- [[Lock_Sharing|07. Lock Sharing]]
- [[Per_Core_Data|08. Per-Core Data]]
- [[Message_Passing|09. Message Passing]]
- [[Startup_Barriers|10. Startup Barriers]]
- [[Failure_Isolation|11. Failure Isolation]]
- [[Architecture_Choice|12. Architecture Choice]]

## Chapter purpose
This chapter builds a reusable mental model for **SMP AMP and Multicore Concurrency**, with emphasis on correctness, timing, memory ordering, lifecycle, debugging, and embedded-system consequences.

## Cross-chapter reasoning
- Start with state ownership.
- Identify execution contexts and possible interleavings.
- State the synchronization edge or ownership transfer.
- Prove safety and liveness separately.
- Then evaluate latency, throughput, power, and maintainability.
