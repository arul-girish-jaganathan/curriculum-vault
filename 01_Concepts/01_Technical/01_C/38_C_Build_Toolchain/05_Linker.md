# Linker

> Canonical C topic note — chapter 38.

## Definition
The linker combines relocatable object files and libraries into a final executable image, resolving symbols and assigning addresses according to linker rules. It is where many embedded memory-layout decisions become concrete.

## Mechanism and language rules
The linker resolves references, applies relocations, merges sections, selects archive members, defines symbols, and emits an executable or firmware image. Its behavior is primarily toolchain/platform-specific rather than ISO C.

## Embedded implications
The linker maps code to flash, initialized data to load/run addresses, zero-initialized data to RAM, stacks/heaps to reserved regions, and vectors/startup sections to hardware-required addresses. It can also discard unused sections with garbage collection.

## Edge cases and failure modes
- Multiple strong definitions.
- Missing symbols or wrong libraries.
- Archive extraction order causing unresolved references.
- Overlapping memory regions.
- Incorrect load versus execution addresses.
- Garbage collection removing indirectly referenced firmware objects.

## Verification / debugging
Read linker diagnostics and the map file. Inspect section addresses, sizes, symbols, and relocation results. Confirm startup copies `.data` and clears `.bss` according to the linker layout. Validate image boundaries against the device memory map.

## Staff-level takeaway
The linker is part of the executable's architecture. Treat the linker script, memory map, symbol contracts, and generated image as reviewed source artifacts rather than opaque build output.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
