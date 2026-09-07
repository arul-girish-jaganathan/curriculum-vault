# 12 C++ Memory Model

## Chapter map

- [[C_Abstract_Machine|01. C++ Abstract Machine]]
- [[std_atomic|02. std::atomic]]
- [[Memory_Orders|03. Memory Orders]]
- [[Happens_Before|04. Happens Before]]
- [[Synchronizes_With|05. Synchronizes With]]
- [[Release_Sequence|06. Release Sequence]]
- [[Data_Races|07. Data Races]]
- [[std_atomic_ref|08. std::atomic_ref]]
- [[Volatile_in_C|09. Volatile in C++]]
- [[Static_Initialization|10. Static Initialization]]
- [[Object_Lifetime_and_Concurrency|11. Object Lifetime and Concurrency]]
- [[C_Memory_Model_Pitfalls|12. C++ Memory Model Pitfalls]]

## Chapter purpose
This chapter builds a reusable mental model for **C++ Memory Model**, with emphasis on correctness, timing, memory ordering, lifecycle, debugging, and embedded-system consequences.

## Cross-chapter reasoning
- Start with state ownership.
- Identify execution contexts and possible interleavings.
- State the synchronization edge or ownership transfer.
- Prove safety and liveness separately.
- Then evaluate latency, throughput, power, and maintainability.
