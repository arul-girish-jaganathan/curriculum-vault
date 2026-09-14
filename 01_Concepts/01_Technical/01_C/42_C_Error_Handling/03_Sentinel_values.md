# Sentinel values

> Canonical C topic note — chapter 42. This note follows the same deep-reference pattern as `01_C/13_C_Pointers/05_void_pointers.md`: precise definition → mechanism and rules → embedded implications → edge cases → example → verification → Staff-level reasoning.

## Definition

**Sentinel values** is the engineering concept concerned with **reserved return values such as -1, NULL, SIZE_MAX, or special enum members and their collision risks.**.

Separate three layers when reasoning about it:

1. **ISO C semantics** — what the language actually guarantees.
2. **Implementation/ABI behavior** — compiler, libc, ABI, object format, optimization, and target-specific rules.
3. **Hardware/system behavior** — MCU/CPU memory system, peripherals, interrupts, DMA, caches, debug hardware, or RTOS behavior where applicable.

Do not use a debugger result, compiler extension, or hardware convention as evidence that ISO C itself guarantees a behavior.

## Mechanism and language rules

The core reasoning model is:

`source construct → C semantic constraints → compiler representation → ABI/machine instructions → target state → externally observable behavior`

For this topic, the important questions are:

- What objects, values, types, pointers, storage durations, and evaluation steps participate?
- Which operations are constrained at compile time, and which failures occur only at runtime?
- Which assumptions are portable and which are implementation-defined, unspecified, or undefined?
- Does optimization preserve the intended invariant, or is the program relying on behavior the language does not guarantee?
- If a pointer is involved, verify **type, alignment, lifetime, bounds, provenance/validity assumptions, and ownership** independently.
- If concurrency or hardware is involved, distinguish **compiler ordering, CPU ordering, atomicity, cache visibility, and device ordering**.

A useful Staff-level rule is to make hidden assumptions explicit in the API contract instead of relying on a caller or debugger to infer them.

## Embedded implications

In firmware, this topic can affect:

- **RAM/ROM:** object size, stack frames, descriptors, diagnostic buffers, and code generation.
- **Timing:** instruction count, worst-case latency, interrupt interference, cache effects, and debugger perturbation.
- **Power:** extra polling, logging, retries, memory traffic, and wakeups.
- **ABI:** register usage, calling convention, interrupt wrappers, structure layout, and address width.
- **Memory system:** SRAM/TCM/flash placement, cacheability, MPU/MMU/IOMMU attributes, and device-visible regions.
- **Reliability:** fault containment, deterministic recovery, watchdog interaction, and diagnosability.

The key embedded question is not merely “does this work?” but **“under the worst compiler, timing, memory, reset, and fault conditions that the product permits, does the contract still hold?”**

## Edge cases and failure modes

The most dangerous failures are usually boundary-condition failures rather than the normal case.

### Common failure classes

- Width or signedness changes the result.
- A boundary value violates an implicit precondition.
- An object is accessed outside its lifetime or valid bounds.
- An address is valid to the CPU but not to a peripheral/device.
- A read-modify-write sequence loses an update.
- A debugger observation changes timing or hardware state.
- A debug build hides an optimization-sensitive defect.
- A compiler extension is silently assumed to be portable C.
- A failure path leaves ownership or resource state ambiguous.
- Error handling, synchronization, or cleanup is correct only on the happy path.

### Review discipline

For every suspicious line, ask:

1. What exact C rule makes this valid?
2. What is the smallest counterexample?
3. What changes at the type/width boundary?
4. What changes at `-O0` versus production optimization?
5. What changes across 32-bit and 64-bit targets?
6. What changes under interrupt/DMA/concurrent access?
7. What evidence would falsify my current hypothesis?

## Example pattern

The following pattern is intentionally small. The important part is the contract around the operation, not clever syntax.

