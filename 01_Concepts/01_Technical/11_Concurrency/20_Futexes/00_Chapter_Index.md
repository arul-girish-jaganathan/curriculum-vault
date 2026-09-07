# 20 Futexes

## Chapter map

- [[Futex_Concept|01. Futex Concept]]
- [[Fast_User_Space_Path|02. Fast User Space Path]]
- [[Kernel_Slow_Path|03. Kernel Slow Path]]
- [[Wait_Queues|04. Wait Queues]]
- [[FUTEX_WAIT|05. FUTEX_WAIT]]
- [[FUTEX_WAKE|06. FUTEX_WAKE]]
- [[Private_Futexes|07. Private Futexes]]
- [[PI_Futexes|08. PI Futexes]]
- [[Robustness|09. Robustness]]
- [[Spurious_Wakeups|10. Spurious Wakeups]]
- [[Pthreads_Mapping|11. Pthreads Mapping]]
- [[Debugging_Futexes|12. Debugging Futexes]]

## Chapter purpose
This chapter builds a reusable mental model for **Futexes**, with emphasis on correctness, timing, memory ordering, lifecycle, debugging, and embedded-system consequences.

## Cross-chapter reasoning
- Start with state ownership.
- Identify execution contexts and possible interleavings.
- State the synchronization edge or ownership transfer.
- Prove safety and liveness separately.
- Then evaluate latency, throughput, power, and maintainability.
