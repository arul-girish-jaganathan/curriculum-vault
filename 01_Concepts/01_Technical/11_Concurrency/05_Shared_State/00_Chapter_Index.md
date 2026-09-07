# 05 Shared State

## Chapter map

- [[Definition|01. Definition]]
- [[Shared_Variables|02. Shared Variables]]
- [[Shared_Objects|03. Shared Objects]]
- [[Shared_Hardware_State|04. Shared Hardware State]]
- [[Ownership_Transfer|05. Ownership Transfer]]
- [[Read_Mostly_State|06. Read-Mostly State]]
- [[Write_Heavy_State|07. Write-Heavy State]]
- [[Composite_State|08. Composite State]]
- [[State_Invariants|09. State Invariants]]
- [[Shadow_Copies|10. Shadow Copies]]
- [[Snapshotting|11. Snapshotting]]
- [[Eliminating_Shared_State|12. Eliminating Shared State]]

## Chapter purpose
This chapter builds a reusable mental model for **Shared State**, with emphasis on correctness, timing, memory ordering, lifecycle, debugging, and embedded-system consequences.

## Cross-chapter reasoning
- Start with state ownership.
- Identify execution contexts and possible interleavings.
- State the synchronization edge or ownership transfer.
- Prove safety and liveness separately.
- Then evaluate latency, throughput, power, and maintainability.
