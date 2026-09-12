# ThreadSanitizer

> Canonical C topic note — chapter 40.

## Definition
ThreadSanitizer (TSan) instruments concurrent programs to detect many data races and synchronization errors. It is a dynamic analysis tool; it does not prove that a program is race-free.

## Mechanism and language rules
TSan tracks memory accesses and synchronization events and reports conflicting accesses lacking the required synchronization relationship. Correct interpretation depends on the language memory model and the actual synchronization primitives.

## Embedded implications
Many MCU firmware projects use RTOS tasks, interrupts, DMA, and lock-free structures rather than host threads. TSan is strongest for host-side concurrency models; interrupt interactions and device memory require separate reasoning.

## Edge cases and failure modes
- Assuming `volatile` makes accesses race-free.
- Running only single-threaded tests.
- Suppressing races without determining ownership.
- Expecting TSan to model MMIO or every RTOS primitive automatically.

## Verification / debugging
Build a host model using real synchronization primitives where possible. Reproduce reports with deterministic tests and inspect both conflicting accesses. For target concurrency, combine code review, atomicity analysis, RTOS checks, and hardware stress tests.

## Staff-level takeaway
TSan is a race detector, not a concurrency design. The real contract is ownership, synchronization, atomicity, and lifetime; the tool provides evidence about violations of that contract.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
