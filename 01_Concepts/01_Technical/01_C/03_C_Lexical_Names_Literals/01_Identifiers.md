# Identifiers and identifier formation

## Core idea
An identifier names a program entity such as an object, function, typedef name, structure/union/enum tag, or enumeration constant. Identifier spelling matters at translation time; what an identifier denotes depends on scope, namespace, linkage, and declaration context.

## Lexical rule versus semantic rule
First ask whether the character sequence is a valid identifier under the active C implementation and source character set. Then ask what declaration it refers to. A valid spelling can still be invalid in context because of scope, redeclaration constraints, or reserved-name rules.

## Embedded consequences
Identifier names often become part of linker symbols, map files, debugger views, trace data, generated headers, and ABI-facing interfaces. Keep public symbols stable when binary compatibility matters. Do not assume the spelling used in C source is identical to the final symbol emitted by the toolchain; assembler/linker naming conventions can transform or decorate it.

## Common traps
- Assuming all Unicode-looking names are portable across compilers.
- Confusing an identifier with a string literal containing the same text.
- Reusing a name across scopes and then debugging the wrong declaration.
- Using implementation-reserved names for application APIs or macros.

## Verification
Use compiler diagnostics for redeclarations and scope errors, inspect preprocessor output when macros affect names, and inspect symbol tables/map files when an identifier crosses a binary boundary.

## Staff-level takeaway
Treat naming as part of interface design: lexical validity is only the first gate; namespace ownership, ABI exposure, generated-code stability, and portability determine whether a name is actually safe.
