# Target triples

## Definition
A **target triple** is a compact identifier describing the platform a compiler toolchain targets, commonly using forms such as `architecture-vendor-system` with optional environment/ABI information. It helps select instruction set, object format, runtime assumptions, and compatible libraries.

## Scope and boundaries
Triple syntax and exact component meanings are toolchain-specific. Do not infer a complete ABI merely from a string such as `arm-none-eabi`; CPU features, floating-point options, ABI flags, libc, and compiler version can still matter.

## Mechanism and language rules
A target selection influences predefined macros, instruction selection, object format, assembler syntax, linker behavior, and library search paths. Related flags may refine the target:

```text
architecture -> CPU/features -> ABI -> sysroot/runtime -> linker
```

For example, an ARM bare-metal toolchain and an ARM Linux toolchain can target similar instruction sets while requiring completely different startup and runtime environments.

## Embedded implications
Target triples are particularly important in CI, package management, build systems, and multi-target firmware. A project may build Cortex-M firmware, a host simulator, and a Linux utility from the same repository. Each must have an explicit toolchain configuration rather than inheriting whichever compiler happens to be first on `PATH`.

CPU feature flags can alter instruction availability, floating-point calling conventions, and compatibility with deployed silicon. A binary built for a newer instruction extension may fail immediately on an older MCU.

## Edge cases and failure modes
- Correct architecture but wrong operating-system/runtime environment.
- Correct CPU family but wrong floating-point ABI.
- Confusing architecture name with exact microarchitecture/features.
- Using a target triple as the only reproducibility identifier.
- Host tools accidentally inheriting target compiler environment variables.

## Verification / debugging
Record the target triple plus CPU, feature, ABI, sysroot, compiler, assembler, and linker versions. Inspect ELF headers and attributes to verify architecture and ABI. In CI, print the complete toolchain configuration and reject unexpected triples.

## Performance, memory, timing and power
Target selection changes instruction encoding, available hardware operations, floating-point support, and runtime libraries, all of which affect code size, execution time, and energy.

## Staff-level takeaway
Use the target triple as the **starting coordinate**, not the entire platform contract. Reproducible embedded builds require the triple plus explicit CPU features, ABI, runtime, linker, and tool versions.