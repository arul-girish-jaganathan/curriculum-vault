# UndefinedBehaviorSanitizer

## Definition
**UndefinedBehaviorSanitizer (UBSan)** instruments selected operations so runtime execution can detect classes of behavior that the C language does not define, such as certain signed overflow, invalid shifts, misaligned accesses, invalid enum values, or out-of-range conversions depending on enabled checks and compiler support.

## Scope and boundaries
UBSan is compiler- and check-specific. It cannot detect every form of undefined behavior, and some checks may recover while others terminate. A clean run means only that exercised, instrumented paths did not trigger the selected checks.

## Mechanism and language rules
Instrumentation is inserted around operations whose preconditions can be checked at runtime:

```c
int shift(int x, unsigned n)
{
    return x << n;
}
```

Depending on enabled checks and type/target rules, an invalid shift count or other undefined operation can produce a diagnostic instead of silently continuing.

## Embedded implications
UBSan is especially useful in host builds for arithmetic-heavy code, parsers, protocol lengths, state machines, and low-level libraries. Target support varies because the runtime may require substantial code and memory. MCU-specific tests are still needed for hardware faults and architecture behavior outside the sanitizer model.

## Edge cases and failure modes
- Assuming one UBSan mode covers every undefined behavior.
- Suppressing a finding because the value “cannot happen” without proving the invariant.
- Relying on recovery mode in safety-critical tests when termination is required.
- Sanitizer runtime changes timing and memory layout.
- Target-specific integer widths differ from the host test environment.

## Verification / debugging
Enable relevant checks deliberately, preserve stack traces, and make sanitizer failures CI-visible. Use targeted tests for boundary values: zero/maximum shift counts, signed limits, alignment boundaries, enum ranges, and conversion extremes. Compare host types with target types.

## Performance, memory, timing and power
Instrumentation adds runtime checks and can substantially increase binary size. It is therefore primarily a validation configuration. The overhead can also expose timing-sensitive assumptions that should be tested separately.

## Staff-level takeaway
Use UBSan to turn hidden language-level assumptions into observable failures. Pair it with static analysis because dynamic sanitization can only detect behavior on executed paths.