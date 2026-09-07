# 06 Races and Race Conditions

## Chapter map

- [[Race_Condition_Definition|01. Race Condition Definition]]
- [[Data_Race_Definition|02. Data Race Definition]]
- [[Check_Then_Act|03. Check-Then-Act]]
- [[Lost_Update|04. Lost Update]]
- [[TOCTOU|05. TOCTOU]]
- [[Double_Initialization|06. Double Initialization]]
- [[Use_After_Free_Races|07. Use-After-Free Races]]
- [[ABA_Like_Races|08. ABA-Like Races]]
- [[Interrupt_Races|09. Interrupt Races]]
- [[Teardown_Races|10. Teardown Races]]
- [[Racy_Error_Handling|11. Racy Error Handling]]
- [[Race_Review_Method|12. Race Review Method]]

## Chapter purpose
This chapter builds a reusable mental model for **Races and Race Conditions**, with emphasis on correctness, timing, memory ordering, lifecycle, debugging, and embedded-system consequences.

## Cross-chapter reasoning
- Start with state ownership.
- Identify execution contexts and possible interleavings.
- State the synchronization edge or ownership transfer.
- Prove safety and liveness separately.
- Then evaluate latency, throughput, power, and maintainability.
