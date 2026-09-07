# 50 Shared Memory IPC

## Chapter map

- [[Shared_Mapping|01. Shared Mapping]]
- [[Synchronization|02. Synchronization]]
- [[Memory_Visibility|03. Memory Visibility]]
- [[Ownership_Protocol|04. Ownership Protocol]]
- [[Double_Buffering|05. Double Buffering]]
- [[Ring_Buffers|06. Ring Buffers]]
- [[Futex_Synchronization|07. Futex Synchronization]]
- [[Cross_Process_Lifetime|08. Cross-Process Lifetime]]
- [[Crash_Recovery|09. Crash Recovery]]
- [[Security|10. Security]]
- [[NUMA|11. NUMA]]
- [[Design_Review|12. Design Review]]

## Chapter purpose
This chapter builds a reusable mental model for **Shared Memory IPC**, with emphasis on correctness, timing, memory ordering, lifecycle, debugging, and embedded-system consequences.

## Cross-chapter reasoning
- Start with state ownership.
- Identify execution contexts and possible interleavings.
- State the synchronization edge or ownership transfer.
- Prove safety and liveness separately.
- Then evaluate latency, throughput, power, and maintainability.
