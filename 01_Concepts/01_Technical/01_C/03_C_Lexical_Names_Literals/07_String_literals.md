# String literals and storage/concatenation rules

## Core idea
A string literal is a sequence of characters followed by a terminating null character. Adjacent string literals are concatenated during translation, while the resulting literal object has implementation-defined storage characteristics beyond the language guarantees that matter for modification and identity.

## Critical rule
A string literal is not a writable character array. Attempting to modify its characters produces undefined behavior. In a firmware API, use `const char *` when passing a literal to a read-only consumer.

## Embedded consequences
Literals normally consume image space and may be placed in read-only flash/ROM, but the exact placement and access mechanism depend on the implementation and memory model. Large diagnostic strings can materially affect firmware image size. Linker garbage collection and section placement can change whether unused strings remain in the image.

## Failure modes
- Passing literals to APIs that write through `char *`.
- Assuming two identical literals have distinct or identical addresses.
- Forgetting the terminating null character when computing storage requirements.
- Building RAM-heavy lookup tables from unnecessarily mutable character arrays.

## Verification
Inspect compiler diagnostics for incompatible qualifiers, use read-only API signatures, and inspect linker maps when flash/RAM usage matters.

## Staff-level takeaway
Treat literal mutability, storage placement, and encoding as explicit API and memory-budget decisions rather than incidental syntax.
