# Rotations

> Canonical C topic note — Chapter 43. A bit rotation moves bits around a fixed-width word while wrapping discarded bits back into the opposite side. Unlike a shift, no information is intentionally discarded.

## Definition
A left rotation of an `N`-bit unsigned value by `r` positions is conceptually `(x << r) | (x >> (N-r))`, with the shift count normalized into `0..N-1`.

## Mechanism and language rules
The naive expression is dangerous when `r == 0` or `r >= N`, because a shift by the type width is undefined. Normalize the count first and use an unsigned type with known width.

### What to reason about
- What is the exact word width?
- Is the rotation count normalized?
- Are all shifts performed on an unsigned type?
- Does the compiler recognize the idiom and emit a rotate instruction?
- Is the operation part of a cryptographic primitive where constant-time behavior matters?

C does not historically provide a universal rotate operator, so target/compiler support may require intrinsics or carefully defined helpers.

## Embedded implications
Rotations are common in hashes, CRC-related transforms, checksums, PRNGs, and bit-scrambling. Native rotate instructions can reduce cycles and code size on some CPUs.

### Firmware review angle
Isolate compiler/target intrinsics behind a small abstraction if multiple architectures are supported. Test the exact-width semantics independently of the CPU's native instruction.

## Edge cases and failure modes
- Rotate count zero causes a shift-by-width in the naive expression.
- Integer promotion changes the intended width.
- Signed operands introduce undesirable semantics.
- Using a 32-bit helper for a 16-bit algorithm changes the algorithm.

## Example pattern
```c
#include <stdint.h>

static uint32_t rotl32(uint32_t x, unsigned r)
{
    r &= 31U;
    if (r == 0U) {
        return x;
    }
    return (x << r) | (x >> (32U - r));
}
```
The explicit zero case avoids an invalid shift count.

## Verification / debugging
Test counts `0`, `1`, `31`, `32`, and values with one bit set at each boundary. Compare against a trusted mathematical/reference implementation. Inspect assembly when rotation is performance-critical.

Staff-level questions: Is the width part of the algorithm contract? Does the compiler generate one rotate instruction? Is the helper portable without relying on implementation-specific behavior?

## Staff-level takeaway
A rotation is a **fixed-width operation**. Normalize the count, use an unsigned width-specific type, and verify generated code when performance or constant-time behavior matters.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
