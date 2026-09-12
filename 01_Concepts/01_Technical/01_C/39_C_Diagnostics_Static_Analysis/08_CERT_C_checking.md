# CERT C checking

## Definition
**CERT C checking** applies secure-coding rules intended to reduce vulnerabilities caused by C's low-level memory, integer, string, and control-flow semantics. It complements compiler diagnostics, static analysis, testing, and security review.

## Scope and boundaries
CERT C is guidance, not ISO C syntax. Rules may address undefined behavior, integer handling, memory management, strings, concurrency, APIs, and error handling. Exact rule applicability and tool coverage depend on the selected edition and analyzer.

## Mechanism and language rules
Typical concerns include avoiding out-of-bounds accesses, validating integer conversions, handling allocation failures, preventing use-after-free, and avoiding unsafe string interfaces. A rule should be traced back to a concrete C mechanism and security consequence rather than followed mechanically.

## Embedded implications
Embedded products often have long lifetimes and limited recovery mechanisms, so a memory-safety defect can become a denial-of-service, code-execution, or persistent-corruption issue. CERT-style checks are valuable around protocol parsing, external inputs, flash metadata, bootloaders, and communication stacks.

Resource exhaustion also matters: a parser that accepts attacker-controlled lengths can consume CPU/RAM even if it never accesses memory out of bounds.

## Edge cases and failure modes
- Applying a secure-coding rule without understanding target-specific constraints.
- Assuming a checked integer conversion is safe without validating the accepted range.
- Treating a static-analysis finding as proof of exploitability without threat modeling.
- Suppressing security findings because the code is “internal.”
- Focusing on memory safety while ignoring concurrency and denial-of-service paths.

## Verification / debugging
Map selected CERT rules to the project's threat model and test strategy. Use static analysis for broad coverage, sanitizers for executable validation, fuzzing for parser behavior, and code review for architectural assumptions. Record justified deviations and residual risk.

## Performance, memory, timing and power
Security checks can add branches and validation work. Measure them in hot paths, but do not remove a security invariant merely for micro-optimization. In many cases early validation reduces downstream work.

## Staff-level takeaway
CERT C is most effective when connected to **threat models and concrete defect classes**. Security rules should lead to measurable controls, tests, and residual-risk decisions—not a compliance score alone.