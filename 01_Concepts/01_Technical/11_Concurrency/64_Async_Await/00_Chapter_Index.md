# 64 Async Await

## Chapter map

- [[Coroutine_State|01. Coroutine State]]
- [[Suspension|02. Suspension]]
- [[Resumption|03. Resumption]]
- [[Executor|04. Executor]]
- [[Cancellation|05. Cancellation]]
- [[Lifetime|06. Lifetime]]
- [[Stackless_Model|07. Stackless Model]]
- [[Stackful_Comparison|08. Stackful Comparison]]
- [[I_O_Integration|09. I/O Integration]]
- [[Scheduling|10. Scheduling]]
- [[Backpressure|11. Backpressure]]
- [[Debugging|12. Debugging]]

## Chapter purpose
This chapter builds a reusable mental model for **Async Await**, with emphasis on correctness, timing, memory ordering, lifecycle, debugging, and embedded-system consequences.

## Cross-chapter reasoning
- Start with state ownership.
- Identify execution contexts and possible interleavings.
- State the synchronization edge or ownership transfer.
- Prove safety and liveness separately.
- Then evaluate latency, throughput, power, and maintainability.
