# As-if rule

## Definition
The **as-if rule** is the central permission that allows a conforming C implementation to transform a program aggressively: the implementation may perform any optimization as long as the observable behavior required by the C abstract machine is preserved. C does not require the generated instructions to resemble the source. It requires the externally observable result to satisfy the language rules.

## Scope and boundaries
The rule governs transformations, not permission to violate the C abstract machine. Undefined behavior, unspecified choices, implementation-defined behavior, volatile accesses, I/O, and synchronization affect what the compiler must preserve. The as-if rule does not make a data race valid, make an invalid pointer usable, or turn `volatile` into a general-purpose synchronization primitive.

## Mechanism and language rules
A compiler builds an internal model of values, control flow, memory, calls, and side effects. It can fold constants, eliminate unreachable work, reorder independent operations, inline functions, vectorize loops, or replace a sequence with an equivalent instruction sequence. The key question is whether a permitted observer could distinguish the transformation.

```c
int square(int x)
{
    return x * x;
}
```

The compiler may emit a multiply, inline the operation, or use another equivalent sequence. Source-level execution order is not itself an observable requirement.

### Observable behavior
Typical observable effects include accesses to volatile objects, interactions with files and terminal I/O in hosted implementations, and program termination behavior. The exact set is defined by ISO C and the implementation environment. Ordinary non-volatile memory accesses that have no externally visible consequence may be cached, reordered, combined, or removed.

### Undefined behavior changes the optimization boundary
If code executes undefined behavior, the implementation is no longer required to preserve the intuitive behavior surrounding that operation. For example, an out-of-bounds access can allow assumptions that make apparently unrelated code disappear. This is why “it worked at `-O0`” is not evidence of correctness.

## Embedded implications
The as-if rule is fundamental to firmware optimization. A compiler may remove a polling loop if the object is not volatile and there is no valid C-visible reason for it to change. It may fold register calculations, eliminate unused peripheral configuration, or reorder ordinary memory operations. Hardware-visible accesses therefore need the correct language and architecture contracts: `volatile` for required volatile accesses, atomics for C-level inter-thread synchronization, and target-specific barriers where hardware ordering requires them.

Optimization can change timing, stack usage, instruction alignment, interrupt latency, and power consumption while remaining fully conforming. Real-time requirements therefore need explicit measurement; source-code appearance is not a timing specification.

## Edge cases and failure modes
- Treating `volatile` as a complete memory barrier.
- Assuming a local variable is stored in RAM because the debugger shows it at `-O0`.
- Using undefined behavior as an accidental hardware primitive.
- Assuming function calls always prevent all reordering; interprocedural optimization can understand more than expected.
- Assuming a compiler must preserve instruction count or source statement order.
- Forgetting that observable behavior is different from “whatever a debugger can currently see.”

## Verification / debugging
Compare `-O0`, `-O2`/`-O3`, and production flags. Inspect assembly, linker maps, and generated DWARF. Use warnings, sanitizers, static analysis, and hardware tracing where appropriate. For hardware accesses, verify that the source uses the correct volatile-qualified declarations and architecture synchronization primitives.

A useful review question is: **what exact C or hardware rule makes this side effect observable or ordered?** If the answer is only “the compiler usually does it,” the design is not robust.

## Performance, timing, memory and power
The as-if rule permits large gains in code size, execution time, register allocation, cache behavior, and energy consumption. Those gains can also expose latent timing assumptions. Measure worst-case execution time and interrupt latency on the actual target rather than inferring them from source complexity.

## Staff-level takeaway
Treat optimization as a consequence of a correct semantic contract, not something that must be disabled to make firmware work. First make the program well-defined and correctly synchronized; then let the compiler optimize it. When behavior must remain visible to hardware or another execution agent, express that requirement with the appropriate C, ABI, and hardware mechanism.