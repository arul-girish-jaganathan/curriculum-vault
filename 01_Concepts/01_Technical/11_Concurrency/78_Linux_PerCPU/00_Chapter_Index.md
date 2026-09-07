# 78 Linux PerCPU and Locality

## Chapter map

- [[PerCPU_Variables|01. PerCPU Variables]]
- [[get_cpu|02. get_cpu]]
- [[preemption|03. preemption]]
- [[this_cpu_Operations|04. this_cpu Operations]]
- [[PerCPU_Counters|05. PerCPU Counters]]
- [[PerCPU_State|06. PerCPU State]]
- [[Migration|07. Migration]]
- [[Interrupt_Context|08. Interrupt Context]]
- [[Cache_Locality|09. Cache Locality]]
- [[Lock_Elision|10. Lock Elision]]
- [[NUMA|11. NUMA]]
- [[Trade_offs|12. Trade-offs]]

## Chapter purpose
This chapter builds a reusable mental model for **Linux PerCPU and Locality**, with emphasis on correctness, timing, memory ordering, lifecycle, debugging, and embedded-system consequences.

## Cross-chapter reasoning
- Start with state ownership.
- Identify execution contexts and possible interleavings.
- State the synchronization edge or ownership transfer.
- Prove safety and liveness separately.
- Then evaluate latency, throughput, power, and maintainability.
