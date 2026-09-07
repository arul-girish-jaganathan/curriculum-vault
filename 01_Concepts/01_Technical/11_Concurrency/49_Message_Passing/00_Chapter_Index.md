# 49 Message Passing

## Chapter map

- [[Message_Ownership|01. Message Ownership]]
- [[Copying|02. Copying]]
- [[Pointers_in_Messages|03. Pointers in Messages]]
- [[Serialization|04. Serialization]]
- [[Mailbox|05. Mailbox]]
- [[Pipes|06. Pipes]]
- [[IPC_Queues|07. IPC Queues]]
- [[Zero_Copy|08. Zero Copy]]
- [[Backpressure|09. Backpressure]]
- [[Ordering|10. Ordering]]
- [[Priority|11. Priority]]
- [[Security|12. Security]]

## Chapter purpose
This chapter builds a reusable mental model for **Message Passing**, with emphasis on correctness, timing, memory ordering, lifecycle, debugging, and embedded-system consequences.

## Cross-chapter reasoning
- Start with state ownership.
- Identify execution contexts and possible interleavings.
- State the synchronization edge or ownership transfer.
- Prove safety and liveness separately.
- Then evaluate latency, throughput, power, and maintainability.
