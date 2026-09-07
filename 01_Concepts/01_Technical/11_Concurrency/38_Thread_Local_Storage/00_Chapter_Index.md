# 38 Thread Local Storage

## Chapter map

- [[TLS_Concept|01. TLS Concept]]
- [[pthread_TLS|02. pthread TLS]]
- [[C_thread_local|03. C++ thread_local]]
- [[RTOS_TLS|04. RTOS TLS]]
- [[Destructor_Semantics|05. Destructor Semantics]]
- [[Per_Thread_Caches|06. Per-Thread Caches]]
- [[Error_Context|07. Error Context]]
- [[Logging_Context|08. Logging Context]]
- [[TLS_Footprint|09. TLS Footprint]]
- [[TLS_Initialization|10. TLS Initialization]]
- [[TLS_Teardown|11. TLS Teardown]]
- [[When_TLS_Is_Appropriate|12. When TLS Is Appropriate]]

## Chapter purpose
This chapter builds a reusable mental model for **Thread Local Storage**, with emphasis on correctness, timing, memory ordering, lifecycle, debugging, and embedded-system consequences.

## Cross-chapter reasoning
- Start with state ownership.
- Identify execution contexts and possible interleavings.
- State the synchronization edge or ownership transfer.
- Prove safety and liveness separately.
- Then evaluate latency, throughput, power, and maintainability.
