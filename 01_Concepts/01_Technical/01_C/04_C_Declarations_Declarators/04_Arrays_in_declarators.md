# Arrays in declarators

## Core idea
An array declarator specifies an array type. In declarations, the bound contributes to the type and object size where the language context requires it; in function parameter declarations, array syntax is adjusted to pointer form rather than declaring an array parameter object.

## Embedded consequences
Array bounds directly affect RAM/flash layout, stack use, DMA buffer sizing, and ABI-facing data structures. Variable-length arrays add runtime sizing and stack implications and should be reviewed separately from fixed-size objects.

## Common traps
- Confusing an array object with a pointer to its first element.
- Forgetting parameter adjustment in function declarations.
- Using an array bound derived from an unchecked runtime value.
- Assuming `sizeof` on a parameter written with array syntax yields the original array size.

## Verification
Use `sizeof` carefully at the object boundary, enable warnings for suspicious array parameters, and inspect stack usage for automatic arrays. For externally visible structures, verify layout with static assertions and target ABI documentation.

## Staff-level takeaway
Array syntax is both type information and a resource decision. Review bounds, lifetime, parameter adjustment, and placement together.
