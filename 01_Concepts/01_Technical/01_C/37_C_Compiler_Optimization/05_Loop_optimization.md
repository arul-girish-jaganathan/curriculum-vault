# Loop optimization

> Canonical C topic note — chapter 37.

## Definition
Loop optimization transforms repeated computation while preserving required C behavior. Common transformations include invariant-code motion, induction-variable simplification, unrolling, fusion, fission, interchange, unswitching, vectorization, and strength reduction.

## Mechanism and language rules
Loops are attractive because small improvements multiply by iteration count. The compiler needs proof that transformations preserve dependencies, overflow semantics, aliasing rules, volatile accesses, and observable effects.

```c
for (size_t i = 0; i < n; ++i)
    dst[i] = src[i] + bias;
```

A compiler may hoist `bias`, choose wider registers, unroll iterations, or vectorize if aliasing and target constraints permit. Signed overflow, pointer provenance/lifetime rules, and possible overlap can block transformations or make incorrect source code appear to work only at low optimization.

## Embedded implications
Loop optimization directly affects CPU cycles, flash size, instruction-cache behavior, memory bandwidth, and energy. Unrolling can reduce branch overhead but increase code size. Vectorization may be irrelevant or unavailable on small MCUs but important on DSP/SIMD-capable cores.

For real-time firmware, average loop speed is insufficient. Consider worst-case iterations, interrupt interference, cache state, memory wait states, and bounds checks. Avoid hand-unrolling until measurements show a need.

## Edge cases and failure modes
- Assuming `n` is nonzero or within a safe range without a contract.
- Violating aliasing assumptions between `src` and `dst`.
- Using signed arithmetic where overflow is possible.
- Expecting a volatile loop to be freely optimized.
- Creating huge unrolled code that increases flash or cache misses.

## Verification / debugging
Use optimization reports and compare generated assembly. Benchmark representative sizes and boundary cases on the target. Use sanitizers and static analysis on host builds to expose overflow, bounds, and aliasing defects before interpreting optimizer behavior.

## Staff-level takeaway
Optimize loops by identifying the dominant resource and preserving proof obligations. A fast loop that depends on UB, accidental non-aliasing, or a particular compiler version is not a robust optimization.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
