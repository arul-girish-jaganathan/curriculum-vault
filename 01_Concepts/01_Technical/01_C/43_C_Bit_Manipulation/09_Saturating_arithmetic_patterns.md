# Saturating arithmetic patterns

> Canonical C topic note — Chapter 43. Saturating arithmetic clamps a result to a defined numeric limit instead of wrapping or invoking signed-overflow undefined behavior.

## Definition
For unsigned addition, normal C arithmetic wraps modulo the type range. For signed arithmetic, overflow is undefined behavior. Saturation detects the boundary before the overflowing operation and returns the chosen limit.

## Mechanism and language rules
For unsigned addition, test `a > MAX - b`; for subtraction, test `a < b`. For signed values, prove the mathematical operation is representable before evaluating it, often by using a wider type where the implementation guarantees sufficient range.

### What to reason about
- Is the limit the C type limit or an application limit?
- Can an intermediate expression overflow before the check?
- What promotions occur?
- Is wraparound actually the intended algorithm?
- Does the implementation need constant-time behavior?

Never write `if (a + b > MAX)` as an overflow test for a type where `a + b` can already overflow.

## Embedded implications
Saturation is common in control, audio, sensor scaling, fixed-point arithmetic, and safety limits. It prevents wraparound from turning a high command into a low or negative value.

### Firmware review angle
Define saturation mathematically and test boundary behavior. Native saturating instructions may improve performance on DSP-capable targets, but isolate compiler intrinsics behind an abstraction when portability matters.

## Edge cases and failure modes
- Overflow occurs before the check.
- Signed overflow is used as an implicit detection mechanism.
- Application limit differs from machine limit.
- A later conversion truncates a correctly saturated result.
- Saturation hides an upstream invalid-input bug when rejection was required.

## Example pattern
```c
#include <stdint.h>

uint32_t sat_add_u32(uint32_t a, uint32_t b)
{
    if (a > UINT32_MAX - b) {
        return UINT32_MAX;
    }
    return a + b;
}
```
The comparison is safe because unsigned subtraction is defined modulo the type range.

## Verification / debugging
Test zero, maximum, maximum-minus-one, exact boundary, and overflowing operands. Use property tests to prove the result never exceeds the permitted range and compare optimized output with a reference implementation.

Staff-level questions: Is saturation part of the algorithm contract? Should out-of-range input be rejected instead? Does the target provide a measured performance advantage?

## Staff-level takeaway
Saturation is an **overflow-avoidance design**, not a post-overflow clamp. Prove every intermediate operation is defined before considering performance optimizations.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
