# Debug vs optimized builds

> Canonical C topic note — chapter 37.

## Definition
Debug and optimized builds differ in optimization, debug information, assertions, instrumentation, libraries, and sometimes compiler-defined configuration. A debugger view of source is therefore not a faithful execution trace of optimized machine code.

## Mechanism and language rules
At `-O0`, variables are more likely to have simple stack/register representations and source statements often map more directly to instructions. At higher optimization, variables can be folded, merged, moved, eliminated, or represented only transiently. Instruction scheduling and inlining can make stepping appear to jump or execute lines out of order.

This does not change defined C semantics; it changes the implementation used to realize them.

## Embedded implications
Never validate firmware correctness only in a debug build. Optimization can expose UB, races, missing volatile qualification, stack assumptions, and timing-sensitive bugs. Conversely, debug instrumentation can hide races or alter timing enough to mask failures.

Production-like builds should use the release compiler, linker script, LTO settings, libraries, startup code, and memory map. Keep enough debug symbols or post-build symbol artifacts to debug the actual image.

## Edge cases and failure modes
- “It works at `-O0`” treated as proof of correctness.
- Debug assertions or logging changing timing.
- Different linker garbage collection changing retained code.
- Stack overflow appearing only in optimized or inlined code.
- Debugger memory reads accidentally interacting with hardware registers.

## Verification / debugging
Reproduce with the exact failing optimization settings. Save ELF/map/disassembly artifacts for the binary. Use sanitizers and static analysis on host builds, then validate target behavior under the production configuration. Compare stack usage, image size, ISR latency, and watchdog margins.

## Staff-level takeaway
Maintain separate debugability and correctness strategies. The strongest workflow makes release builds observable enough to diagnose while ensuring that debug builds are never the only evidence of system correctness.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
