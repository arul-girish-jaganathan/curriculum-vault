# Saturating arithmetic patterns

> Canonical C topic note — Chapter 43. Saturating arithmetic clamps a result to a representable minimum or maximum instead of wrapping or invoking signed-overflow undefined behavior.

## Definition
For unsigned values, ordinary C arithmetic wraps modulo the type's range. For signed values, overflow is undefined behavior. Saturation intentionally detects the boundary before performing an overflowing operation and returns the limit instead.

## Mechanism and language rules
For unsigned addition, overflow can be detected with `a > UINT_MAX - b`. For unsigned subtraction, underflow can be detected with `a < b`. For signed arithmetic, perform a range check in a wider type when one is guaranteed to represent the mathematical result, or use a carefully proven comparison before the operation.

### What to reason about
- What is the exact numeric range?
- Can the intermediate expression overflow before the check?
- Are operands promoted to a wider type?
- Is wraparound actually desired?
- Is the operation required to be constant-time?

## Embedded implications
Saturation is common in audio, control, sensor scaling, fixed-point arithmetic, and safety limits. It prevents wraparound from turning a large positive command into a negative or small value.

### Firmware review angle
Saturation policy should be part of the algorithm contract. On DSP-capable MCUs, native saturating instructions may outperform portable C, but compiler intrinsics should be isolated behind a target abstraction when portability matters.

## Edge cases and failure modes
- Checking `a + b > MAX` is already too late if `a + b` overflows.
- Signed overflow is not a valid way to detect overflow.
- Saturating at an application limit differs from saturating at the C type limit.
- Conversions after a saturated calculation can still truncate.

## Example pattern
```c
#include <stdint.h>
#include <stdint.h>

uint32_t sat_add_u32(uint32_t a, uint32_t b)
{
    if (a > UINT32_MAX - b) {
        return UINT32_MAX;
    }
    return a + b;
}
```
The subtraction in the comparison is safe for unsigned arithmetic.

## Verification / debugging
Test zero, maximum, one below maximum, exact overflow boundary, and large operands. Use property tests to verify commutativity where expected and that the result never leaves the defined range.

## Staff-level takeaway
Saturation is fundamentally an **overflow-avoidance design**, not a post-processing clamp. Prove the intermediate arithmetic is defined, then evaluate whether target-specific instructions are justified by measured performance requirements.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
