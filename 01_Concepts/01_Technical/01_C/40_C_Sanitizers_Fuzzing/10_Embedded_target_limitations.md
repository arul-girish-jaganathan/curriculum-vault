# Embedded-target limitations

## Definition
Sanitizers and fuzzers are powerful, but constrained embedded targets impose limits in address space, RAM, flash, execution speed, I/O, debugging, and runtime support. These limitations determine which testing techniques should run on the MCU and which should run on a host or simulation environment.

## Scope and boundaries
A host sanitizer build is not equivalent to the target binary. It cannot directly prove MMIO correctness, interrupt behavior, DMA ownership, cache coherency, target alignment faults, or exact ABI behavior. Conversely, target fuzzing can expose hardware-specific defects that host execution cannot reproduce.

## Mechanism and language rules
Use a layered strategy:

```text
host + sanitizers + fuzzing
          |
          v
target unit/integration tests
          |
          v
hardware-in-loop / fault injection
```

Keep portable logic isolated from hardware so it can receive high-volume host testing.

## Embedded implications
Common constraints include insufficient RAM for ASan shadow memory, unavailable sanitizer runtime, slow flash writes for corpus storage, watchdog resets during long fuzz cases, and difficulty collecting stack traces. DMA and peripherals can modify memory without passing through instrumented compiler code.

## Edge cases and failure modes
- Assuming a target sanitizer-clean result covers DMA/hardware accesses.
- Host and target have different integer widths or alignment.
- Instrumentation changes real-time behavior.
- Watchdog or low-power behavior invalidates fuzz execution.
- Debug UART becomes the bottleneck or changes timing.

## Verification / debugging
Document which defect classes each environment can detect. Use host fuzzing for parsers and algorithms, target tests for hardware contracts, and differential testing for portable outputs. Where target sanitizers are unavailable, add allocator guards, stack canaries, MPU checks, hardware watchpoints, and targeted fault injection where supported.

## Performance, memory, timing and power
Instrumentation can multiply memory and execution costs, which is often unacceptable on an MCU. Target testing should therefore remain lean and deterministic while host testing provides high-volume exploration.

## Staff-level takeaway
Do not ask “host or target?” Ask **which environment can observe the failure mode?** Build a layered validation architecture so each environment covers the blind spots of the others.