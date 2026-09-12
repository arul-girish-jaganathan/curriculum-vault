# Compiler selection

## Definition
**Compiler selection** is the engineering decision of choosing the compiler, version, C dialect, runtime libraries, assembler, linker, debugger, and supporting tools that together produce the firmware artifact. The compiler is part of the product toolchain and therefore part of the system's reproducibility, ABI, safety, performance, and maintenance contract.

## Scope and boundaries
A compiler is not evaluated only by whether it accepts the source. Selection should consider ISO C conformance, target support, ABI compatibility, diagnostics, optimization quality, debug information, static-analysis integration, license/support constraints, library behavior, long-term availability, and known defects.

## Mechanism and language rules
Compiler options can select language modes, target architecture, floating-point ABI, optimization, section generation, warnings, extensions, and runtime assumptions. A change such as `-mcpu`, `-mfloat-abi`, or the C language standard can alter generated code and ABI. Never treat flags as interchangeable between compiler families.

A strong selection record includes:
- exact compiler version and build identity;
- target CPU/architecture and ABI;
- language standard and extensions;
- optimization/debug flags;
- libc/startup/runtime choice;
- assembler/linker versions;
- known deviations and qualification evidence.

## Embedded implications
Compiler choice affects interrupt entry, instruction selection, floating-point support, code size, startup code, exception handling, stack alignment, atomic operations, and peripheral access conventions. A compiler upgrade can change timing without changing source semantics. Safety-critical products may require compiler qualification evidence or a documented justification for the selected version.

## Edge cases and failure modes
- Mixing object files built for incompatible ABIs.
- Accidentally using a host compiler instead of the cross compiler.
- Changing compiler version without rebuilding all dependencies.
- Enabling extensions that another compiler interprets differently.
- Assuming identical optimization flags imply identical generated code.
- Updating the compiler without rerunning timing, size, static analysis, and regression suites.

## Verification / debugging
Capture `--version`, target flags, predefined macros, linker version, and build metadata in CI artifacts. Build a known-good benchmark and compare code size, ABI-sensitive tests, warnings, and target timing. Keep a compiler upgrade checklist and preserve the previous toolchain for bisecting regressions.

## Performance, memory, timing and power
Different compilers and versions can make materially different inlining, register-allocation, loop, and instruction-selection decisions. Evaluate flash/RAM, startup time, interrupt latency, worst-case execution time, and energy on representative hardware.

## Staff-level takeaway
Choose a compiler as an **evidence-backed platform decision**, not personal preference. Freeze and reproduce the toolchain for releases, document its contracts, and make upgrades deliberate, measurable, and reversible.