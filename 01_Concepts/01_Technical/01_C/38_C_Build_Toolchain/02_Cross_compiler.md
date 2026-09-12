# Cross compiler

## Definition
A **cross compiler** runs on one platform (the host/build machine) and produces code for a different platform (the target). Embedded development commonly uses an x86-64 Linux/Windows/macOS host to build ARM, RISC-V, or another MCU architecture.

## Scope and boundaries
Cross compilation separates build, host, and target environments. The compiler's target options determine instruction set, ABI, data model, floating-point conventions, alignment, and calling convention. The host compiler must not accidentally compile target sources merely because the source is valid C on both machines.

## Mechanism and language rules
A typical pipeline is:

```text
host source -> target compiler -> target object -> target linker -> firmware image
```

The compiler can use target-specific headers, builtins, and predefined macros. The linker resolves target addresses using a target linker script. Runtime libraries must also be target-compatible.

Distinguish:
- **build machine:** where tools execute;
- **host:** the environment on which a host-side tool executes;
- **target:** the MCU/system for which the program is produced.

## Embedded implications
Cross compilation is mandatory when the target cannot practically build itself or lacks an operating system/toolchain. It makes sysroot, startup code, libc selection, linker scripts, and target headers critical. A wrong sysroot can silently mix incompatible headers and libraries.

Host tests are valuable, but they do not prove target ABI, alignment, endianness, register access, interrupt behavior, or memory-map correctness.

## Edge cases and failure modes
- Host and target `sizeof` assumptions differ.
- A host library accidentally enters the target link.
- Build scripts invoke `gcc` instead of the target-prefixed compiler.
- Floating-point ABI mismatch causes link errors or runtime corruption.
- Target-specific headers are shadowed by host headers.
- Generated code is compiled for the wrong architecture.

## Verification / debugging
Record the compiler target triple, sysroot, include paths, library search paths, and linker script. Inspect object files with `file`, `readelf`, `objdump`, or target-equivalent tools. Verify that every object has the expected architecture and ABI. Make CI fail if host and target tool invocations are ambiguous.

## Performance, memory, timing and power
The cross compiler determines target instruction selection and therefore flash, RAM, cycle count, and energy. Build reproducibility also affects the ability to compare performance across toolchain versions.

## Staff-level takeaway
Treat cross compilation as a controlled transformation between two environments. Explicitly define the target triple, sysroot, ABI, libraries, and linker inputs so that the build cannot accidentally depend on the host.