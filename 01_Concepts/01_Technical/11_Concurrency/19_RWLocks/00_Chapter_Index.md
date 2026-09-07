# 19 Reader-Writer Locks

## Chapter map

- [[Read_Sharing|01. Read Sharing]]
- [[Write_Exclusivity|02. Write Exclusivity]]
- [[Reader_Bias|03. Reader Bias]]
- [[Writer_Bias|04. Writer Bias]]
- [[Fairness|05. Fairness]]
- [[Upgrade_and_Downgrade|06. Upgrade and Downgrade]]
- [[Lock_Recursion|07. Lock Recursion]]
- [[Contention|08. Contention]]
- [[Cache_Traffic|09. Cache Traffic]]
- [[When_RWLock_Fails|10. When RWLock Fails]]
- [[Alternatives|11. Alternatives]]
- [[Embedded_Review|12. Embedded Review]]

## Chapter purpose
This chapter builds a reusable mental model for **Reader-Writer Locks**, with emphasis on correctness, timing, memory ordering, lifecycle, debugging, and embedded-system consequences.

## Cross-chapter reasoning
- Start with state ownership.
- Identify execution contexts and possible interleavings.
- State the synchronization edge or ownership transfer.
- Prove safety and liveness separately.
- Then evaluate latency, throughput, power, and maintainability.
