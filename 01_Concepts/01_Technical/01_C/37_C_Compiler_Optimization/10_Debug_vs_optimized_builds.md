# Debug vs optimized builds

## Definition
A **debug build** and an **optimized build** differ in compiler transformations, debug information, assertions, instrumentation, libraries, linker behavior, and often timing. Debugging at `-O0` is useful, but it is not a substitute for validating the production configuration.

## Scope and boundaries
Optimization does not create bugs in well-defined C; it often exposes bugs that were already present. Undefined behavior, data races, lifetime errors, uninitialized reads, invalid aliasing, and timing-sensitive assumptions can behave differently when optimization changes code layout and execution order.

## Mechanism and language rules
At low optimization levels, compilers tend to preserve more source structure and emit more loads/stores. At higher levels they can inline, fold constants, eliminate code, reorder instructions, coalesce variables, and transform control flow. Debug information maps machine instructions back to source but cannot recreate eliminated source operations.

```text
source -> preprocessing -> compilation -> optimization -> assembly -> linking
```

Debug symbols describe the resulting machine code; they do not force the machine code to mirror the source.

## Embedded implications
A firmware defect that exists only in the release build is usually a major clue to undefined behavior, missing synchronization, uninitialized state, stack corruption, or an incorrect hardware contract. Conversely, a timing bug can disappear in a debug build because extra instructions slow execution.

Release builds should therefore be debuggable: keep suitable DWARF/debug information, map files, symbol files, trace support, and controlled optimization settings rather than relying on an entirely unoptimized image.

## Edge cases and failure modes
- Variables appear as “optimized out.”
- Breakpoints move or multiple source lines map to one instruction.
- Stack frames are omitted or transformed.
- A race disappears under a debugger because timing changes.
- An invalid pointer works at `-O0` but fails at `-O2`.
- Assertions or logging alter timing and hide a fault.

## Verification / debugging
Reproduce issues with the exact production compiler flags whenever possible. Use disassembly, map files, core dumps, trace, watchpoints, and sanitizers on host/reference builds. Compare optimization levels only as a diagnostic experiment, not as proof that the lower level is correct.

Record compiler version, target options, preprocessor defines, linker script, libraries, and LTO state so a failing binary can be reproduced.

## Performance, memory, timing and power
Optimization changes code size, stack usage, interrupt latency, cache behavior, and power. Debug instrumentation can radically distort all of these. Measure production images on the target, especially for real-time paths.

## Staff-level takeaway
The production build is a first-class test target. A mature firmware workflow supports source-level debugging of optimized binaries and uses controlled differential builds to isolate optimization-sensitive defects without weakening the final configuration.