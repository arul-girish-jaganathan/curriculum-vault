# Target triples

> Canonical C topic note — chapter 38.

## Definition
A target triple identifies the broad compilation target, conventionally using architecture, vendor, operating system, and environment components, such as `arm-none-eabi`. It is a toolchain identity, not a complete description of every MCU option.

## Mechanism and language rules
The triple influences compiler defaults, ABI, runtime libraries, assembler syntax, and linker behavior. Additional options select a concrete CPU, ISA extensions, floating-point unit, ABI variant, and tuning strategy.

For example, two builds may share `arm-none-eabi` but differ in Cortex-M core, floating-point instructions, optimization tuning, or vendor-specific startup code.

## Embedded implications
The target identity must match silicon and board assumptions. Wrong ISA/FPU selection can cause immediate faults; wrong ABI can silently corrupt calls across object boundaries. A build manifest should therefore record triple plus CPU/architecture flags and library versions.

## Edge cases and failure modes
- Treating the triple as sufficient hardware identification.
- Mixing `arm-none-eabi` and Linux/ARM objects.
- Selecting an ISA extension unsupported by the installed MCU.
- Mixing hard-float and soft-float objects.

## Verification / debugging
Inspect compiler predefined macros, verbose compiler output, ELF attributes, and object metadata. Compile ABI probes and verify the final image's architecture attributes. Make the target tuple a CI input rather than an implicit workstation default.

## Staff-level takeaway
A target triple is the beginning of target identity, not the end. Record every ABI and ISA dimension that can affect interoperability or executable correctness.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
