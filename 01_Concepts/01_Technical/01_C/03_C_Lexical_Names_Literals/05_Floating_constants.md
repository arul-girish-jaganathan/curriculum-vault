# Floating constants and translation-time interpretation

## Core idea
A floating constant denotes a floating value and has a type selected from `float`, `double`, or `long double` according to its suffix and C rules. The source spelling does not guarantee a particular runtime representation or exact value on every target.

## Key distinctions
Separate decimal/hexadecimal source notation, suffix-driven type, constant evaluation, rounding, floating environment, and target representation. A compiler can fold expressions, but the resulting behavior must still respect the applicable language and implementation rules.

## Embedded consequences
Floating support may be expensive or absent on small MCUs. A source literal such as `0.1` can create floating operations, constant tables, conversions, or library calls. This affects flash size, latency, stack use, determinism, and power. On targets without hardware FP, inspect generated code rather than assuming a simple arithmetic expression is cheap.

## Failure modes
- Accidental `double` promotion increases code size.
- Binary representation makes decimal equality tests unreliable.
- Literal suffixes differ from the intended storage type.
- Compile-time folding hides the runtime cost of later conversions.

## Verification
Use compiler warnings, inspect generated assembly/map files for floating helper calls, and test numerical boundaries on the target toolchain. Where exact representation matters, document the required format rather than assuming it from the C type name.

## Staff-level takeaway
In embedded systems, floating literals are both language operands and potential resource consumers. Review numerical intent and generated implementation together.
