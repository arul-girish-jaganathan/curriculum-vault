# 10: Embedded UB Examples

## Definition
Embedded UB Examples represent classic, high-consequence instances of undefined behavior that frequently manifest in embedded firmware and bare-metal microcontroller development, often leading to hard faults, watchdog resets, and silent data corruption.

## Scope and Boundaries
- **Covers:** Volatile omission on MMIO registers, unaligned access faults, interrupt race conditions, stack overflows, and invalid pointer casts.
- **Does not cover:** General desktop software UB or hosted OS memory management bugs.

## Why Does It Exist
Embedded systems interact directly with bare metal, memory-mapped peripherals, and asynchronous hardware interrupts:
- **Hardware Intimacy:** Low-level register manipulation pushes C code to its absolute semantic boundaries.
- **Severe Consequence:** Unlike hosted desktop applications where a crash terminates a process, embedded UB causes physical system crashes, hardware lockups, or safety hazards.

## Mechanism and Language Rules
- **Volatile Omission:** Accessing a memory-mapped hardware status register through a normal `uint32_t *` pointer without `volatile` allows the compiler to cache the value in a CPU register, creating an infinite polling loop.
- **Interrupt Data Races:** Modifying shared global flags between background loops and ISRs without `atomic` or critical section guards triggers undefined data race behavior.

## Examples
```c
#include <stdint.h>

#define UART_STATUS_REG (*((volatile uint32_t *)0x4000C000))
#define UART_DATA_REG   (*((volatile uint32_t *)0x4000C004))

/* Correct: Using volatile prevents compiler from optimizing away status polling */
void uart_wait_transmit(void) 
{
    while (!(UART_STATUS_REG & 0x01)) {
        /* Poll until transmitter ready */
    }
}

/* Incorrect: Missing volatile allows compiler to read status once and loop forever */
void uart_wait_broken(void) 
{
    const uint32_t *status_ptr = (const uint32_t *)0x4000C000;
    while (!(*status_ptr & 0x01)) { /* UB / Infinite loop risk */ }
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- **Hardware Exception Triggers:** Embedded UB frequently translates directly into CPU hardware exception vectors (e.g., UsageFault, HardFault on ARM Cortex-M).

## Edge Cases and Failure Modes
- **Intermittent Lockups:** Interrupt race conditions occur rarely during load testing, making them notoriously difficult to reproduce and debug in the field.

## Embedded Implications
- **Watchdog Triggering:** Unhandled embedded UB causes system hangs that trip hardware watchdog timers, forcing unexpected reboots.

## Firmware Review Angle
- **Audit MMIO Pointers:** Inspect all hardware register definitions to ensure `volatile` qualifiers are correctly applied.
- **Audit ISR Sharing:** Verify all variables shared between ISRs and main loops use atomic operations or explicit interrupt masking.

## Compiler, ABI, and Toolchain Implications
- **Optimization Destruction:** High optimization levels (`-O3`) aggressively expose embedded UB by stripping redundant-seeming hardware register accesses.

## Performance, Memory, Timing, and Power
- **Reliability Priority:** In embedded systems, correctness and avoidance of UB always supersedes aggressive micro-optimizations.

## Verification / Debugging
- **Hardware Trace & Emulation:** Use JTAG/SWD hardware debuggers, ITM console tracing, and Fault Status Registers (HFSR/CFSR) to diagnose embedded UB crashes.

## Safety, Security, and Reliability
- **Safety Certification:** ISO 26262 and IEC 61508 compliance requires rigorous elimination of all embedded UB hazards.

## Trade-offs and Alternatives
- **`volatile` vs. Atomics:** Use `volatile` strictly for memory-mapped I/O registers; use C11 atomics (`<stdatomic.h>`) for multi-threaded or multi-core shared variables.

## Staff-Level Takeaway
Embedded undefined behavior is unforgiving. A missing `volatile` or an unprotected ISR data race will pass unit tests on your development laptop and crash your hardware in production. Master embedded safety boundaries.

## Related Concepts
- [[00_Chapter_Index]]
- [[04_Undefined_behavior]]
- [[07_Optimizer_exploitation]]
- [[09_Portable_defensive_coding]]
