# 75 Linux Seqlocks and Sequence Counters

## Chapter map

- [[Sequence_Counter|01. Sequence Counter]]
- [[Read_Retry|02. Read Retry]]
- [[Writer_Serialization|03. Writer Serialization]]
- [[Lockless_Reads|04. Lockless Reads]]
- [[Tearing|05. Tearing]]
- [[Pointer_Restrictions|06. Pointer Restrictions]]
- [[seqcount_t|07. seqcount_t]]
- [[seqlock_t|08. seqlock_t]]
- [[Latch_Variants|09. Latch Variants]]
- [[PREEMPT_RT_Considerations|10. PREEMPT_RT Considerations]]
- [[Use_Cases|11. Use Cases]]
- [[Review|12. Review]]

## Chapter purpose
This chapter builds a reusable mental model for **Linux Seqlocks and Sequence Counters**, with emphasis on correctness, timing, memory ordering, lifecycle, debugging, and embedded-system consequences.

## Cross-chapter reasoning
- Start with state ownership.
- Identify execution contexts and possible interleavings.
- State the synchronization edge or ownership transfer.
- Prove safety and liveness separately.
- Then evaluate latency, throughput, power, and maintainability.
