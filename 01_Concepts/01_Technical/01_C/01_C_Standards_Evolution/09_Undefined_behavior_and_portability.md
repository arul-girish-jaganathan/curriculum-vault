# Undefined Behavior and Portability

Undefined behavior (UB) occurs when the C standard imposes no requirements on the program's behavior for a particular execution. Once UB is reached, reasoning from the apparent source-level operation is no longer valid. This is why compiler optimization can expose bugs that appeared stable at `-O0`.

## Typical embedded sources
Common examples include signed integer overflow, invalid shifts, out-of-bounds access, use-after-lifetime, invalid pointer arithmetic, incompatible aliasing assumptions, and incorrect format or variadic arguments. Some failures corrupt data; others alter control flow or disappear under a debugger.

## Three different categories
Do not mix UB with unspecified behavior or implementation-defined behavior.
- **Undefined:** the standard imposes no requirements.
- **Unspecified:** one of multiple permitted behaviors may occur and the implementation need not document which.
- **Implementation-defined:** the implementation chooses and documents a permitted behavior.

## Why optimization changes symptoms
The compiler is allowed to assume that a conforming program does not execute undefined operations. It can therefore simplify control flow or eliminate checks that would only matter after UB. The resulting binary is not “random”; it is the consequence of compiling outside the language's defined semantic contract.

## Embedded debugging
When a failure disappears with optimization disabled, do not conclude that the optimizer is broken. First investigate UB, data races, lifetime errors, uninitialized data, stack corruption and timing-sensitive hardware interactions. Compare optimized assembly only after the source-level contract is understood.

## Defensive techniques
Use compiler warnings, static analysis, sanitizers on host builds, assertions, fuzzing for parsers, bounded APIs, explicit integer types, and tests around boundary values. Avoid relying on a single runtime symptom as proof of correctness.

## Portability
A program can be portable across multiple implementations only to the extent that it stays within defined language behavior and controls its implementation dependencies. Portability is a property of assumptions and contracts, not just source syntax.

## Staff-level view
The key question during a root-cause review is: “What semantic contract did the code violate, and why did our engineering process fail to prevent it?” Fixing the immediate line is necessary; eliminating the class of defect is the Staff-level outcome.

## Related
- [[08_Implementation_defined_behavior]]
- [[29_C_Behavior_Categories]]
- [[39_C_Diagnostics_Static_Analysis]]
- [[40_C_Sanitizers_Fuzzing]]
