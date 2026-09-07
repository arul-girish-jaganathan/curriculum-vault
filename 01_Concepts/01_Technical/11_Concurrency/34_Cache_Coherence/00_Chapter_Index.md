# 34 Cache Coherence

## Chapter map

- [[Coherence_Goal|01. Coherence Goal]]
- [[MESI_Family|02. MESI Family]]
- [[Invalidation|03. Invalidation]]
- [[Update_Protocols|04. Update Protocols]]
- [[Shared_vs_Modified|05. Shared vs Modified]]
- [[Cache_Line_Ownership|06. Cache Line Ownership]]
- [[Snoop_Traffic|07. Snoop Traffic]]
- [[Directory_Protocols|08. Directory Protocols]]
- [[Multicore_Effects|09. Multicore Effects]]
- [[DMA_Coherency|10. DMA Coherency]]
- [[Coherence_vs_Consistency|11. Coherence vs Consistency]]
- [[Performance_Implications|12. Performance Implications]]

## Chapter purpose
This chapter builds a reusable mental model for **Cache Coherence**, with emphasis on correctness, timing, memory ordering, lifecycle, debugging, and embedded-system consequences.

## Cross-chapter reasoning
- Start with state ownership.
- Identify execution contexts and possible interleavings.
- State the synchronization edge or ownership transfer.
- Prove safety and liveness separately.
- Then evaluate latency, throughput, power, and maintainability.
