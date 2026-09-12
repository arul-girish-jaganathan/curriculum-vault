# Cross compiler

> Canonical C topic note — chapter 38.

## Definition
A cross compiler runs on one host while producing code for a different target architecture or operating environment. Embedded development is predominantly cross-compilation because the build workstation and MCU differ.

## Mechanism and language rules
The toolchain normally includes compiler, assembler, linker, headers, startup/runtime objects, and target libraries. Host and target are distinct concepts: the compiler executes on the host, while the generated binary executes on the target. `sizeof`, integer widths, alignment, endianness, ABI, and available headers/libraries therefore follow the target implementation.

## Embedded implications
Cross builds must select the correct CPU, instruction set, FPU/ABI, memory model, linker script, startup files, and libc. Accidentally using host headers or libraries can compile successfully but generate an unusable image.

## Edge cases and failure modes
- Host `sizeof(long)` assumptions leaking into target code.
- Wrong `-mcpu`/FPU options producing illegal instructions.
- Mixing target and host objects.
- Executing target binaries during the build without an emulator.
- Non-reproducible SDK paths or environment variables.

## Verification / debugging
Print the complete compiler command line and target triple. Inspect object attributes, ELF headers, symbol tables, and final image metadata. Run a trivial target program and a compile-time ABI probe containing `sizeof`, `_Alignof`, and integer-width checks.

## Staff-level takeaway
Treat cross compilation as a typed pipeline: host tools produce target artifacts under a precisely defined ABI and sysroot. Every stage must agree on the same target contract.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
