# Assembler

> Canonical C topic note — chapter 38.

## Definition
The assembler converts assembly source or compiler-generated assembly into relocatable object code. It establishes instruction encodings, sections, symbols, relocations, alignment, and target-specific directives that later stages consume.

## Mechanism and language rules
A compiler may emit assembly or object code directly. The assembler resolves local syntax and creates relocation records when an address cannot yet be known. It does not normally decide the final address of every symbol; the linker does that later.

## Embedded implications
Assembly appears at ABI boundaries, startup, interrupt entry, context switching, low-level barriers, boot code, and performance-critical primitives. The C compiler must know about any inline assembly inputs, outputs, clobbers, and memory effects; otherwise optimizer assumptions can invalidate the program.

## Edge cases and failure modes
- Wrong instruction-set mode.
- Incorrect alignment or section flags.
- Missing relocation assumptions.
- Inline assembly with incomplete clobber constraints.
- Assembly routines violating the C calling convention.

## Verification / debugging
Disassemble object and final ELF files. Inspect relocations and section attributes. Compare register use with the ABI. Keep assembly interfaces small and document every compiler-visible side effect.

## Staff-level takeaway
Assembly is not just “machine code text”; it is an object-generation stage with symbols, relocations, sections, and ABI contracts. Review those artifacts explicitly when C crosses into assembly.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
