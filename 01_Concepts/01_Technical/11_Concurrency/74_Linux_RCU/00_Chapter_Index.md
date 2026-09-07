# 74 Linux RCU

## Chapter map

- [[RCU_Motivation|01. RCU Motivation]]
- [[Read_Side_Critical_Section|02. Read-Side Critical Section]]
- [[Grace_Period|03. Grace Period]]
- [[Quiescent_State|04. Quiescent State]]
- [[Call_RCU|05. Call RCU]]
- [[synchronize_rcu|06. synchronize_rcu]]
- [[kfree_rcu|07. kfree_rcu]]
- [[Update_Side|08. Update Side]]
- [[RCU_List|09. RCU List]]
- [[SRCU|10. SRCU]]
- [[RCU_vs_RWLock|11. RCU vs RWLock]]
- [[RCU_Debugging|12. RCU Debugging]]

## Chapter purpose
This chapter builds a reusable mental model for **Linux RCU**, with emphasis on correctness, timing, memory ordering, lifecycle, debugging, and embedded-system consequences.

## Cross-chapter reasoning
- Start with state ownership.
- Identify execution contexts and possible interleavings.
- State the synchronization edge or ownership transfer.
- Prove safety and liveness separately.
- Then evaluate latency, throughput, power, and maintainability.
