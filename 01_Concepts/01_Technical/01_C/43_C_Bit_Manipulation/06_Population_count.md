# Population count

> Canonical C topic note — Chapter 43. Population count, or popcount, returns the number of set bits in an integer. It is a basic primitive for masks, bitsets, checksums, scheduling, and algorithms.

## Definition
For an unsigned value, popcount is the number of one bits in its representation. The result is bounded by the operand width.

## Mechanism and language rules
A portable implementation can repeatedly clear the lowest set bit with `x &= x - 1`, counting iterations. The expression relies on unsigned arithmetic, where wraparound is defined. C23 and implementation libraries may provide more direct facilities, while compiler builtins can map to target instructions.

### What to reason about
- What width is being counted?
- Is the operand signed or unsigned?
- Is execution time allowed to depend on the number of set bits?
- Does the target have a hardware popcount instruction?
- Is the result type large enough for the maximum count?

Choose the algorithm based on timing requirements, compiler support, and target capabilities.

## Embedded implications
Popcount can be used for active-channel counts, bitmap allocation, feature masks, and error syndromes. A variable-iteration implementation may be undesirable in a constant-time security path or hard real-time path.

### Firmware review angle
Use fixed-width types and isolate compiler intrinsics when portability is required. Measure actual generated code rather than assuming a clever source idiom is faster.

## Edge cases and failure modes
- Counting the wrong width after implicit promotion.
- Variable execution time violates a timing/security requirement.
- Signed input creates confusing representation assumptions.
- Target builtin availability differs between toolchains.

## Example pattern
```c
static unsigned popcount32(uint32_t x)
{
    unsigned count = 0U;
    while (x != 0U) {
        x &= x - 1U;
        ++count;
    }
    return count;
}
```
This performs one iteration per set bit.

## Verification / debugging
Test zero, one, all ones, alternating bits, and highest-bit-only values. Compare against a trusted reference or compiler builtin. Benchmark across realistic data distributions and optimization levels.

Staff-level questions: Is data-dependent timing acceptable? Does the compiler lower this to a hardware instruction? Is the width explicit?

## Staff-level takeaway
Popcount is simple mathematically but has **algorithmic, timing, and toolchain choices**. Select the implementation based on the actual target contract rather than source-level cleverness.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
