# 04 Execution Context and Ownership

## Chapter map

- [[Execution_Context|01. Execution Context]]
- [[Who_Owns_the_State|02. Who Owns the State]]
- [[Call_Stack_Ownership|03. Call Stack Ownership]]
- [[Heap_Object_Ownership|04. Heap Object Ownership]]
- [[Context_Migration|05. Context Migration]]
- [[Thread_Affinity|06. Thread Affinity]]
- [[Context_Capture|07. Context Capture]]
- [[Reentrant_Context|08. Reentrant Context]]
- [[Resource_Lifetime|09. Resource Lifetime]]
- [[Cancellation_Context|10. Cancellation Context]]
- [[Cross_Context_APIs|11. Cross-Context APIs]]
- [[Reviewing_Ownership|12. Reviewing Ownership]]

## Chapter purpose
This chapter builds a reusable mental model for **Execution Context and Ownership**, with emphasis on correctness, timing, memory ordering, lifecycle, debugging, and embedded-system consequences.

## Cross-chapter reasoning
- Start with state ownership.
- Identify execution contexts and possible interleavings.
- State the synchronization edge or ownership transfer.
- Prove safety and liveness separately.
- Then evaluate latency, throughput, power, and maintainability.
