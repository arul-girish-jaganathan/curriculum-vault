# 13 Linux Kernel Memory Model

## Chapter map

- [[LKMM_Purpose|01. LKMM Purpose]]
- [[Plain_Accesses|02. Plain Accesses]]
- [[READ_ONCE|03. READ_ONCE]]
- [[WRITE_ONCE|04. WRITE_ONCE]]
- [[Atomic_RMW|05. Atomic RMW]]
- [[smp_load_acquire|06. smp_load_acquire]]
- [[smp_store_release|07. smp_store_release]]
- [[smp_mb|08. smp_mb]]
- [[Control_Dependencies|09. Control Dependencies]]
- [[Address_Dependencies|10. Address Dependencies]]
- [[Locking_and_Ordering|11. Locking and Ordering]]
- [[Common_LKMM_Mistakes|12. Common LKMM Mistakes]]

## Chapter purpose
This chapter builds a reusable mental model for **Linux Kernel Memory Model**, with emphasis on correctness, timing, memory ordering, lifecycle, debugging, and embedded-system consequences.

## Cross-chapter reasoning
- Start with state ownership.
- Identify execution contexts and possible interleavings.
- State the synchronization edge or ownership transfer.
- Prove safety and liveness separately.
- Then evaluate latency, throughput, power, and maintainability.
