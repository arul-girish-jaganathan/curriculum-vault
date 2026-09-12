# Debugger scripting

> Canonical C topic note — Chapter 41. Debugger scripting automates repeatable target inspection and control. It is tooling rather than C syntax, so its correctness depends on the debugger, probe, binary, ABI, memory map, and target state.

## Definition
A debugger script is a command sequence or extension that sets breakpoints, inspects registers and memory, evaluates symbols, configures target state, collects traces, or automates repetitive experiments. Environments may expose command languages, Python APIs, GDB/MI, IDE macros, or probe-specific interfaces.

## Mechanism and language rules
Scripts operate on compiled artifacts and live machine state. Symbol-based commands depend on debug information; raw addresses depend on the target memory map. A script must therefore encode its assumptions explicitly.

### What to reason about
- Does a command merely observe state or mutate it?
- Does a memory read access side-effecting MMIO?
- Are addresses derived from symbols or hard-coded?
- Does the script assume `-O0`, a frame pointer, or a particular ABI?
- Does it halt execution and alter timing?
- Is it idempotent after a partial failure?

Prefer evidence collection over mutation. When writes are necessary, make them explicit, bounded, and reversible.

## Embedded implications
Scripts are useful for board bring-up, register validation, memory tests, fault injection, repeated reproduction, and automated capture of CPU context. They can turn a long manual debugger procedure into a deterministic experiment.

### Firmware review angle
Keep important scripts under version control with the firmware/tooling. Record debugger and probe versions. Validate that the running image matches the expected symbol file before issuing address-sensitive commands.

## Edge cases and failure modes
- **Wrong image:** symbols resolve to incorrect addresses.
- **MMIO side effect:** inspection changes peripheral state.
- **Timing distortion:** repeated halts hide races.
- **Version drift:** debugger command behavior changes.
- **Unsafe writes:** scripts can disable clocks, watchdogs, or protection.

## Example pattern
```text
load_symbols(exact_elf)
assert_symbol("fault_record")
read_register(PC)
read_register(SP)
dump_memory(fault_record, RECORD_SIZE)
resolve_symbol(PC)
```
The exact syntax varies by debugger; the design principle is to validate identity, capture raw state, then symbolize it.

## Verification / debugging
Test scripts on known-good and intentionally-faulted images. Check expected symbol addresses, output formats, error handling, and incompatible-image detection. For CI use, prefer machine-readable output and deterministic exit status.

Staff-level questions: What assumptions are encoded? Can the script detect a mismatched binary? What state can it mutate? Does automation preserve the timing conditions relevant to the defect?

## Staff-level takeaway
Debugger automation should make diagnosis **repeatable, reviewable, and evidence-driven**. Once it becomes part of bring-up or production incident response, treat it like production engineering tooling with versioning and tests.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
