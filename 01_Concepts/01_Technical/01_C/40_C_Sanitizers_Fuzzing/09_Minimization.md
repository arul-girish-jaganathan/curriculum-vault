# Minimization

## Definition
**Minimization** reduces a failing or interesting fuzz input to the smallest input that still reproduces the same behavior or coverage property. A minimized reproducer is easier to debug, review, store, and convert into a regression test.

## Scope and boundaries
Minimization is only meaningful relative to a predicate: crash, sanitizer report, timeout, coverage feature, or other observable condition. Removing bytes can change parsing state, so the smallest file is not necessarily the simplest semantic test case.

## Mechanism and language rules
A conceptual minimization loop is:

```text
input -> remove/change part -> execute predicate -> keep change if predicate survives
```

Fuzzing frameworks often automate this process. For structured formats, grammar-aware reduction may outperform byte-level deletion.

## Embedded implications
A minimized protocol packet can expose exactly which header, length, or state transition triggers a firmware defect. For bootloaders, a minimized malformed image can make root-cause analysis and security review substantially easier.

## Edge cases and failure modes
- Minimizer changes a timeout into a normal execution.
- Crash depends on environmental state not represented in the input.
- Nondeterministic bugs disappear during minimization.
- A byte-level minimizer destroys required checksums or framing.
- The reduced case no longer represents the security scenario that matters.

## Verification / debugging
Re-run the minimized input repeatedly and under the same sanitizer/toolchain configuration. Preserve the original failing input as evidence. Convert the minimized reproducer into a deterministic regression test and document the original discovery context.

## Performance, memory, timing and power
Smaller inputs generally execute faster and are easier to store. Minimization itself may require many executions, but the long-term payoff is faster regression testing and simpler diagnosis.

## Staff-level takeaway
Minimization turns a large fuzzing artifact into a **human-scale defect specification**. Preserve both the minimized reproducer and enough provenance to understand what was originally discovered.