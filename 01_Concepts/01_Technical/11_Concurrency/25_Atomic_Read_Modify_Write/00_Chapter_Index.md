# 25 Atomic Read Modify Write

## Chapter map

- [[fetch_add|01. fetch_add]]
- [[fetch_sub|02. fetch_sub]]
- [[fetch_or|03. fetch_or]]
- [[fetch_and|04. fetch_and]]
- [[fetch_xor|05. fetch_xor]]
- [[exchange|06. exchange]]
- [[test_and_set|07. test_and_set]]
- [[Clear|08. Clear]]
- [[Reference_Counts|09. Reference Counts]]
- [[Statistics_Counters|10. Statistics Counters]]
- [[Ticket_Allocation|11. Ticket Allocation]]
- [[RMW_Contention|12. RMW Contention]]

## Chapter purpose
This chapter builds a reusable mental model for **Atomic Read Modify Write**, with emphasis on correctness, timing, memory ordering, lifecycle, debugging, and embedded-system consequences.

## Cross-chapter reasoning
- Start with state ownership.
- Identify execution contexts and possible interleavings.
- State the synchronization edge or ownership transfer.
- Prove safety and liveness separately.
- Then evaluate latency, throughput, power, and maintainability.
