# 63 Futures and Promises

## Chapter map

- [[Future_State|01. Future State]]
- [[Promise_Ownership|02. Promise Ownership]]
- [[Value_Publication|03. Value Publication]]
- [[Exception_Propagation|04. Exception Propagation]]
- [[Waiting|05. Waiting]]
- [[Polling|06. Polling]]
- [[Continuation|07. Continuation]]
- [[Timeout|08. Timeout]]
- [[Cancellation|09. Cancellation]]
- [[Broken_Promise|10. Broken Promise]]
- [[Shared_Future|11. Shared Future]]
- [[Embedded_Trade_offs|12. Embedded Trade-offs]]

## Chapter purpose
This chapter builds a reusable mental model for **Futures and Promises**, with emphasis on correctness, timing, memory ordering, lifecycle, debugging, and embedded-system consequences.

## Cross-chapter reasoning
- Start with state ownership.
- Identify execution contexts and possible interleavings.
- State the synchronization edge or ownership transfer.
- Prove safety and liveness separately.
- Then evaluate latency, throughput, power, and maintainability.
