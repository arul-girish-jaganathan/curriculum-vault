# UndefinedBehaviorSanitizer

> Canonical C topic note — chapter 40.

## Definition
UndefinedBehaviorSanitizer (UBSan) instruments selected operations to diagnose undefined or invalid behavior such as signed overflow, invalid shifts, misaligned accesses, and certain bounds/type violations, depending on compiler and enabled checks.

## Mechanism and language rules
UBSan checks are implementation features layered onto C semantics. Some modes recover and continue; others trap. A report identifies the operation and often the source location. Not every form of UB is dynamically detectable.

## Embedded implications
UBSan is valuable on host builds for firmware algorithms, parsers, arithmetic, and state machines. On-target instrumentation may be too expensive or unavailable, so use a representative host harness and supplement it with target tests.

## Edge cases and failure modes
- Assuming one sanitizer configuration covers all UB.
- Continuing after a recovered error and creating misleading secondary failures.
- Relying on host integer widths or alignment.
- Disabling checks that reveal a fundamental contract defect.

## Verification / debugging
Enable relevant checks incrementally, reproduce the smallest failure, and fix the violated contract. Test boundary arithmetic, shifts, enum values, pointer alignment, and conversions explicitly.

## Staff-level takeaway
UBSan turns many optimizer-sensitive assumptions into actionable failures. It is especially effective before interpreting release-only behavior as a compiler problem.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
