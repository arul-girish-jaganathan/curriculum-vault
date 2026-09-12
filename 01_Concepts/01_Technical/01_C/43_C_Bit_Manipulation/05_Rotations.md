# Rotations

> Canonical C topic note — Chapter 43. A rotation moves bits out of one end of a fixed-width word back into the other end. Unlike a shift, no information is discarded when the width and count are valid.

## Definition
For an unsigned `W`-bit word, rotate-left by `n` can be expressed as `(x << n) | (x >> (W - n))`, with `n` normalized into `[0, W-1]`. A zero count must be handled specially because shifting by the word width is invalid.

## Mechanism and language rules
C has no universally available pre-C23 rotate operator. Implementations may recognize canonical idioms or provide builtins. Use unsigned fixed-width types and validate/normalize the count.

### What to reason about
- What is the exact word width?
- Can `n == 0` occur?
- Is `n >= W` possible?
- Are operands promoted unexpectedly?
- Does the target have a native rotate instruction?

## Embedded implications
Rotations appear in hash functions, checksums, cryptographic primitives, PRNGs, bit scramblers, and protocol algorithms. A compiler may map a safe rotate idiom to one instruction, while a poorly written expression can generate extra shifts and branches.

### Firmware review angle
For cryptographic or constant-time code, inspect generated assembly rather than assuming the C idiom has constant latency. Use compiler builtins only behind a portability wrapper when the implementation set is controlled.

## Edge cases and failure modes
- Shifting by `W` is undefined.
- Signed operands introduce unnecessary complexity.
- Assuming `uint32_t` exists without checking the implementation profile.
- Using an expression that evaluates a volatile/MMIO operand more than once.

## Example pattern
```c
static uint32_t rotl32(uint32_t x, unsigned n)
{
    n &= 31U;
    if (n == 0U) {
        return x;
    }
    return (x << n) | (x >> (32U - n));
}
```
The explicit zero case prevents a 32-bit shift.

## Verification / debugging
Test counts 0, 1, 31, 32, 33 and random values. Compare against a reference implementation and inspect compiler output at the production optimization level.

## Staff-level takeaway
A rotate is a **fixed-width operation with a dangerous boundary at zero/full width**. Normalize counts, use unsigned operands, and verify the generated code when performance or constant-time behavior matters.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
