# Static analyzers

## Definition
**Static analyzers** examine source or intermediate representations without executing the program to identify likely defects, violated coding rules, dataflow problems, portability hazards, and architectural patterns. They complement compiler warnings, testing, sanitizers, and code review.

## Scope and boundaries
Static analysis can reason about paths that tests never execute, but it relies on assumptions and approximations. Results may include false positives and false negatives. A tool's findings are only meaningful when the project supplies the correct build configuration, headers, macros, compiler model, and suppression policy.

## Mechanism and language rules
Analyzers may model:
- control and data flow;
- nullability and initialization;
- range and integer behavior;
- aliasing and lifetime;
- resource ownership;
- concurrency;
- API contracts;
- coding standards such as MISRA-C or CERT C.

For example, a path-sensitive analyzer may detect that an error return is ignored on one branch even though tests cover only the success path.

## Embedded implications
Static analysis is valuable for firmware because many defects are difficult to reproduce on hardware: unchecked register values, invalid state transitions, buffer bounds, integer narrowing, resource leaks, ISR misuse, and API contract violations. It is particularly useful before integration, when target execution is expensive.

The analyzer must understand target types and ABI assumptions. A host-oriented analysis can miss defects involving 16/32-bit widths, address spaces, compiler extensions, or special memory qualifiers.

## Edge cases and failure modes
- Running analysis without the production compile configuration.
- Ignoring findings because the tool reports too much noise.
- Treating one tool as complete coverage.
- Suppressing a finding without documenting the violated assumption.
- Failing to re-run analysis after compiler or SDK changes.

## Verification / debugging
Use a representative compilation database. Categorize findings by severity and defect class. Validate important findings with a minimal reproducer or code inspection. Track tool/version/configuration and compare results between revisions.

## Performance, memory, timing and power
Static analysis runs outside the target and has no firmware runtime cost. Its indirect value is preventing defects that can create performance or resource failures. For large repositories, incremental analysis and changed-code gates can reduce CI cost.

## Staff-level takeaway
Static analysis is an **evidence-producing engineering process**, not a checkbox. Configure it to model the real target, prioritize high-consequence defects, and combine multiple analysis techniques rather than chasing a single tool's score.