# Reading compiler output

## Definition
Reading compiler output means using assembly, optimization reports, intermediate artifacts, symbol tables, section maps, and diagnostics to understand what the toolchain actually generated from C. For Staff-level embedded work, source inspection alone is insufficient when performance, ABI, timing, memory placement, or optimization is under review.

## Scope and boundaries
Assembly is target-specific; C semantics are not. Never infer ISO C guarantees from one compiler's output. Conversely, when validating a firmware image, generated output is essential evidence because the MCU executes machine code, not the C source.

## Mechanism and language rules
A useful inspection chain is:

```text
C source -> preprocessed source -> compiler diagnostics -> assembly/object -> linker -> ELF/map -> binary
```

Inspect function prologues/epilogues, loads/stores, branches, calls, register allocation, literal pools, section placement, relocations, and symbol visibility. Optimization remarks can explain why a loop was or was not vectorized or inlined.

## Embedded implications
For a suspicious driver function, confirm that MMIO accesses use the intended width and ordering. For an ISR, inspect entry/exit code and saved registers. For a hot loop, count relevant instructions and memory operations on the real architecture. For startup code, inspect reset entry, data copying, zeroing, stack setup, and constructor/runtime hooks where present.

The linker map reveals flash/RAM consumption and placement that cannot be understood from one `.c` file.

## Edge cases and failure modes
- Debugging the wrong binary or stale object file.
- Inspecting source with different preprocessor configuration than the released build.
- Counting instructions without considering pipeline, wait states, caches, or flash accelerators.
- Assuming a visible symbol must correspond to an executed function; LTO and section garbage collection can alter reachability.
- Assuming assembly from one MCU family applies to another.

## Verification / debugging
Use the compiler's assembly output, optimization reports, `objdump`/`readelf`/`nm` or target-equivalent tools, and the linker map. Correlate addresses with the ELF and debugger symbols. For performance, use cycle counters or hardware trace to validate the static inspection.

A strong workflow is to formulate a hypothesis first—such as “this load is repeated”—then locate the corresponding instructions and measure whether it matters.

## Performance, memory, timing and power
Assembly inspection can reveal redundant memory accesses, spills, branches, missed inlining, unexpected library calls, and code-size growth. But static instruction counts are only a model; target measurements determine actual timing and energy.

## Staff-level takeaway
Generated artifacts are engineering evidence. A Staff engineer should be able to move from a high-level requirement to C semantics, compiler decisions, ABI details, linker placement, and finally measured hardware behavior without treating any one layer as the whole system.