# 72 Linux Futex and Condvar Internals

## Chapter map

- [[Futex_Word|01. Futex Word]]
- [[Hash_Buckets|02. Hash Buckets]]
- [[Waiters|03. Waiters]]
- [[Wakeups|04. Wakeups]]
- [[Requeue|05. Requeue]]
- [[Priority_Inheritance|06. Priority Inheritance]]
- [[Robust_Lists|07. Robust Lists]]
- [[Pthread_Condvars|08. Pthread Condvars]]
- [[Memory_Ordering|09. Memory Ordering]]
- [[Thundering_Herd|10. Thundering Herd]]
- [[Tracing|11. Tracing]]
- [[Troubleshooting|12. Troubleshooting]]

## Chapter purpose
This chapter builds a reusable mental model for **Linux Futex and Condvar Internals**, with emphasis on correctness, timing, memory ordering, lifecycle, debugging, and embedded-system consequences.

## Cross-chapter reasoning
- Start with state ownership.
- Identify execution contexts and possible interleavings.
- State the synchronization edge or ownership transfer.
- Prove safety and liveness separately.
- Then evaluate latency, throughput, power, and maintainability.
