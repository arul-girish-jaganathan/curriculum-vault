# Constant Expressions

A constant expression is an expression restricted by C's rules so that its value can be determined in contexts requiring compile-time evaluation. Constant-expression rules are stricter than the informal idea that “the compiler can probably calculate it.”

## Where they matter
They appear in array bounds in contexts where constant expressions are required, enumerator values, bit-field widths, `_Static_assert` conditions, initializers for objects with static storage where applicable, and other compile-time constraints.

## Embedded value
Compile-time constants can move validation from runtime to build time. Register masks, buffer sizes, protocol field widths and table dimensions are safer when invalid relationships become compilation failures.

## Do not confuse with `const`
A `const` object is an object that cannot be modified through that lvalue; it is not automatically an integer constant expression. Storage, linkage and addressability still matter. Similarly, compiler constant folding is an optimization and does not redefine the language's constant-expression rules.

## Debugging
When an expression is rejected in a constant-expression context, identify the exact language category required and inspect every operand. A value being known to a human or folded by an optimizer does not mean the syntax satisfies the required constraint.

## Staff-level view
Prefer compile-time invariants for properties that are structural: array capacity, configuration ranges, type sizes and protocol constants. Runtime checks remain necessary for values arriving from hardware, communication channels or external configuration.

## Related
- [[04_Parsing_and_semantic_analysis]]
- [[08_Implementation_defined_behavior]]
- [[64_C_Designated_Initialization]]
- [[56_C23_Bit_Utilities_Checked_Arithmetic]]
