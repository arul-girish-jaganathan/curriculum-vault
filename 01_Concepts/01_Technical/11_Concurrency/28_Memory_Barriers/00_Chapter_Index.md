# 28 Memory Barriers and Fences

## Chapter map

- [[Compiler_Barrier|01. Compiler Barrier]]
- [[CPU_Fence|02. CPU Fence]]
- [[Acquire_Fence|03. Acquire Fence]]
- [[Release_Fence|04. Release Fence]]
- [[Full_Fence|05. Full Fence]]
- [[DMA_Barriers|06. DMA Barriers]]
- [[MMIO_Barriers|07. MMIO Barriers]]
- [[Lock_Barriers|08. Lock Barriers]]
- [[Atomic_Fences|09. Atomic Fences]]
- [[Barrier_Placement|10. Barrier Placement]]
- [[Over_Barrierization|11. Over-Barrierization]]
- [[Under_Barrierization|12. Under-Barrierization]]

## Chapter purpose
This chapter builds a reusable mental model for **Memory Barriers and Fences**, with emphasis on correctness, timing, memory ordering, lifecycle, debugging, and embedded-system consequences.

## Cross-chapter reasoning
- Start with state ownership.
- Identify execution contexts and possible interleavings.
- State the synchronization edge or ownership transfer.
- Prove safety and liveness separately.
- Then evaluate latency, throughput, power, and maintainability.
