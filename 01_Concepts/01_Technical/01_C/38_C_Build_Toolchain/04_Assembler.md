# Assembler

## Definition
The **assembler** converts assembly language into relocatable machine-code object files. In a C toolchain it is usually used after the compiler emits assembly or directly for startup code, context-switch code, interrupt entry, linker glue, and architecture-specific routines.

## Scope and boundaries
Assembly syntax, directives, relocation types, object formats, and instruction sets are implementation-specific. C does not define assembly language. Inline assembly adds another compiler contract and should be treated separately from standalone assembly sources.

## Mechanism and language rules
A typical path is:

```text
C -> compiler -> .s -> assembler -> .o -> linker -> ELF/image
```

The assembler resolves local assembly syntax but generally leaves external symbol addresses and relocations for the linker. Directives can define sections, symbols, alignment, visibility, constants, and metadata.

## Embedded implications
Standalone assembly is common for reset handlers, vector tables, exception entry, context switching, atomic primitives, bootloader handoff, and tightly controlled instruction sequences. Such code is tightly coupled to the ABI: register preservation, stack alignment, argument registers, return registers, and unwind/debug conventions must match compiled C.

Assembly that touches peripherals must also respect the architecture's memory ordering and the device's programming model. The assembler itself does not know whether a memory access is semantically safe.

## Edge cases and failure modes
- Assembly written for the wrong instruction set or ISA extension.
- Incorrect stack alignment at a C function boundary.
- Missing `.type`, visibility, unwind, or section directives expected by the toolchain.
- Clobbering callee-saved registers.
- Incorrect relocation or literal-pool assumptions.
- Mixing assembler syntax modes or object formats.

## Verification / debugging
Inspect the generated `.o` with `objdump`, `readelf`, or equivalent tools. Check relocations and symbol tables. Disassemble the final ELF and verify that startup/ISR entry code follows the documented ABI. Build assembly under every supported target variant.

## Performance, memory, timing and power
Assembly can provide exact instruction selection and may be necessary for architecture-specific primitives, but it increases maintenance cost and can block compiler optimization. Measure cycle counts and verify instruction availability on the exact silicon revision.

## Staff-level takeaway
Keep assembly at narrow, justified boundaries. Define the C/assembly ABI explicitly, test it with disassembly and runtime checks, and prefer compiler-generated code when it can meet the requirement without sacrificing correctness or evidence.