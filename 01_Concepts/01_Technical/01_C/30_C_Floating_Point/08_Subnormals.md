# 08: Subnormals

## Definition
Subnormal numbers (formerly known as denormalized numbers) are positive and negative floating-point values that are smaller in magnitude than the minimum normal number representable by the format. They allow gradual underflow by sacrificing precision, preventing abrupt underflow to exact zero.

## Scope and Boundaries
- **Covers:** Gradual underflow, subnormal representation, performance traps, and flush-to-zero (FTZ) / denormals-are-zero (DAZ) hardware modes.
- **Does not cover:** Normal floating types, NaNs and infinities, or rounding modes.

## Why Does It Exist
Without subnormals, numbers falling below the minimum normal exponent abruptly drop to zero, causing relative error to jump from machine epsilon to 100%:
- **Gradual Underflow:** Maintains precision gracefully as values approach zero.
- **Mathematical Continuity:** Prevents premature division-by-zero errors or sudden loss of tracking in recursive numerical filters.

## Mechanism and Language Rules
- **Representation:** In subnormal numbers, the implicit leading mantissa bit is `0` (whereas normal numbers have an implicit leading `1`). The exponent field is set to its minimum value.
- **Performance Penalty:** Processing subnormal numbers in hardware without microcode assistance can cause severe execution stalls (taking hundreds of CPU cycles per instruction) on certain CPU architectures.

## Examples
```c
#include <stdio.h>
#include <math.h>
#include <float.h>

int main(void) 
{
    double sub = DBL_MIN / 2.0;

    printf("DBL_MIN = %e\n", DBL_MIN);
    printf("Subnormal value = %e\n", sub);

    int cls = fpclassify(sub);
    if (cls == FP_SUBNORMAL) {
        printf("Value is FP_SUBNORMAL\n");
    } else {
        printf("Value is normal or other\n");
    }

    return 0;
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- **Implementation-Defined:** Whether hardware handles subnormal arithmetic natively in full speed or traps them into microcode emulation routines, causing massive latency spikes.

## Edge Cases and Failure Modes
- **Subnormal Performance Stalls:** Real-time audio processing, control loops, and high-frequency trading algorithms experience catastrophic latency jitter when audio signals or sensor errors decay into subnormal ranges.

## Embedded Implications
- **Cortex-M FPUs:** Many ARM Cortex-M FPUs handle subnormals in hardware, but older or constrained implementations trap subnormals, destroying real-time deterministic timing guarantees. Engineers often enable Flush-To-Zero (FTZ) and Denormals-Are-Zero (DAZ) control bits.

## Firmware Review Angle
- **Enable FTZ/DAZ in Real-Time Code:** In hard real-time control loops or audio firmware, explicitly configure FPU control registers to flush subnormals to zero to eliminate unpredictable timing jitter.

## Compiler, ABI, and Toolchain Implications
- **Fast-Math Flags:** Compiler flags like `-ffast-math` or `-funsafe-math-optimizations` frequently enable FTZ/DAZ hardware modes globally.

## Performance, Memory, Timing, and Power
- **Latency Spikes:** A single subnormal floating-point multiplication can stall a CPU pipeline for 100–1000 cycles, ruining determinism in hard real-time systems.

## Verification / Debugging
- **Performance Profiling:** Use hardware timer counters to measure execution duration of numerical functions when inputs decay into subnormal ranges.

## Safety, Security, and Reliability
- **Hard Real-Time Compliance:** Unmitigated subnormal performance stalls violate worst-case execution time (WCET) bounds required in safety-critical hard real-time systems.

## Trade-offs and Alternatives
- **Gradual Underflow vs. Flush-To-Zero:** Subnormals provide mathematical rigor (gradual underflow); Flush-To-Zero provides deterministic execution speed and stable real-time timing. Real-time embedded systems almost always choose FTZ.

## Staff-Level Takeaway
Subnormals are mathematically elegant but performance killers in real-time embedded systems. Understand how your target MCU handles subnormal arithmetic, and actively enable Flush-To-Zero (FTZ) / Denormals-Are-Zero (DAZ) if your real-time deadline jitter requires absolute determinism.

## Related Concepts
- [[00_Chapter_Index]]
- [[01_Floating_types]]
- [[09_Exceptions_and_fenv]]
- [[11_Embedded_floating_point_cost]]
