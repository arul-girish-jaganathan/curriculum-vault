# Leading/trailing zeros

> Canonical C topic note — Chapter 43. Counting leading zeros (CLZ) and trailing zeros (CTZ) finds bit positions efficiently, but zero-input behavior must be explicitly defined because many compiler builtins leave it undefined.

## Definition
CLZ counts zero bits above the highest set bit; CTZ counts zero bits below the lowest set bit. For an `N`-bit word, nonzero results are in `0..N-1`.

## Mechanism and language rules
Portable algorithms can test bits iteratively or use binary-search-style masks. Compiler builtins may map to efficient instructions, but their zero-input contracts differ. Never call a primitive with zero unless its specification defines that case.

### What to reason about
- Is zero a valid input?
- What exact operand width is counted?
- Does the compiler builtin define zero behavior?
- Is the result used as a shift count or index?
- Does the target have CLZ/CTZ instructions?

If the result feeds a shift, prove that the resulting shift count is within range.

## Embedded implications
These operations are useful for priority bitmaps, scheduler selection, normalization, encoding, and resource allocation. Hardware instructions can make them very fast and deterministic on supported CPUs.

### Firmware review angle
Wrap target builtins with a project-defined zero-safe API when portability matters. Document whether the operation is expected to be constant-time.

## Edge cases and failure modes
- Zero input passed to an undefined builtin.
- Wrong width due to `int` promotion.
- CLZ result used directly as an invalid shift count.
- Signed value interpreted as a bit pattern without an explicit contract.

## Example pattern
```c
static unsigned ctz32(uint32_t x)
{
    if (x == 0U) {
        return 32U; /* project-defined sentinel */
    }
    unsigned n = 0U;
    while ((x & 1U) == 0U) {
        x >>= 1U;
        ++n;
    }
    return n;
}
```
The sentinel `32` is part of the wrapper contract and must not be used as an unchecked shift count.

## Verification / debugging
Test zero, one, highest bit, lowest bit, and alternating patterns. Compare portable and target-specific implementations. Verify the compiler builtin's exact zero behavior before wrapping it.

Staff-level questions: Is zero possible at the call site? Is the sentinel type-safe? Does the generated implementation meet timing requirements?

## Staff-level takeaway
CLZ/CTZ are **boundary-sensitive primitives**. Zero-input semantics and exact width must be part of the API contract, especially when results feed shifts, indexes, or priority calculations.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
