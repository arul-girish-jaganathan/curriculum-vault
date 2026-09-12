# Debugger scripting

> Canonical C topic note — Chapter 41. Debugger scripting automates repeatable target inspection and control. It is debugger-specific tooling, not C syntax, and should be treated as an engineering instrument with a defined safety and reproducibility model.

## Definition
A debugger script is a sequence of commands or a debugger extension that can set breakpoints, inspect registers/memory, evaluate expressions, configure target state, collect traces, or automate repetitive tests. Common environments provide command languages, Python APIs, GDB/MI interfaces, IDE macros, or probe-specific scripting.

## Mechanism and language rules
The script operates on the compiled program and target state. It can use symbols and source names when debug information exists, or raw addresses/registers when it does not. Script correctness therefore depends on the binary, ABI, memory map, debugger version, and target configuration.

### What to reason about
- Does the script read ordinary RAM or side-effecting MMIO?
- Is an address derived from symbols or hard-coded?
- Does the script assume a particular optimization level?
- Does it halt execution or merely observe state?
- Are commands idempotent and safe after partial failure?
- Can the script itself perturb timing or race behavior?

Prefer scripts that collect evidence rather than mutate firmware state. When mutation is necessary, make it explicit and reversible.

## Embedded implications
Scripts are valuable for board bring-up, repeated register checks, fault injection, memory-pattern tests, peripheral configuration validation, and automated regression reproduction. They can turn a manual 20-step debugger procedure into a repeatable experiment.

Hard-coded addresses become fragile across MCU variants and linker layouts. Prefer symbol-based access for firmware objects and documented register names/addresses for hardware. Scripts should fail loudly when expected symbols or memory regions are absent.

### Firmware review angle
Store important scripts with the firmware/tooling repository, record debugger/probe versions, and avoid hidden IDE state. A production incident should be reproducible by another engineer using documented artifacts.

## Edge cases and failure modes
- **Wrong image:** symbols resolve to incorrect addresses.
- **Side-effecting reads:** MMIO inspection changes peripheral state.
- **Timing distortion:** repeated halts hide a race.
- **Version drift:** debugger command semantics change.
- **Unsafe writes:** a script can disable clocks, watchdogs, or protection accidentally.

## Example pattern
```text
# Pseudocode for a debugger procedure
load_symbols(exact_elf)
read_register(PC)
read_register(SP)
dump_memory(stack_base, stack_size)
resolve_symbol(PC)
```
The exact commands are debugger-specific; the important design is to establish binary identity, capture raw context, then symbolize it.

## Verification / debugging
Test scripts against known-good and intentionally-faulted images. Validate expected addresses, register values, and failure handling. Keep a machine-readable output mode when scripts feed CI or incident tooling.

Staff-level questions:
- What assumptions about ABI, symbols, and memory map are encoded?
- Can the script detect an incompatible image?
- What target state can it mutate?
- Does automation preserve the timing characteristics relevant to the bug?

## Staff-level takeaway
Debugger scripts should make debugging **repeatable, reviewable, and evidence-driven**. Treat them as production-quality diagnostic tooling when they become part of bring-up, CI, or field-failure analysis.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
