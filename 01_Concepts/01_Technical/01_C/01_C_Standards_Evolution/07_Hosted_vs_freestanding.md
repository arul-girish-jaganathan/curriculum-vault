# Hosted vs Freestanding

ISO C distinguishes hosted and freestanding implementations. The distinction is fundamental for embedded systems because a bare-metal firmware environment may not provide the assumptions associated with a general-purpose hosted environment.

## Hosted implementation
A hosted implementation provides the complete required language environment and standard library facilities defined for hosted implementations. The program startup and execution environment are therefore governed by the implementation's hosted requirements.

## Freestanding implementation
A freestanding implementation is permitted a smaller execution environment and is intended for systems where a full host environment is unavailable or inappropriate. This is common in firmware, boot code and low-level runtime environments.

## What this changes
A freestanding implementation does not mean “anything goes.” ISO C still defines language semantics and required portions of the freestanding environment. But facilities such as general file I/O or process-oriented behavior cannot simply be assumed to exist because they exist on Linux or Windows.

## Embedded boundary
The startup symbol, vector table, reset handler, memory initialization, interrupt mechanism, linker script, peripheral access and RTOS startup are implementation/platform concerns. The C standard does not specify how an MCU enters `main`, how `.data` is copied from flash, how `.bss` is cleared, or how a watchdog reset is recorded.

## Common mistake
“Bare metal means C is non-standard” is wrong. A firmware project can use conforming C language constructs in a freestanding implementation while depending on documented implementation and hardware interfaces at its system boundary.

## Verification
Record the target's claimed C conformance profile, compiler mode, library subset and startup model. Test standard-library availability instead of assuming hosted APIs exist.

## Staff-level view
Architecture documents should explicitly label the boundary between ISO C, compiler/runtime support and hardware. This prevents portability arguments from being applied to the wrong layer.

## Related
- [[08_Implementation_defined_behavior]]
- [[54_C_Freestanding_Hosted_Conformance]]
- [[83_C_Start_Up_Runtime]]
