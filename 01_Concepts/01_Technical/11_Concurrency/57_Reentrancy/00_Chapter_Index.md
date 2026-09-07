# 57 Reentrancy

## Chapter map

- [[Definition|01. Definition]]
- [[Static_State_Hazards|02. Static State Hazards]]
- [[Recursive_Calls|03. Recursive Calls]]
- [[Signal_ISR_Reentry|04. Signal/ISR Reentry]]
- [[Callbacks|05. Callbacks]]
- [[Reentrant_APIs|06. Reentrant APIs]]
- [[Reentrancy_vs_Thread_Safety|07. Reentrancy vs Thread Safety]]
- [[Library_Constraints|08. Library Constraints]]
- [[Locking_Pitfalls|09. Locking Pitfalls]]
- [[State_Machines|10. State Machines]]
- [[Design_Patterns|11. Design Patterns]]
- [[Review|12. Review]]

## Chapter purpose
This chapter builds a reusable mental model for **Reentrancy**, with emphasis on correctness, timing, memory ordering, lifecycle, debugging, and embedded-system consequences.

## Cross-chapter reasoning
- Start with state ownership.
- Identify execution contexts and possible interleavings.
- State the synchronization edge or ownership transfer.
- Prove safety and liveness separately.
- Then evaluate latency, throughput, power, and maintainability.
