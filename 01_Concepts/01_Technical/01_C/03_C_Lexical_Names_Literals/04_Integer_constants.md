# Integer constants and suffix/type selection

## Core idea
An integer constant is interpreted during translation according to its spelling, base, suffix, and the set of candidate integer types permitted by the selected C version. The type of a literal therefore cannot be inferred from the number alone.

## Reasoning model
For every integer literal ask: decimal, octal, or hexadecimal/binary form; which suffix is present; which candidate type is selected; and what happens when the value is outside the range of the intended target type. `0` prefixes are especially dangerous because a leading zero can select octal interpretation.

## Embedded consequences
Literal types affect arithmetic width, signedness, register access expressions, constant folding, array sizes, enumeration-related code, and generated machine instructions. On a 16-bit, 32-bit, or 64-bit target, relying on `int` width without checking the ABI can change correctness or diagnostics.

## Example
```c
uint32_t mask = 0x80000000u;
int timeout = 1000;
```
Use suffixes when the intended unsigned or wide type is part of the contract; still verify conversions at the assignment boundary.

## Failure modes
- Octal literals accidentally encode a different value.
- A signed literal participates in an expression with unsigned operands.
- A literal silently has a narrower type than expected.
- A constant that fits one target's `long` does not fit another's.

## Verification
Compile with signedness and conversion warnings enabled. Use `<stdint.h>` types for data contracts, but remember that a literal's own type is chosen before the assignment conversion.

## Staff-level takeaway
Review integer literals as typed operands, not decorative numbers. Literal type can change comparison, promotion, overflow behavior, code generation, and portability.
