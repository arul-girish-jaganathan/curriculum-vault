# 11: Embedded Floating Point Cost

## Definition
Embedded Floating Point Cost refers to the performance, memory footprint, timing jitter, and power penalties associated with utilizing floating-point arithmetic on resource-constrained microcontrollers, particularly those lacking hardware Floating-Point Units (FPUs).

## Scope and Boundaries
- **Covers:** Soft-float vs. hard-float ABIs, software floating-point runtime libraries, context-switching overhead, and execution timing.
- **Does not cover:** High-performance desktop FPU tuning, vector extensions, or general floating types specifications.

## Why Does It Exist
Low-cost microcontrollers are designed for minimal silicon area and power consumption:
- **Absence of Hardware FPU:** Without a hardware FPU, every `float` or `double` operation must be emulated in software by runtime helper functions.
- **Execution Time Inflation:** Software-emulated floating-point arithmetic can be 10x to 100x slower than native integer arithmetic.
- **Context-Switch Overhead:** When an RTOS switches tasks on an MCU with a hardware FPU, the FPU registers must be saved to the task stack, increasing context-switch latency unless lazy stacking is enabled.

## Mechanism and Language Rules
- **Soft-Float ABI:** Compiles all floating-point operations into calls to software runtime library routines.
- **Hard-Float ABI:** Emits direct hardware FPU machine instructions. Mixing soft-float and hard-float object files in the same link step results in a fatal linker ABI mismatch error.

## Examples
```c
#include <stdio.h>
#include <stdint.h>

void update_motor_speed_fixed(int32_t *speed_q16, int32_t target_q16, int32_t kp_q16) 
{
    int32_t error = target_q16 - *speed_q16;
    int32_t adjustment = (error * kp_q16) >> 16;
    *speed_q16 += adjustment;
}

int main(void) 
{
    int32_t speed = 0;
    update_motor_speed_fixed(&speed, 1000 << 16, 0x8000);
    printf("Updated fixed-point speed (Q16): %d\n", speed);
    return 0;
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- **Implementation-Defined:** Whether the target toolchain defaults to soft-float or hard-float ABI for a given microcontroller model.

## Edge Cases and Failure Modes
- **Linker ABI Mismatch:** Linking a third-party static library compiled with soft-float against an application compiled with hard-float causes silent register corruption or linker errors.

## Embedded Implications
- **Real-Time Deadline Misses:** Software-emulated floating point in a high-frequency interrupt service routine will destroy interrupt responsiveness and cause deadline misses.

## Firmware Review Angle
- **Audit ISR Math:** Strictly ban floating-point operations inside high-frequency ISRs on microcontrollers without hardware FPUs.
- **Verify Toolchain Flags:** Inspect compiler build flags to ensure hardware FPU utilization on capable silicon.

## Compiler, ABI, and Toolchain Implications
- **Runtime Library Bloat:** Software float runtime routines pull in kilobytes of helper code, bloating ROM footprint.

## Performance, Memory, Timing, and Power
- **Energy Cost:** Executing hundreds of software emulation cycles per math operation drains battery power rapidly in IoT edge devices.

## Verification / Debugging
- **Execution Profiling:** Use cycle counters to measure exact CPU execution time differences between float and fixed-point implementations.

## Safety, Security, and Reliability
- **Deterministic Timing:** Replacing unnecessary floats with fixed-point integer math ensures deterministic worst-case execution time (WCET) in safety-critical firmware.

## Trade-offs and Alternatives
- **Floating-Point vs. Fixed-Point Math:** Fixed-point arithmetic provides near-integer execution speed and determinism on non-FPU hardware.

## Staff-Level Takeaway
Floating point is not free on embedded hardware. If your microcontroller lacks an FPU, floating-point math triggers massive software emulation overhead and timing jitter. Use fixed-point arithmetic for inner control loops on constrained silicon.

## Related Concepts
- [[00_Chapter_Index]]
- [[01_Floating_types]]
- [[03_Precision]]
- [[12_Deterministic_numeric_design]]
