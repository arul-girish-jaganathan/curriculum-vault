# Compiler flags

## Definition
**Compiler flags** are command-line options that control language mode, target architecture, optimization, diagnostics, ABI, code generation, preprocessing, debug information, and other compiler behavior. In embedded C, the complete flag set is effectively part of the source-level and binary-level build contract.

## Scope and boundaries
Flags are implementation-specific. The same spelling can have different meaning across GCC, Clang, IAR, Arm Compiler, MSVC, and vendor toolchains. Some flags alter ISO C semantics by enabling extensions or changing assumptions; others select target ABI or optimization only.

## Mechanism and language rules
Separate flags conceptually into:
- **language:** `-std=...`, extensions, feature-test macros;
- **warnings:** diagnostic policy;
- **optimization:** `-O...`, LTO, size/speed tuning;
- **target:** CPU, ISA, floating-point ABI;
- **code generation:** sections, PIC, alignment, calling convention;
- **debug:** DWARF and instrumentation;
- **link:** libraries, linker script, garbage collection.

A compilation database should preserve the exact command used for every translation unit.

## Embedded implications
Flags can change structure packing, enum representation, floating-point calling conventions, atomic instruction selection, exception/unwind support, startup/runtime requirements, and generated instruction sets. Mixing incompatible flags between object files can create subtle ABI failures even when compilation succeeds.

Avoid global “magic” flags whose purpose is undocumented. Product builds should distinguish intentional configuration from accidental environment inheritance.

## Edge cases and failure modes
- `-fshort-enums` or packing changes structure/ABI expectations.
- CPU flags enable instructions unsupported by deployed silicon.
- Floating-point ABI mismatch occurs across libraries.
- Optimization or LTO changes timing and debug behavior.
- A warning suppression hides a new defect after a compiler upgrade.
- Host and target flags leak into one another.

## Verification / debugging
Version-control build configuration and generate a compilation database. Print compiler and linker commands in CI. Diff flags between release configurations. For ABI-sensitive changes, inspect ELF attributes, symbol interfaces, structure sizes, and target execution.

## Performance, memory, timing and power
Optimization flags directly affect code size and execution. Target flags determine instruction availability and hardware-unit use. Debug/instrumentation flags can distort timing and memory. Measure the exact release configuration.

## Staff-level takeaway
Flags are not incidental command-line decoration. Treat them as versioned engineering inputs with owners, rationale, compatibility constraints, and tests.