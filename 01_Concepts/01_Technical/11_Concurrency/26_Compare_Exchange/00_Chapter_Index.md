# 26 Compare Exchange

## Chapter map

- [[CAS_Semantics|01. CAS Semantics]]
- [[Strong_vs_Weak|02. Strong vs Weak]]
- [[Expected_Argument|03. Expected Argument]]
- [[Failure_Memory_Order|04. Failure Memory Order]]
- [[CAS_Loop|05. CAS Loop]]
- [[Stack_Pop|06. Stack Pop]]
- [[Atomic_State_Machine|07. Atomic State Machine]]
- [[ABA_Interaction|08. ABA Interaction]]
- [[Spurious_Failure|09. Spurious Failure]]
- [[Backoff|10. Backoff]]
- [[Memory_Reclamation|11. Memory Reclamation]]
- [[CAS_Debugging|12. CAS Debugging]]

## Chapter purpose
This chapter builds a reusable mental model for **Compare Exchange**, with emphasis on correctness, timing, memory ordering, lifecycle, debugging, and embedded-system consequences.

## Cross-chapter reasoning
- Start with state ownership.
- Identify execution contexts and possible interleavings.
- State the synchronization edge or ownership transfer.
- Prove safety and liveness separately.
- Then evaluate latency, throughput, power, and maintainability.
