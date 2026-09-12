# Debugger scripting

> Canonical C topic note — chapter 41.

## Definition
Debugger scripting automates repetitive inspection and control operations: loading an image, setting breakpoints, dumping memory, collecting registers, walking stacks, checking invariants, and producing crash reports. It turns manual debugging into repeatable evidence collection.

## Mechanism and language rules
Debugger commands operate on implementation-level state. A script may evaluate C expressions using debug information, inspect registers, access memory, and control execution. Exact command languages and capabilities are tool-specific.

A robust script should distinguish:
- target connection/setup;
- symbol/image validation;
- observation;
- mutation of target state;
- output formatting;
- failure handling.

Avoid scripts that silently continue after an image mismatch or invalid memory access.

## Embedded implications
Scripts are especially valuable for fleet debugging and lab regression. A standard fault script can collect PC, SP, LR, status registers, fault-status registers, stack windows, task state, selected globals, and memory-map information in a consistent order.

For boot failures, automate reset, halt-at-entry, vector-table inspection, startup stepping, and register snapshots. For peripheral issues, automate register dumps before and after a transaction while respecting clear-on-read/write-one-to-clear semantics.

### Example workflow
```text
connect target
verify image/build-id
reset and halt
read PC/SP/LR/status
read fault registers
validate SP region
save stack window
symbolize PC
export timestamped report
```
The exact syntax varies by debugger; the workflow is the important reusable artifact.

## Edge cases and failure modes
- Scripts can read destructive MMIO registers.
- A target may be running while the script assumes it is halted.
- Reset may invalidate previous symbol or peripheral state.
- Memory reads can fault or hang on an inaccessible bus region.
- Automation can accidentally write registers and alter the failure.
- A script tied to absolute addresses breaks across firmware layouts.

## Verification / debugging
Version-control scripts alongside the firmware tooling. Include expected architecture, debugger version, image identity, and assumptions. Prefer symbolic names and linker-derived addresses where supported. Test scripts against known-good and injected-fault targets.

For crash collection, emit machine-readable output in addition to human-readable text so results can be compared across builds and devices.

## Staff-level takeaway
Debugger scripts are infrastructure, not personal shortcuts. Standardize them around repeatable evidence collection, explicit safety boundaries, build identity, and deterministic output. The payoff is reduced mean time to diagnose and fewer “it worked on my debugger session” conclusions.

## Related
[[00_Chapter_Index]]
[[08_Core_dumps]]
[[09_Post_mortem_analysis]]
[[12_Debugging_production_firmware]]
