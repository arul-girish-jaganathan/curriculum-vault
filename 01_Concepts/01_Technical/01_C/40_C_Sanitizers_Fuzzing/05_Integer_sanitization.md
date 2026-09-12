# Integer sanitization

> Canonical C topic note — chapter 40.

## Definition
Integer sanitization detects selected arithmetic and conversion hazards such as signed overflow, invalid shifts, and some implicit conversion problems, depending on compiler configuration.

## Mechanism and language rules
Sanitizers instrument operations that have defined preconditions. For example, signed overflow is undefined in C, while unsigned arithmetic wraps modulo the width of the unsigned type. Correct diagnosis requires knowing the actual operand types after integer promotions and conversions.

## Embedded implications
Integer defects commonly occur at packet lengths, register fields, counters, timeouts, array indices, and size calculations. Host sanitizer tests should exercise maximum, minimum, zero, and boundary-crossing values.

## Edge cases and failure modes
- Assuming unsigned wrap is automatically safe.
- Sanitizing after a narrowing conversion instead of validating the range before conversion.
- Missing integer-promotion effects.
- Using sanitizer behavior as the production arithmetic policy.

## Verification / debugging
Test boundary matrices and run sanitizer-enabled builds. Add explicit checked arithmetic at security/safety boundaries where overflow is part of the expected input model.

## Staff-level takeaway
Sanitizers identify suspicious arithmetic; robust APIs define what ranges are legal and how overflow is handled. The latter is the product contract.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
