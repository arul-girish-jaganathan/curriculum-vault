# Declaration specifiers

## Core idea
Declaration specifiers describe major properties of a declaration: type information and, where applicable, storage-class, function, alignment, qualifier, or other standard specifiers. The declarator then determines the declared entity's shape.

## Reasoning model
Do not read a declaration left-to-right as if it were prose. Separate the specifier sequence from the declarator. Then determine the base type and the entity described by the declarator, followed by scope, storage duration, linkage, and any constraints imposed by the declaration context.

## Embedded consequences
Specifiers can alter object placement, mutability, access semantics, calling interfaces, and generated code. `static`, `extern`, `const`, `_Atomic`, alignment specifications, and function-related specifiers can become ABI or linker-visible decisions depending on context.

## Failure modes
- Confusing storage class with storage duration.
- Assuming `const` alone guarantees hardware read-only placement.
- Combining specifiers that are individually valid but invalid together.
- Treating compiler extensions as ISO C guarantees.

## Verification
Use compiler diagnostics, inspect generated symbols and map files, and compare declarations across translation units. For ABI-facing declarations, ensure every declaration is compatible and comes from a common header.

## Staff-level takeaway
A declaration is a contract. Review both its language legality and the concrete storage, linkage, ABI, and toolchain consequences on the target.
