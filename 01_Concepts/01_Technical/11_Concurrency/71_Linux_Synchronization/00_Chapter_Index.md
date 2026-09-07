# 71 Linux Synchronization Primitives

## Chapter map

- [[Mutex|01. Mutex]]
- [[Spinlock|02. Spinlock]]
- [[RW_Semaphore|03. RW Semaphore]]
- [[Semaphore|04. Semaphore]]
- [[Completion|05. Completion]]
- [[Wait_Queue|06. Wait Queue]]
- [[Atomic|07. Atomic]]
- [[PerCPU|08. PerCPU]]
- [[RCU|09. RCU]]
- [[Seqcount|10. Seqcount]]
- [[Completions_vs_Waitqueues|11. Completions vs Waitqueues]]
- [[Selection_Guide|12. Selection Guide]]

## Chapter purpose
This chapter builds a reusable mental model for **Linux Synchronization Primitives**, with emphasis on correctness, timing, memory ordering, lifecycle, debugging, and embedded-system consequences.

## Cross-chapter reasoning
- Start with state ownership.
- Identify execution contexts and possible interleavings.
- State the synchronization edge or ownership transfer.
- Prove safety and liveness separately.
- Then evaluate latency, throughput, power, and maintainability.
