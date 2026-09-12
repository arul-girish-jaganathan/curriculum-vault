# Compiler selection

> Canonical C topic note — chapter 38.

## Definition
Compiler selection is an engineering decision about the implementation of C, target ISA, ABI, diagnostics, optimization quality, runtime support, licensing, reproducibility, and long-term maintenance. ISO C defines the language; the compiler supplies the target-specific realization.

## Mechanism and language rules
Evaluate language-version support, extensions, diagnostics, ABI compatibility, floating-point model, atomic support, linker integration, debug formats, static-analysis integration, and library/runtime availability. A compiler choice should be tied to a documented target tuple and release version, not simply “GCC” or “Clang.”

## Embedded implications
For MCUs, compare generated code, startup/runtime requirements, interrupt attributes, section placement, linker support, CMSIS/vendor SDK compatibility, FPU settings, and debugger ecosystem. Small differences can affect flash, RAM, cycles, power, and certification evidence.

## Edge cases and failure modes
- Mixing object files built for different ABIs.
- Accidentally enabling incompatible ISA/FPU options.
- Relying on undocumented extensions.
- Upgrading compilers without regression measurements.
- Treating warning changes as harmless.

## Verification / debugging
Record compiler version, target triple, flags, sysroot/libc, linker, and binutils. Build a representative benchmark and compare warnings, binary size, timing, and ABI-sensitive interfaces. Keep a reproducible release manifest.

## Staff-level takeaway
Select a toolchain as part of the product architecture. The best compiler is the one whose language, ABI, diagnostics, generated code, ecosystem, and lifecycle satisfy the product constraints with evidence.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
