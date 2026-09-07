# 85 MMIO and Device Concurrency

## Chapter map

- [[MMIO_Ordering|01. MMIO Ordering]]
- [[Register_Races|02. Register Races]]
- [[Read_Modify_Write|03. Read Modify Write]]
- [[Shadow_Registers|04. Shadow Registers]]
- [[Volatile_vs_Barriers|05. Volatile vs Barriers]]
- [[Interrupt_Registers|06. Interrupt Registers]]
- [[Status_Acknowledge|07. Status Acknowledge]]
- [[Polling_vs_Interrupt|08. Polling vs Interrupt]]
- [[Multi_Core_Device_Access|09. Multi-Core Device Access]]
- [[Power_State_Races|10. Power State Races]]
- [[Register_Ownership|11. Register Ownership]]
- [[Driver_Review|12. Driver Review]]

## Chapter purpose
This chapter builds a reusable mental model for **MMIO and Device Concurrency**, with emphasis on correctness, timing, memory ordering, lifecycle, debugging, and embedded-system consequences.

## Cross-chapter reasoning
- Start with state ownership.
- Identify execution contexts and possible interleavings.
- State the synchronization edge or ownership transfer.
- Prove safety and liveness separately.
- Then evaluate latency, throughput, power, and maintainability.
