# Linker scripts

> Canonical C topic note — chapter 38.

## Definition
A linker script describes how input sections and symbols are arranged into output sections and memory regions. In embedded systems it is effectively part of the memory architecture.

## Mechanism and language rules
Typical concepts include `MEMORY`, `SECTIONS`, load addresses (`AT`), alignment, symbols, section placement, and retention (`KEEP`). Input sections such as `.text`, `.rodata`, `.data`, `.bss`, interrupt vectors, and custom DMA sections can be mapped deliberately.

## Embedded implications
A common pattern places initialized data in flash while its runtime address is RAM; startup code copies it. `.bss` occupies RAM but has no stored image bytes. Custom regions may reserve bootloader/application boundaries, non-cacheable DMA memory, retention RAM, or persistent records.

## Edge cases and failure modes
- Wrong region origin/length.
- Misaligned DMA buffers.
- Forgetting load-versus-run address handling.
- Garbage collection removing required sections.
- Symbols used by startup code being changed without review.

## Verification / debugging
Review the script with the MCU reference manual. Inspect the linker map and final ELF. Assert critical boundaries with linker `ASSERT` where supported. Test startup initialization and boot/update layouts on hardware.

## Staff-level takeaway
A linker script is executable architecture documentation: every memory region and special section should have an owner, purpose, size budget, initialization policy, and verification method.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