```c
#include <stdint.h>
#include <stdbool.h>

static bool example_operation(uint32_t input, uint32_t *output)
{
    if (output == NULL) {
        return false;
    }

    /* Establish the precondition before producing externally visible state. */
    if (input > UINT32_C(1000)) {
        return false;
    }

    *output = input + UINT32_C(1);
    return true;
}
```

For **Sentinel values**, adapt the example so that the critical invariant is visible at the boundary. **Example investigation:** Use a pointer NULL sentinel only when NULL cannot also be a valid result.

## Performance, timing, memory, and power

Do not optimize this topic in isolation.

- Measure **worst case**, not only average case, when it participates in a real-time path.
- Inspect code size and stack impact when changing implementation technique.
- Consider memory traffic, cache behavior, bus contention, and peripheral access cost.
- On low-power systems, account for polling, trace, wakeups, and retained diagnostic state.
- Compare production-like optimization and link-time settings before accepting timing conclusions.
- If behavior is safety/security sensitive, prefer deterministic and auditable operations over clever micro-optimizations.

A useful evidence chain is:

`requirement → invariant → implementation → generated code/hardware transaction → measurement → regression test`

## Verification / debugging

Use multiple independent forms of evidence.

### Static checks

- Enable strong compiler warnings.
- Run static analysis for type, bounds, lifetime, concurrency, and API-contract violations.
- Add `_Static_assert` checks for widths, sizes, alignment, and configuration assumptions where appropriate.

### Dynamic checks

- Unit-test nominal and boundary values.
- Inject failures at every resource/ownership/state transition.
- Use sanitizers on host builds where the target cannot support them.
- Stress timing-sensitive paths at worst-case event rates.

### Target checks

- Inspect disassembly when source-level behavior is surprising.
- Inspect linker maps for placement and size assumptions.
- Capture registers, memory, timestamps, and ownership state.
- Use non-halting trace or instrumentation when a breakpoint would perturb timing.

### Topic-specific verification

**prove the sentinel is outside the valid domain and test boundary values.**

## Topic-specific failure modes

sentinel collisions, signed/unsigned conversion, and APIs that return both data and status in one scalar.

## Common mistakes

1. **Confusing syntax with a guarantee.** A construct compiling successfully does not prove its runtime behavior is defined.
2. **Ignoring boundaries.** Most defects appear at width, lifetime, ownership, or timing transitions.
3. **Trusting `volatile` as a universal synchronization mechanism.** It is not a substitute for atomicity, memory ordering, or cache maintenance.
4. **Debugging only the debug build.** Production optimization is part of the system under test.
5. **Hiding assumptions in comments.** Put important constraints into types, assertions, APIs, tests, or generated configuration checks.
6. **Fixing symptoms without preserving evidence.** A workaround that changes timing can make an intermittent bug disappear without removing its cause.

## Staff-level review checklist

Before approving code involving **Sentinel values**, verify:

- [ ] The language-level rule is stated precisely.
- [ ] Implementation-defined and target-specific behavior is identified.
- [ ] Type, width, alignment, lifetime, and ownership assumptions are explicit.
- [ ] Failure behavior and recovery boundaries are documented.
- [ ] Optimization effects have been considered.
- [ ] Timing and memory costs are measured where relevant.
- [ ] Boundary and fault-injection tests exist.
- [ ] Debug/diagnostic evidence can be collected without invalidating the failure.
- [ ] Portability impact is understood across compilers/architectures.
- [ ] The design is simpler or safer than the obvious alternatives for the product context.

## Staff-level takeaway

A Staff engineer should be able to explain not only **what Sentinel values does**, but **why the design remains correct when the compiler optimizes it, the target behaves adversarially, and the system enters failure or recovery states**.

The strongest implementation makes its assumptions visible, minimizes undefined behavior and hidden coupling, provides evidence for timing/memory claims, and gives reviewers a clear contract they can independently verify.

## Related

[[02_*]]
[[04_*]]
[[00_Chapter_Index]]
