# MISRA-C checking

## Definition
**MISRA C checking** applies the MISRA C coding guidelines as a systematic set of rules for safer, more predictable C in embedded systems. MISRA is not the C language standard; it constrains how C is used to reduce ambiguity, undefined behavior, portability risk, and difficult-to-analyze constructs.

## Scope and boundaries
MISRA versions and rule classifications differ, and project compliance requires a defined edition, tool configuration, deviation process, and interpretation. “MISRA compliant” should never mean merely “the analyzer emitted no warnings.”

## Mechanism and language rules
Rules address areas such as implicit conversions, essential types, control flow, pointer use, initialization, declarations, macros, side effects, and library use. Some rules are decidable by syntax; others require semantic analysis and project context.

A robust workflow is:

```text
MISRA rules -> analyzer configuration -> findings -> deviations -> evidence
```

## Embedded implications
MISRA is especially useful where firmware must be predictable, reviewable, and portable across compilers. Essential-type rules can expose integer conversion hazards; pointer-related rules can expose unsafe casts; control-flow rules can improve analyzability.

The rules do not replace hardware reviews. A codebase can be MISRA-clean while still using the wrong register width, violating a DMA contract, or missing a required memory barrier.

## Edge cases and failure modes
- Treating a rule as an absolute law without considering its classification/deviation process.
- Suppressing a rule globally instead of documenting a justified deviation.
- Using a cast merely to silence an essential-type warning.
- Applying generic rules to generated code without an ownership strategy.
- Confusing static-analysis compliance with functional correctness.

## Verification / debugging
Pin the MISRA edition and analyzer version. Maintain a deviation record containing rule, location, rationale, risk assessment, and approval. Verify that analysis uses production compiler defines and include paths. Track findings by rule and module over time.

## Performance, memory, timing and power
MISRA rules have no direct runtime cost. They can, however, encourage explicit conversions and simpler control flow that improve portability and analysis. Compliance should not justify inefficient abstractions without measurement.

## Staff-level takeaway
MISRA is best viewed as a **risk-control framework for C usage**. Combine automated checking, disciplined deviations, code review, testing, and target-specific engineering evidence.