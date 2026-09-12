# Linker scripts

## Definition
A **linker script** describes how the linker should arrange sections, define memory regions and symbols, control placement, and sometimes enforce image constraints. It is especially important in bare-metal firmware because the target has a fixed memory map rather than a general-purpose operating-system loader.

## Scope and boundaries
Linker-script syntax is toolchain-specific, commonly GNU ld-style in embedded environments. It is not part of ISO C. The C program can refer to symbols created by the linker, but their addresses and placement are implementation contracts.

## Mechanism and language rules
A conceptual script describes:

```text
MEMORY: FLASH, RAM, peripheral/retention regions
SECTIONS: .text, .rodata, .data, .bss, custom sections
symbols: _stack_top, __data_start, __bss_end, etc.
```

Initialized `.data` may have a load address in flash and a runtime address in RAM. Startup code copies the initial image before C code uses the objects. `.bss` is normally zero-initialized by startup code.

### Custom sections
Attributes such as `__attribute__((section(".fast")))` can place objects/functions into special regions. The compiler, linker script, startup code, debugger, and hardware must agree on the contract.

## Embedded implications
Scripts control vector tables, boot/application boundaries, execute-in-place code, RAM functions, DMA buffers, no-init retention areas, calibration data, secure partitions, and stack/heap regions. Alignment and region attributes can determine whether DMA or a peripheral can access an object correctly.

A linker script should encode important limits so failures occur at build time rather than on the target.

## Edge cases and failure modes
- Load address confused with virtual/runtime address.
- `.bss` or `.data` startup symbols do not match startup code.
- Custom section is orphaned or placed into an inaccessible memory region.
- Alignment is insufficient for hardware requirements.
- A section is not retained because no ordinary reference exists.
- Stack grows into heap or another region without a build-time check.

## Verification / debugging
Review `MEMORY` regions, section placement, `LOADADDR`, alignment, generated symbols, and map output. Add assertions for image size, vector placement, and region boundaries where supported. Inspect the final ELF rather than assuming the script did what the source intended.

## Performance, memory, timing and power
Placement determines memory speed, wait states, cacheability, XIP behavior, DMA reachability, and startup copy cost. Moving a hot function to fast RAM can reduce latency but consumes scarce RAM and may increase startup time.

## Staff-level takeaway
Treat the linker script as executable architecture documentation. Every custom section should have a stated owner, placement requirement, initialization model, retention rule, and verification method.