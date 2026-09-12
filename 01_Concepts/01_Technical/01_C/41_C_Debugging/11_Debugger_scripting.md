# Debugger scripting

> Canonical C topic note — chapter 41.

## Definition
Debugger scripting automates repeatable debugging actions such as loading symbols, validating a firmware image, stopping at known points, collecting registers and memory, checking invariants, walking stacks, and generating machine-readable reports. It converts personal debugger expertise into repeatable engineering infrastructure.

## Mechanism and language rules
Debugger scripts operate below ISO C semantics. They may:

- evaluate typed expressions using debug information;
- inspect and modify registers;
- read/write target memory;
- control execution;
- set or remove breakpoints/watchpoints;
- invoke debugger-specific commands;
- access target peripherals.

A robust script separates:

```text
connection/setup
→ image/symbol validation
→ target state validation
→ observation
→ optional mutation
→ output
→ failure handling
```

The script must make its assumptions explicit. Continuing after an image mismatch or invalid memory read can produce authoritative-looking but false diagnostics.

### Example workflow
```text
connect target
verify architecture and build-id
reset and halt
capture PC/SP/LR/status
capture fault registers
validate stack bounds
save stack window
symbolize PC and caller chain
export timestamped report
```

The exact command language differs among GDB, OpenOCD, vendor IDEs, JTAG tools, and other environments; the workflow is the reusable engineering pattern.

## Embedded implications
Standard scripts are especially useful for lab triage and fleet crash analysis. Typical automated collections include:

- PC/SP/LR and general registers;
- exception/fault status;
- vector-table/reset-state information;
- selected task/ISR metadata;
- stack windows;
- firmware build ID;
- linker-derived memory ranges;
- selected peripheral registers.

For MMIO, scripts must know which registers are clear-on-read, write-one-to-clear, FIFO-backed, or otherwise destructive. Prefer read-only diagnostic register lists maintained with the BSP.

For boot failures, automate reset, halt-at-entry, vector-table verification, startup-register capture, and bounded stepping. For memory corruption, automate guard checks rather than broad unstructured RAM dumping.

## Edge cases and failure modes
- The script assumes a halted target while the CPU is running.
- Reset invalidates previously collected target state.
- Absolute addresses change across linker layouts.
- MMIO reads alter hardware state.
- An inaccessible memory region can fault or stall the debugger connection.
- A script silently operates on the wrong core or wrong image.
- Debugger/version changes alter command behavior.
- A script performs writes while intended to be observational only.

## Verification / debugging
Version-control scripts with the firmware tooling and document the expected architecture, debugger version, symbol format, and safety assumptions. Test against:

1. known-good firmware;
2. deliberately injected faults;
3. image mismatch;
4. unavailable peripheral/memory regions;
5. reset during collection;
6. partially connected/failed debug sessions.

Emit machine-readable output such as JSON/CSV where practical so reports can be compared automatically across builds and devices.

## Staff-level takeaway
Debugger scripts are part of the diagnostic architecture. Treat them like production tooling: deterministic, versioned, validated, explicit about destructive operations, and tied to immutable firmware identity. The goal is repeatable evidence, not merely fewer keystrokes.

## Related
[[00_Chapter_Index]]
[[08_Core_dumps]]
[[09_Post_mortem_analysis]]
[[10_Fault_localization]]
[[12_Debugging_production_firmware]]
