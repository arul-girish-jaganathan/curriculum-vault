# Shifts

> Canonical C topic note — Chapter 43. Shift operators move the value's bits left or right. Correct reasoning requires the promoted operand type, shift count, signedness, and destination width.

## Definition
`x << n` shifts bits toward higher positions; `x >> n` shifts toward lower positions. The right operand must be nonnegative and less than the width of the promoted left operand. Violating the count constraint is undefined behavior.

## Mechanism and language rules
The operands undergo integer promotions. For unsigned operands, left shifts are defined modulo the relevant range subject to the shift-count constraint; right shift of unsigned values is a logical shift. For signed operands, especially negative values and left shifts, the rules are more restrictive. Right shift of a negative signed value is implementation-defined.

### What to reason about
- What is the promoted width?
- Is the shift count provably within range?
- Is the operand signed or unsigned?
- Is the shifted value intended as a mathematical multiply/divide or bit manipulation?
- Does the result need a fixed-width representation?

Prefer unsigned fixed-width operands for protocol/register manipulation.

## Embedded implications
Shifts implement field extraction, scaling, register programming, CRC logic, and bit packing. A compiler may turn constant shifts into efficient instructions, but a variable shift can have different latency across cores.

### Firmware review angle
Use `UINT32_C(1) << bit` only when `bit < 32` is guaranteed. Avoid macros that evaluate a shift expression without validating its width. On narrow MCUs, explicitly sized types prevent accidental promotion surprises.

## Edge cases and failure modes
- `1 << 31` can be problematic because `1` is an `int`.
- `x << 32` on a 32-bit promoted operand is undefined.
- Right shifting a negative signed value is implementation-defined.
- Left shifting a signed value into an unrepresentable result can be undefined.
- Applying a shift before masking can invoke UB even if the final masked result would appear harmless.

## Example pattern
```c
uint32_t make_mask(unsigned bit)
{
    return (bit < 32U) ? (UINT32_C(1) << bit) : 0U;
}
```
The explicit bound makes the shift count valid.

## Verification / debugging
Test counts 0, 1, width-1, width, and values around signed boundaries. Enable compiler shift warnings and run UBSan on host builds where applicable. Inspect generated instructions when shift timing matters.

## Staff-level takeaway
Never reason about a shift as “just moving bits.” First establish **promoted type, width, signedness, and valid count**; only then reason about the resulting bit pattern and hardware effect.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
