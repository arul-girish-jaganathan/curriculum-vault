# Reading compiler output

> Canonical C topic note — chapter 37.

## Definition
Compiler output includes assembly, object files, symbol tables, relocation records, optimization reports, debug information, and linker maps. Reading these artifacts is how an embedded engineer verifies what the toolchain actually produced.

## Mechanism and language rules
At minimum, learn to correlate C source with: function entry/exit, loads/stores, branches, calls, returns, constant materialization, stack offsets, and register use. Then learn ELF/object concepts, sections, symbols, relocations, and linker placement.

A source statement can produce zero, one, or many instructions. Conversely, several source operations can combine into one instruction sequence.

## Embedded implications
Assembly inspection is essential for MMIO width, barrier instructions, interrupt prologues, calling conventions, stack usage, flash placement, and hot-loop timing. Map files reveal RAM/ROM consumption and unexpected library pulls.

Useful tools include compiler `-S`, object disassemblers such as `objdump`, symbol tools such as `nm`, and linker map files. Exact options are toolchain-specific.

## Edge cases and failure modes
- Reading assembly without knowing the ABI.
- Confusing addresses in a relocatable object with final linked addresses.
- Assuming source line order equals instruction order.
- Ignoring literal pools, veneers, thunks, or linker-generated stubs.
- Measuring a non-production build.

## Verification / debugging
Pick one critical function and inspect its final linked disassembly. Confirm argument passing, return value, MMIO accesses, stack frame, section placement, and expected barriers. Compare map-file symbols against the memory budget.

## Staff-level takeaway
A Staff engineer should be able to cross the abstraction boundary from C to ELF to machine code and explain discrepancies using evidence rather than intuition.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
