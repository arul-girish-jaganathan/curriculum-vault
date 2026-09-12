# MISRA-C checking

> Canonical C topic note — chapter 39.

## Definition
MISRA C is a coding-guideline framework for safer, more analyzable C, especially in embedded and safety-related systems. It is not part of ISO C and compliance is a project/process claim supported by a selected edition, tool configuration, deviations, and evidence.

## Mechanism and language rules
MISRA rules address areas such as conversions, essential types, control flow, declarations, macros, pointer use, library usage, and undefined/unspecified behavior. Tools automate many checks but cannot replace engineering judgment or documented deviations.

## Embedded implications
MISRA checking can reduce defect-prone language freedom in drivers and safety logic. Rules should be applied with knowledge of the compiler, target, generated code, hardware abstraction, and project safety case.

## Edge cases and failure modes
- Calling “MISRA compliant” without declaring edition/configuration.
- Suppressing a rule instead of documenting a justified deviation.
- Applying generic rules to generated/vendor code without a boundary.
- Confusing guideline compliance with functional correctness.

## Verification / debugging
Version the checker configuration and deviation records. Review critical violations against the actual C rule and project requirement. Combine MISRA results with compiler warnings, static analysis, tests, and code review.

## Staff-level takeaway
MISRA is most effective as a controlled engineering system: defined scope, tool qualification/validation where required, justified deviations, measurable gates, and traceable ownership.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
