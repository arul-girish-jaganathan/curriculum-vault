# Optimized-code debugging

> Canonical C topic note — chapter 41.

## Definition
Optimized-code debugging means diagnosing a program while compiler transformations such as inlining, constant propagation, dead-code elimination, register allocation, loop transformation, and tail calls are active. The debugger presents source mappings, but execution follows the generated machine code.

## Mechanism and language rules
The as-if rule permits any transformation that preserves behavior required by the C abstract machine. Consequently:
- a source variable may not exist at runtime;
- source statements may execute in a different apparent order when their observable behavior permits it;
- several source statements can share instructions;
- calls can disappear through inlining;
- stack frames can disappear through tail calls;
- values can remain entirely in registers.

If the source program has undefined behavior, optimization may expose surprising results because the compiler has no obligation to preserve an intuitive execution trace.

## Embedded implications
Optimization is often mandatory for realistic timing, flash, and power targets, so “debug only at `-O0`” is not a sufficient strategy. A race that disappears at `-O0` may be a symptom of incorrect synchronization rather than an optimization defect. Likewise, timing-sensitive peripheral code can behave differently because instruction count and placement change.

Keep a reproducible optimized ELF with full debug information. Use lower optimization only as a controlled experiment, not as the definition of expected production behavior.

### Example
```c
static uint32_t flag;

void set_flag(void)
{
    flag = 1U;
}
```
If `flag` is never observed by defined program behavior, the store can be removed. If hardware or another execution agent observes it, the C declaration must correctly model that interaction; debugger visibility is not a substitute for correct language semantics.

## Edge cases and failure modes
- “Cannot inspect variable” is often normal under optimization.
- Stepping may skip, repeat, or reorder source lines.
- A debugger may show stale-looking values due to location changes.
- LTO can optimize across translation-unit boundaries.
- Inlining can make a backtrace look different from the source call graph.
- Undefined behavior can produce optimizer-dependent symptoms.
- Adding logging can change timing and hide the bug.

## Verification / debugging
First reproduce with the exact production optimization settings. Compare source view with disassembly around the failing PC. Inspect registers, memory, and branch targets rather than relying solely on source watches. Generate compiler optimization remarks when supported.

If behavior changes with optimization, investigate data races, volatile misuse, strict-aliasing violations, lifetime bugs, signed overflow, uninitialized data, and ABI violations before disabling optimization.

## Staff-level takeaway
Optimization is not an obstacle to debugging; it is part of the system under test. The Staff-level skill is translating between source intent and generated instructions while distinguishing legitimate transformations from evidence of undefined behavior, synchronization bugs, or toolchain defects.

## Related
[[00_Chapter_Index]]
[[01_Source_level_debugging]]
[[05_Registers]]
[[../37_C_Compiler_Optimization/00_Chapter_Index]]
