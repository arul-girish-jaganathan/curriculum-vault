# 46 Producer Consumer

## Chapter map

- [[Bounded_Buffer|01. Bounded Buffer]]
- [[Unbounded_Queue|02. Unbounded Queue]]
- [[Blocking_Producer|03. Blocking Producer]]
- [[Blocking_Consumer|04. Blocking Consumer]]
- [[Backpressure|05. Backpressure]]
- [[Full_Buffer|06. Full Buffer]]
- [[Empty_Buffer|07. Empty Buffer]]
- [[Semaphore_Counting|08. Semaphore Counting]]
- [[Condition_Variable|09. Condition Variable]]
- [[Ring_Buffer|10. Ring Buffer]]
- [[Priority_Effects|11. Priority Effects]]
- [[Embedded_Design|12. Embedded Design]]

## Chapter purpose
This chapter builds a reusable mental model for **Producer Consumer**, with emphasis on correctness, timing, memory ordering, lifecycle, debugging, and embedded-system consequences.

## Cross-chapter reasoning
- Start with state ownership.
- Identify execution contexts and possible interleavings.
- State the synchronization edge or ownership transfer.
- Prove safety and liveness separately.
- Then evaluate latency, throughput, power, and maintainability.
