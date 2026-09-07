# 65 C++ Threads

## Chapter map

- [[std_thread|01. std::thread]]
- [[jthread|02. jthread]]
- [[Joinability|03. Joinability]]
- [[RAII_Thread_Ownership|04. RAII Thread Ownership]]
- [[Arguments|05. Arguments]]
- [[Thread_IDs|06. Thread IDs]]
- [[Native_Handles|07. Native Handles]]
- [[Stop_Tokens|08. Stop Tokens]]
- [[Thread_Naming|09. Thread Naming]]
- [[Thread_Lifetime|10. Thread Lifetime]]
- [[Exceptions|11. Exceptions]]
- [[Embedded_Caveats|12. Embedded Caveats]]

## Chapter purpose
This chapter builds a reusable mental model for **C++ Threads**, with emphasis on correctness, timing, memory ordering, lifecycle, debugging, and embedded-system consequences.

## Cross-chapter reasoning
- Start with state ownership.
- Identify execution contexts and possible interleavings.
- State the synchronization edge or ownership transfer.
- Prove safety and liveness separately.
- Then evaluate latency, throughput, power, and maintainability.
