# Sanitizer triage

> Canonical C topic note — chapter 40.

## Definition
Sanitizer triage is the disciplined process of turning an instrumentation report into a root-cause defect, fix, and regression test.

## Mechanism and language rules
Start with the first meaningful report, not the final cascade. Identify operation, object lifetime, bounds, types, thread context, and the contract violated. Distinguish primary memory corruption from secondary crashes caused by the corrupted state.

## Embedded implications
For firmware, map host findings back to target memory models and then test hardware-specific boundaries separately. A host sanitizer finding in parser code may be directly applicable; a finding involving MMIO semantics requires target-aware validation.

## Edge cases and failure modes
- Fixing the symptom rather than the ownership/bounds defect.
- Ignoring the first report because a later crash looks more obvious.
- Suppressing flaky failures instead of making the test deterministic.
- Failing to add a regression case.

## Verification / debugging
Preserve the crashing input, sanitizer configuration, stack trace, compiler version, and relevant build flags. Minimize the case, fix the root contract violation, rerun all relevant sanitizers, and add the input to regression coverage.

## Staff-level takeaway
Triage closes the loop between dynamic evidence and engineering change. A sanitizer is valuable only when reports reliably become fixes and durable tests.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
