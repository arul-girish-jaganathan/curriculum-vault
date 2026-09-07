# 66 C++ Mutexes and Locks

## Chapter map

- [[std_mutex|01. std::mutex]]
- [[recursive_mutex|02. recursive_mutex]]
- [[timed_mutex|03. timed_mutex]]
- [[shared_mutex|04. shared_mutex]]
- [[lock_guard|05. lock_guard]]
- [[unique_lock|06. unique_lock]]
- [[scoped_lock|07. scoped_lock]]
- [[adopt_lock|08. adopt_lock]]
- [[defer_lock|09. defer_lock]]
- [[try_to_lock|10. try_to_lock]]
- [[RAII_Locking|11. RAII Locking]]
- [[Exception_Safety|12. Exception Safety]]

## Chapter purpose
This chapter builds a reusable mental model for **C++ Mutexes and Locks**, with emphasis on correctness, timing, memory ordering, lifecycle, debugging, and embedded-system consequences.

## Cross-chapter reasoning
- Start with state ownership.
- Identify execution contexts and possible interleavings.
- State the synchronization edge or ownership transfer.
- Prove safety and liveness separately.
- Then evaluate latency, throughput, power, and maintainability.
