# Constant-time bit operations

> Canonical C topic note — Chapter 43. Constant-time bit manipulation aims to avoid secret-dependent execution behavior, but C source alone cannot guarantee constant machine-level timing.

## Definition
A constant-time implementation avoids secret-dependent branches, memory addresses, and other operations that can produce measurable timing differences. It is a security property evaluated against a defined target and threat model.

## Mechanism and language rules
C specifies functional semantics, not pipeline latency, caches, branch prediction, interrupt behavior, or compiler transformations. A branchless source expression may still compile into conditional instructions or use variable-latency operations.

### What to reason about
- Are branches controlled by secret data?
- Are table indices secret-dependent?
- Can optimization reintroduce branches?
- Are arithmetic instructions data-dependent in latency on the target?
- Do caches, flash wait states, or interrupts dominate the measurement?
- Does undefined behavior give the optimizer extra freedom?

Use unsigned arithmetic and eliminate invalid shifts/overflow before making timing claims.

## Embedded implications
MCUs without caches can simplify analysis, but flash wait states, memory buses, interrupts, DMA contention, and variable-latency instructions still matter. Cryptographic primitives should normally come from vetted implementations with established constant-time properties.

### Firmware review angle
Fix compiler/toolchain versions for security-sensitive builds, inspect optimized assembly, and evaluate the complete call path—not just a helper function. Consider whether hardware crypto accelerators provide a stronger isolation boundary.

## Edge cases and failure modes
- Secret-dependent table lookup.
- Branchless source becomes conditional machine code.
- Undefined behavior enables unexpected transformations.
- Data-dependent instruction latency is ignored.
- A constant-time primitive is called from a secret-dependent outer branch.

## Example pattern
```c
uint32_t mask_from_bool(unsigned condition)
{
    return 0U - (uint32_t)(condition != 0U);
}
```
This is a common mask construction; it does not by itself prove the complete algorithm is constant-time.

## Verification / debugging
Inspect optimized assembly and memory-access traces. Use constant-time analysis tools where available and measure timing distributions under controlled conditions. Keep security review focused on the threat model and leakage channel rather than a generic “branchless” label.

Staff-level questions: What attacker can measure timing? Which compiler transformations are possible? Are memory accesses secret-independent? What hardware noise sources exist, and which ones are actually relevant?

## Staff-level takeaway
Constant-time behavior is a **whole-toolchain, target, and threat-model property**. Eliminate UB, control compiler assumptions, inspect generated code, and validate the complete execution path.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
