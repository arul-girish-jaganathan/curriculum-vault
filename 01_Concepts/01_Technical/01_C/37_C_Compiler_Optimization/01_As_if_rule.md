# As-if rule

> Canonical C topic note — chapter 37.

## Definition
The C implementation may transform a program in any way as long as every **observable behavior required by the language** is preserved. This is commonly called the *as-if rule*. It is not permission to change defined behavior arbitrarily; it is the foundation on which optimization is built.

ISO C does not prescribe a particular instruction sequence, register allocation, stack frame, or execution time for ordinary hosted code. It does constrain what a conforming implementation must make observable. The exact boundary also depends on the C standard version, implementation extensions, volatile semantics, library behavior, I/O, atomics, and the target ABI.

## Mechanism and language rules
A compiler reasons from the C abstract machine. If two executions are indistinguishable with respect to required observable behavior, the implementation may choose the cheaper representation.

Important observables include accesses to `volatile` objects, externally visible I/O and library effects, termination behavior, and the sequencing requirements imposed by the language. Ordinary non-volatile memory that is never externally observed can often be eliminated, reordered, folded, or kept entirely in registers.

```c
int square_plus_one(int x)
{
    return x * x + 1;
}
```

The compiler can replace arithmetic with equivalent instructions, inline the function, specialize constant arguments, or remove the function entirely if no observable distinction remains.

### Undefined behavior changes the optimization boundary
If a program executes undefined behavior, the implementation has no requirement to preserve the programmer's intended result. Optimizers may use assumptions such as “this signed addition cannot overflow” or “this pointer is valid” when proving transformations. A release-only failure is often evidence of a violated language contract, not an optimizer bug.

### `volatile` is not a universal optimization barrier
A volatile access is observable and must be performed according to the rules for volatile accesses, but `volatile` does not automatically make surrounding non-volatile operations atomic, ordered with other threads, or synchronized with hardware. Hardware memory barriers and C atomics solve different problems.

## Embedded implications
For firmware, the as-if rule explains why source-level intuition is unreliable for timing and register state. A loop can disappear, a helper can become zero instructions, and a memory access can move into a different generated sequence while preserving the C-defined result.

MMIO should normally be represented through appropriately qualified volatile objects or vendor abstractions. Shared data between execution contexts needs an actual concurrency contract; volatile alone does not establish inter-thread happens-before relationships.

Optimization can also alter interrupt latency, stack depth, flash footprint, power consumption, and worst-case execution time. Therefore “same C behavior” does not mean “same real-time behavior.”

## Edge cases and failure modes
- Assuming every source statement executes exactly once.
- Using a non-volatile variable as a hardware register.
- Depending on the number of loop iterations for delay without a timing contract.
- Expecting an unused write to remain in the binary.
- Treating undefined behavior as a valid optimization constraint.
- Assuming `volatile` prevents compiler reordering of all surrounding operations.
- Measuring debug builds and assuming the measurements represent production firmware.

## Verification / debugging
Compare `-O0`, `-O2`/`-O3`, and the production configuration. Inspect disassembly and map files rather than source alone. If behavior changes with optimization, first run undefined-behavior sanitizers on a host build and enable aggressive warnings. For firmware, inspect MMIO accesses, interrupt entry/exit timing, and generated barriers.

A useful review question is: **Which C-level observable behavior requires this generated instruction to exist?** If there is no valid answer, the compiler may legally remove or transform it.

## Staff-level takeaway
Optimization is not a separate semantic universe. The compiler is exploiting the C contract you wrote. Staff-level engineers should make invariants explicit, eliminate undefined behavior, identify true observables, and verify timing or hardware requirements at the binary boundary instead of relying on source-code appearance.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
