# Parsing and Semantic Analysis

Parsing determines whether the token stream conforms to C grammar; semantic analysis determines whether the resulting constructs satisfy the language's type and constraint rules. These are compiler concepts rather than runtime phases.

## Parsing
The parser builds an internal representation corresponding to declarations, expressions, statements and other grammar constructs. Precedence and associativity affect how expressions are grouped. A syntactically valid expression can still be semantically invalid.

## Semantic analysis
Type compatibility, required conversions, constraints on declarations and expressions, object/function rules, and many diagnostics are established here. The compiler must diagnose violations for which the standard requires a diagnostic, but diagnostic wording and recovery behavior are implementation-specific.

## Why this matters in firmware
A warning-free build is not proof of semantic correctness. The compiler can accept code that is well-formed but logically wrong, violates a hardware protocol, races with an ISR, accesses a peripheral incorrectly, or depends on an invalid assumption outside the language model.

## Optimization boundary
After semantic analysis, the compiler is free to transform a conforming program while preserving the observable behavior required by the language and implementation environment. Undefined behavior removes constraints and can therefore permit aggressive transformations.

## Debugging workflow
Classify the first diagnostic rather than the last cascade. Reduce the translation unit if necessary, inspect preprocessing output, verify the selected standard mode, and then inspect types and declarations. Do not “fix” diagnostics by casts until the intended type relationship is understood.

## Staff-level view
Compiler diagnostics are design feedback. A mature codebase treats warning policy, static analysis and build configuration as part of its language contract and avoids suppressing diagnostics without a documented reason.

## Related
- [[03_Tokenization]]
- [[05_Constant_expressions]]
- [[07_Assembly_inspection]]
- [[39_C_Diagnostics_Static_Analysis]]
