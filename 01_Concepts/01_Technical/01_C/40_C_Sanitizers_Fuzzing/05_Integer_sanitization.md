# Integer sanitization

## Definition
**Integer sanitization** instruments integer operations and conversions to detect selected arithmetic errors at runtime, such as signed overflow, invalid shifts, or suspicious unsigned behavior depending on the compiler's sanitizer options. It targets one of the most common sources of C security and reliability defects.

## Scope and boundaries
C has defined, implementation-defined, and undefined integer behaviors. Sanitizers cover only selected operations and exercised paths. Unsigned arithmetic intentionally wraps modulo its range, so not every wrap is an error.

## Mechanism and language rules
A sanitizer can turn an operation such as:

```c
int n = INT_MAX;
int x = n + 1; /* signed overflow: undefined behavior */
```

into a runtime diagnostic under the relevant instrumentation. Shift counts, signedness, and conversion checks require separate analysis because their C rules differ.

## Embedded implications
Integer defects are common in packet lengths, buffer indexing, timer arithmetic, register fields, ADC scaling, fixed-point calculations, and size conversions. Host sanitizer builds can exercise these paths cheaply before target execution.

The target's integer widths and compiler options must be represented in tests. A 64-bit host may hide a defect that appears with 32-bit `size_t` or another target data model.

## Edge cases and failure modes
- Assuming unsigned wrap is automatically undefined.
- Checking `a + b` after the overflow already occurred instead of before it.
- Converting a large unsigned value to signed and assuming truncation is harmless.
- Shift count equals or exceeds the width.
- Host and target integer widths differ.

## Verification / debugging
Test around `0`, minimum, maximum, and one-past-boundary values. Run sanitizer-enabled unit and fuzz tests. Pair dynamic checks with static range analysis and explicit checked-arithmetic helpers where values cross trust boundaries.

## Performance, memory, timing and power
Instrumentation adds checks and can significantly slow execution or increase image size. Use it in validation builds rather than production unless the target explicitly supports the required overhead and policy.

## Staff-level takeaway
Integer sanitization is most valuable when connected to **range contracts**. Define valid ranges at API boundaries, validate before arithmetic, and use sanitizer evidence to find paths where those contracts are violated.