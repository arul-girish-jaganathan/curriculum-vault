# Embedded-target limitations

> Canonical C topic note — chapter 40.

## Definition
Sanitizers and fuzzers require runtime instrumentation, memory, execution time, and often operating-system facilities that may not exist on an MCU. Their absence on target does not make them unsuitable; it changes how evidence is collected.

## Mechanism and language rules
Host instrumentation can validate target-independent C logic. Target testing must cover implementation-specific behavior such as MMIO, interrupts, DMA, alignment, cache/coherency, startup, and actual ABI.

## Embedded implications
Instrumented images can consume substantial flash/RAM, alter timing, change memory layout, and interfere with watchdog or real-time constraints. Fuzzing on target may therefore be selective rather than continuous.

## Edge cases and failure modes
- Assuming host sanitizer results cover target-specific UB.
- Running instrumentation in timing-critical production-like measurements.
- Ignoring allocator differences.
- Testing only valid protocol inputs.

## Verification / debugging
Partition the test strategy: host sanitizer/fuzz coverage for pure logic, target tests for hardware contracts, and differential tests for representation-sensitive behavior. Document which defect classes each layer can detect.

## Staff-level takeaway
Do not ask whether sanitizers “work on the MCU” as a binary question. Ask which semantic boundary is being tested and which evidence is still missing.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
