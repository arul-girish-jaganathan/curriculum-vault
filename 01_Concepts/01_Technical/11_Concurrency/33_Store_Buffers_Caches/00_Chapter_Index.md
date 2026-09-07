# 33 Store Buffers and Caches

## Chapter map

- [[Store_Buffer|01. Store Buffer]]
- [[Invalidate_Queue|02. Invalidate Queue]]
- [[Load_Delay|03. Load Delay]]
- [[Cache_Hit|04. Cache Hit]]
- [[Cache_Miss|05. Cache Miss]]
- [[Coherence_Traffic|06. Coherence Traffic]]
- [[Visibility_Delays|07. Visibility Delays]]
- [[Store_to_Load_Forwarding|08. Store-to-Load Forwarding]]
- [[Fence_Effects|09. Fence Effects]]
- [[False_Sharing|10. False Sharing]]
- [[Performance_Counters|11. Performance Counters]]
- [[Concurrency_Consequences|12. Concurrency Consequences]]

## Chapter purpose
This chapter builds a reusable mental model for **Store Buffers and Caches**, with emphasis on correctness, timing, memory ordering, lifecycle, debugging, and embedded-system consequences.

## Cross-chapter reasoning
- Start with state ownership.
- Identify execution contexts and possible interleavings.
- State the synchronization edge or ownership transfer.
- Prove safety and liveness separately.
- Then evaluate latency, throughput, power, and maintainability.
