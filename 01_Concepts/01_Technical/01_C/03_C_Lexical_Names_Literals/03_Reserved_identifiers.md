# Reserved identifiers and namespace hazards

## Core idea
C reserves classes of identifier spellings for the implementation and standard library. Reserving names protects library and implementation evolution; application code that violates those reservations can lose portability or collide with future headers, builtins, or implementation details.

## What to watch
Do not treat reservation as a cosmetic naming convention. The exact rule depends on where the identifier appears: file scope, external linkage, use in a standard header, or special implementation namespaces. A safe project convention should avoid implementation namespaces entirely unless a documented compiler extension requires them.

## Embedded consequences
Vendor SDKs frequently expose implementation-specific macros, attributes, intrinsics, and linker symbols. Keep those names isolated behind project-owned wrappers so application code does not accidentally become dependent on a vendor namespace.

## Failure modes
- A local macro collides with a standard-library macro or future header.
- A global symbol collides with a runtime or startup symbol.
- A third-party header changes behavior after a compiler/libc upgrade.
- A supposedly private name becomes externally visible through the linker.

## Verification
Run builds with stricter warnings and multiple libc/toolchain versions where practical. Search for reserved-prefix patterns during code review and static analysis.

## Staff-level takeaway
Namespace hygiene is compatibility engineering. Reserve your own project namespace just as deliberately as you avoid the implementation's namespace.
