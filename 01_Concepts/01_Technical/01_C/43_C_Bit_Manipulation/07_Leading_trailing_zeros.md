# Leading/trailing zeros

> Canonical C topic note — Chapter 43. Count-leading-zeros and count-trailing-zeros operations locate the highest or lowest set bit and are building blocks for normalization, priority selection, and integer algorithms.

## Definition
For a fixed-width unsigned integer, CLZ counts zero bits before the highest set bit; CTZ counts zero bits after the lowest set bit. The all-zero input is a critical boundary and must be defined by the chosen API or implementation.

## Mechanism and language rules
C does not historically provide universal `clz`/`ctz` functions. Compiler builtins commonly exist, but many specify undefined behavior for zero. C23 adds standard bit utilities in implementations that support them, but the supported language/library profile must be checked.

### What to reason about
- What happens for zero?
- What is the exact width?
- Is the operand unsigned?
- Is the returned count used as a shift count?
- Does the next operation remain within range?

## Embedded implications
CLZ can implement priority encoders, normalization before fixed-point arithmetic, logarithm approximations, bitmap allocation, and efficient packet parsing. Many MCUs have native CLZ instructions, making intrinsic-based code highly efficient.

### Firmware review angle
A common defect is `1U << ctz(x)` without checking `x != 0`; another is using the result as a shift count equal to the word width. Treat zero as an explicit input case.

## Edge cases and failure modes
- Calling an API with zero when zero is outside its domain.
- Mixing 16-bit logical width with a 32-bit promoted operand.
- Using a returned count directly as a shift without bounds analysis.
- Assuming timing is constant across all implementations.

## Example pattern
```c
unsigned first_set_bit(uint32_t x)
{
    if (x == 0U) {
        return 32U; /* explicit sentinel for this API */
    }
    return (unsigned)__builtin_ctz(x);
}
```
The builtin is compiler-specific; production code should hide it behind a portability wrapper or use the project's supported standard API.

## Verification / debugging
Test zero, one, highest bit, lowest bit, and multiple-bit patterns. Compile with UBSan and warnings where applicable, and inspect the target instruction sequence when latency is important.

## Staff-level takeaway
Bit-count operations are dominated by their **zero-input and width contracts**. Establish those first, then select the implementation that best matches portability, latency, and target instruction support.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
