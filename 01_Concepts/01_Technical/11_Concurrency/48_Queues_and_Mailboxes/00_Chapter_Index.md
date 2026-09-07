# 48 Queues and Mailboxes

## Chapter map

- [[FIFO_Semantics|01. FIFO Semantics]]
- [[Bounded_Queue|02. Bounded Queue]]
- [[Mailbox_Slot|03. Mailbox Slot]]
- [[Priority_Queue|04. Priority Queue]]
- [[Copy_vs_Reference|05. Copy vs Reference]]
- [[Ownership_Transfer|06. Ownership Transfer]]
- [[Blocking_API|07. Blocking API]]
- [[Timeout|08. Timeout]]
- [[ISR_Use|09. ISR Use]]
- [[Backpressure|10. Backpressure]]
- [[Queue_Depth|11. Queue Depth]]
- [[Failure_Handling|12. Failure Handling]]

## Chapter purpose
This chapter builds a reusable mental model for **Queues and Mailboxes**, with emphasis on correctness, timing, memory ordering, lifecycle, debugging, and embedded-system consequences.

## Cross-chapter reasoning
- Start with state ownership.
- Identify execution contexts and possible interleavings.
- State the synchronization edge or ownership transfer.
- Prove safety and liveness separately.
- Then evaluate latency, throughput, power, and maintainability.
