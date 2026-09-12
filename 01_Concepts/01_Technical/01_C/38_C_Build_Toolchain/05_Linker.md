# Linker

## Definition
The **linker** combines relocatable object files and libraries into a final executable image, resolving symbols and relocations and assigning addresses to sections. In embedded systems it is a core architectural tool: it determines where code, constants, initialized data, zero-initialized data, stacks, boot metadata, and special sections live.

## Scope and boundaries
Linking is largely implementation and object-format specific. ISO C defines source-level translation and program semantics, not ELF symbol binding or linker scripts. The linker must nevertheless produce an executable consistent with the compiler's ABI and the target memory map.

## Mechanism and language rules
Conceptually:

```text
foo.o + bar.o + libraries + startup.o + linker script
                    |
                  linker
                    v
              ELF / image
```

The linker resolves undefined references, selects archive members, applies relocations, merges/places sections, defines symbols, and reports unresolved or multiply defined symbols.

### Symbol resolution
Strong/weak definitions, visibility, archive extraction order, and object-file relationships can determine which implementation is selected. Link order can matter for static archives because members are commonly extracted to satisfy currently unresolved references.

## Embedded implications
The linker maps logical sections into physical flash/RAM regions and may define symbols used by startup code, bootloaders, stacks, heaps, DMA buffers, interrupt vectors, and persistent storage. A successful link does not prove that the memory map is correct; an address can be link-valid but hardware-invalid.

Link-time garbage collection can remove unused sections, while explicit retention rules may be required for vectors, registration tables, metadata, or bootloader-visible symbols.

## Edge cases and failure modes
- Multiple incompatible libraries satisfy the same symbol.
- Archive order changes the selected implementation.
- A section is garbage-collected even though firmware discovers it indirectly.
- A symbol crosses a bootloader/application ABI without a stable contract.
- RAM/flash overflow is hidden until a configuration changes.
- Relocation range or section placement exceeds architectural limits.

## Verification / debugging
Treat the linker map as a primary review artifact. Check section sizes, addresses, alignment, symbols, memory-region utilization, and retained sections. Inspect ELF symbols and relocations. Compare map files between releases to detect unexpected growth or placement changes.

## Performance, memory, timing and power
Placement affects flash wait states, cache locality, execute-in-place behavior, RAM access, and DMA accessibility. Dead-section removal reduces image size. Poor placement can increase startup copy time or put hot code/data into slower memory.

## Staff-level takeaway
The linker is where software architecture becomes a concrete memory image. Review the linker script and map with the same seriousness as C source: verify symbol contracts, placement constraints, image boundaries, and failure margins.