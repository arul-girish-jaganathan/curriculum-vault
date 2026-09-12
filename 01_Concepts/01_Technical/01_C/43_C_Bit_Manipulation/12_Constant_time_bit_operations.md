# Constant-time bit operations

> Canonical C topic note — Chapter 43. Constant-time bit manipulation aims to make execution behavior independent of secret-dependent values. C syntax alone cannot guarantee constant machine-level timing.

## Definition
A constant-time algorithm avoids secret-dependent branches, memory accesses, and other operations whose timing can reveal information. This is a security property stronger than simply writing a loop with a fixed source-level iteration count.

## Mechanism and language rules
C specifies functional behavior, not instruction latency, caches, pipelines, branch prediction, interrupts, or compiler transformations. Therefore constant-time claims require an implementation and target model.

### What to reason about
- Are branches controlled by secret data?
- Are table indices secret-dependent?
- Can the compiler transform branchless code into branches?
- Does the target have variable-latency arithmetic?
- Can interrupts or caches dominate the timing signal?

Bitwise select idioms can avoid obvious branches, but signed overflow, invalid shifts, and undefined behavior must still be eliminated because the compiler can exploit UB when optimizing.

## Embedded implications
On MCUs without caches, timing analysis can be simpler, but interrupt latency, flash wait states, memory buses, and variable-latency instructions still matter. Cryptographic code often requires a defined threat model rather than a generic “constant-time” label.

### Firmware review angle
Prefer vetted cryptographic primitives and compiler/target combinations with established constant-time analysis. Inspect assembly for security-critical functions and test timing distributions, while recognizing that board-level noise does not prove absence of leakage.

## Edge cases and failure modes
- Secret-dependent table lookup leaks through memory timing.
- A branchless source expression becomes conditional machine code.
- Undefined behavior enables unexpected compiler transformations.
- Data-dependent instruction latency is ignored.
- A constant-time function is called through a path with secret-dependent control flow.

## Example pattern
```c
uint32_t select_mask(uint32_t condition)
{
    uint32_t mask = 0U - (condition != 0U);
    return mask;
}
```
This illustrates a common mask construction; whether the surrounding algorithm is constant-time still requires target/compiler analysis.

## Verification / debugging
Inspect optimized assembly, use static constant-time analysis where available, test representative timing distributions, and review memory-access patterns. Keep compiler versions fixed for security-sensitive builds.

## Staff-level takeaway
Constant-time is a **whole toolchain and threat-model property**, not a visual property of C code. Eliminate UB, constrain compiler freedom appropriately, inspect generated code, and validate the complete execution path.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
