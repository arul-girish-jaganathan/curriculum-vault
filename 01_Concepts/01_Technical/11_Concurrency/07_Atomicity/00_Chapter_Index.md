# 07 Atomicity

## Chapter map

- [[Atomic_Operation_Meaning|01. Atomic Operation Meaning]]
- [[Atomic_Read|02. Atomic Read]]
- [[Atomic_Write|03. Atomic Write]]
- [[Atomic_RMW|04. Atomic RMW]]
- [[Multi_Field_Atomicity|05. Multi-Field Atomicity]]
- [[Critical_Sections|06. Critical Sections]]
- [[Transactional_Thinking|07. Transactional Thinking]]
- [[Atomicity_vs_Visibility|08. Atomicity vs Visibility]]
- [[Atomicity_vs_Ordering|09. Atomicity vs Ordering]]
- [[Interrupt_Atomicity|10. Interrupt Atomicity]]
- [[Hardware_Atomic_Width|11. Hardware Atomic Width]]
- [[Atomicity_Review|12. Atomicity Review]]

## Chapter purpose
This chapter builds a reusable mental model for **Atomicity**, with emphasis on correctness, timing, memory ordering, lifecycle, debugging, and embedded-system consequences.

## Cross-chapter reasoning
- Start with state ownership.
- Identify execution contexts and possible interleavings.
- State the synchronization edge or ownership transfer.
- Prove safety and liveness separately.
- Then evaluate latency, throughput, power, and maintainability.
