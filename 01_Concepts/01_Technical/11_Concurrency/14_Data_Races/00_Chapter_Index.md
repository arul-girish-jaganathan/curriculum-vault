# 14 Data Races

## Chapter map

- [[Race_Detection_Concept|01. Race Detection Concept]]
- [[Benign_vs_Non_Benign_Races|02. Benign vs Non-Benign Races]]
- [[Race_Patterns|03. Race Patterns]]
- [[Read_Modify_Write_Races|04. Read-Modify-Write Races]]
- [[Pointer_Publication_Races|05. Pointer Publication Races]]
- [[Lifetime_Races|06. Lifetime Races]]
- [[Reference_Count_Races|07. Reference Count Races]]
- [[Interrupt_vs_Thread_Races|08. Interrupt vs Thread Races]]
- [[DMA_Races|09. DMA Races]]
- [[Shutdown_Races|10. Shutdown Races]]
- [[Race_Reproduction|11. Race Reproduction]]
- [[Race_Prevention|12. Race Prevention]]

## Chapter purpose
This chapter builds a reusable mental model for **Data Races**, with emphasis on correctness, timing, memory ordering, lifecycle, debugging, and embedded-system consequences.

## Cross-chapter reasoning
- Start with state ownership.
- Identify execution contexts and possible interleavings.
- State the synchronization edge or ownership transfer.
- Prove safety and liveness separately.
- Then evaluate latency, throughput, power, and maintainability.
