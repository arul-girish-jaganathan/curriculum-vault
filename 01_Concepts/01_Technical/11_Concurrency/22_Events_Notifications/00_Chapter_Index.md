# 22 Events and Notifications

## Chapter map

- [[Event_Flags|01. Event Flags]]
- [[One_Shot_Events|02. One-Shot Events]]
- [[Level_Triggered_Events|03. Level-Triggered Events]]
- [[Edge_Triggered_Events|04. Edge-Triggered Events]]
- [[Task_Notifications|05. Task Notifications]]
- [[Notification_Consumption|06. Notification Consumption]]
- [[Coalescing|07. Coalescing]]
- [[Wakeup_Semantics|08. Wakeup Semantics]]
- [[ISR_Signaling|09. ISR Signaling]]
- [[Lost_Events|10. Lost Events]]
- [[Event_Ownership|11. Event Ownership]]
- [[Review|12. Review]]

## Chapter purpose
This chapter builds a reusable mental model for **Events and Notifications**, with emphasis on correctness, timing, memory ordering, lifecycle, debugging, and embedded-system consequences.

## Cross-chapter reasoning
- Start with state ownership.
- Identify execution contexts and possible interleavings.
- State the synchronization edge or ownership transfer.
- Prove safety and liveness separately.
- Then evaluate latency, throughput, power, and maintainability.
