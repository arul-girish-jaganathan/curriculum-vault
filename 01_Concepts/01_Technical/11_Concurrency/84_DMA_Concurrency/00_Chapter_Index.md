# 84 DMA and Concurrency

## Chapter map

- [[DMA_Ownership|01. DMA Ownership]]
- [[CPU_vs_Device_Ownership|02. CPU vs Device Ownership]]
- [[Descriptor_Rings|03. Descriptor Rings]]
- [[Cache_Maintenance|04. Cache Maintenance]]
- [[Memory_Barriers|05. Memory Barriers]]
- [[Completion_Interrupt|06. Completion Interrupt]]
- [[Double_Buffering|07. Double Buffering]]
- [[DMA_API_Synchronization|08. DMA API Synchronization]]
- [[IOMMU|09. IOMMU]]
- [[Teardown|10. Teardown]]
- [[Race_Patterns|11. Race Patterns]]
- [[Review|12. Review]]

## Chapter purpose
This chapter builds a reusable mental model for **DMA and Concurrency**, with emphasis on correctness, timing, memory ordering, lifecycle, debugging, and embedded-system consequences.

## Cross-chapter reasoning
- Start with state ownership.
- Identify execution contexts and possible interleavings.
- State the synchronization edge or ownership transfer.
- Prove safety and liveness separately.
- Then evaluate latency, throughput, power, and maintainability.
