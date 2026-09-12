# Population count

> Canonical C topic note — Chapter 43. Population count (popcount) counts the number of set bits in an integer representation.

## Definition
For an unsigned word, popcount returns a value from zero through the word width. It is useful for masks, resource allocation, parity-related algorithms, bitmap management, and protocol validation. C does not require a particular implementation strategy.

## Mechanism and language rules
A classic portable algorithm repeatedly clears the lowest set bit: `x &= x - 1`, incrementing a counter until zero. Hardware may provide a dedicated instruction; compilers can recognize loops or expose builtins.

### What to reason about
- What is the operand width?
- Is the operand unsigned?
- Is latency required to be constant with respect to input population?
- Does the target have a hardware instruction?
- Is the result type large enough to represent the maximum count?

## Embedded implications
The Kernighan-style loop takes work proportional to the number of set bits. A lookup-table implementation trades flash for predictable operations. A native instruction may be both smaller and faster. On timing-sensitive or security-sensitive paths, input-dependent latency must be considered.

### Firmware review angle
For a 32-bit word the maximum result is 32, so a small unsigned type is sufficient for the result, but using `unsigned` often avoids unnecessary conversion issues. Prefer compiler-supported intrinsics behind a portability layer when performance is critical.

## Edge cases and failure modes
- Signed operands invite representation/sign issues.
- Lookup tables can create cache-dependent timing on larger systems.
- Assuming hardware popcount exists on every target harms portability.
- Treating the count as parity confuses two different operations.

## Example pattern
```c
unsigned popcount32(uint32_t x)
{
    unsigned count = 0U;
    while (x != 0U) {
        x &= x - 1U;
        ++count;
    }
    return count;
}
```
The loop removes one set bit per iteration.

## Verification / debugging
Test zero, one-bit values, all bits set, alternating patterns, and random words. Compare against a trusted host implementation. Benchmark worst-case and best-case latency on the actual MCU if timing matters.

## Staff-level takeaway
Choose popcount implementation based on **target instruction set, code size, latency determinism, and security requirements**, not merely source-level elegance.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
