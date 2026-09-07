# 81 RTOS Locks and IPC

## Chapter map

- [[Mutex|01. Mutex]]
- [[Binary_Semaphore|02. Binary Semaphore]]
- [[Counting_Semaphore|03. Counting Semaphore]]
- [[Event_Flags|04. Event Flags]]
- [[Queues|05. Queues]]
- [[Mailboxes|06. Mailboxes]]
- [[Message_Buffers|07. Message Buffers]]
- [[Stream_Buffers|08. Stream Buffers]]
- [[Notifications|09. Notifications]]
- [[Critical_Sections|10. Critical Sections]]
- [[Priority_Inheritance|11. Priority Inheritance]]
- [[Shutdown|12. Shutdown]]

## Chapter purpose
This chapter builds a reusable mental model for **RTOS Locks and IPC**, with emphasis on correctness, timing, memory ordering, lifecycle, debugging, and embedded-system consequences.

## Cross-chapter reasoning
- Start with state ownership.
- Identify execution contexts and possible interleavings.
- State the synchronization edge or ownership transfer.
- Prove safety and liveness separately.
- Then evaluate latency, throughput, power, and maintainability.
