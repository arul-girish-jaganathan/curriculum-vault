# Declarator grammar

## Core idea
C declarators describe an entity's derived type using operators such as `*`, `[]`, and `()`. Parentheses alter how those operators bind. Mastery comes from parsing the declarator as syntax rather than memorizing ad hoc examples.

## Mechanical method
Start at the identifier when present. Move outward, respecting parentheses, and explain each suffix/prefix as it is encountered. For example, `int *f[4]` declares an array of four pointers to `int`, while `int (*f)[4]` declares a pointer to an array of four `int`.

## Embedded consequences
This distinction directly affects driver tables, callback registries, DMA descriptors, memory-mapped data structures, and APIs. A declaration that is syntactically valid can still describe an entirely different memory layout or calling interface from what the designer intended.

## Failure modes
- Missing parentheses around pointer-to-array or pointer-to-function types.
- Reading declarations by English intuition instead of grammar.
- Assuming typedefs make declarators semantically simpler when they can hide pointer/array structure.

## Verification
Reduce complex declarations to small equivalent examples, let the compiler print warnings/type diagnostics, and use IDE AST/type inspection where available. Add compile-time type checks for critical interfaces.

## Staff-level takeaway
For difficult declarations, prove the type mechanically before reviewing the implementation. This is faster and safer than relying on visual familiarity.
