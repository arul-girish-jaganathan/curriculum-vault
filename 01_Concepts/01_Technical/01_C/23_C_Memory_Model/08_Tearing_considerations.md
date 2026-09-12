# 08: Tearing Considerations

## Definition
Memory tearing (word tearing) occurs when a read or write operation on an object cannot be completed in a single indivisible memory bus transaction, forcing the processor to execute multiple discrete memory accesses. If preemption, an interrupt, or a concurrent thread accesses the object mid-operation, it observes a corrupted hybrid state consisting of partially updated old and new bytes.

## Scope and Boundaries
Covers: Word tearing, bus alignment requirements, 64-bit variables on 32-bit MCUs, and struct tearing.
Does not cover: Cache coherency protocols across multi-socket servers.

## Why Does It Exist
CPUs have fixed physical bus widths (e.g., 32 bits on ARM Cortex-M, 64 bits on x86_64). When manipulating data types wider than the native bus, or types that span unaligned memory boundaries, the processor emits multiple load or store instructions. Without hardware locks, mid-operation preemption causes torn reads and writes.

## Mechanism and Language Rules
1. **Natural Alignment Rule:** Unaligned objects straddle bus boundaries, forcing the CPU to issue two separate memory cycles to fetch a single scalar.
2. **Double-Word Arithmetic:** On a 32-bit MCU, a 64-bit integer (`uint64_t`) requires two instructions: `STR` (low word) and `STR` (high word), or an `STRD` pair that is NOT guaranteed to be atomic against interrupts.
3. **C11 Protection:** Declaring an object `_Atomic` guarantees that the compiler and hardware prevent tearing, using either atomic bus instructions or internal locks.

## Diagram: Torn Read on 32-Bit Bus
$$\begin{array}{rcc}
\text{Initial Value:} & \texttt{0x00000000\_00000000} & (0) \\[2pt]
\text{Writer writes Low Word:} & \texttt{0x00000000\_FFFFFFFF} & \\\[2pt]
\textbf{--- INTERRUPT / PREEMPTION OCCURS HERE ---} & & \\\[2pt]
\text{Reader reads both words:} & \texttt{0x00000000\_FFFFFFFF} & (4{,}294{,}967{,}295) \\[2pt]
\text{Writer finishes High Word:} & \texttt{0x00000001\_FFFFFFFF} & (8{,}589{,}934{,}591) \\[4pt]
\multicolumn{3}{c}{\textbf{Catastrophic Error: Reader read an impossible intermediate value!}}
\end{array}$$

## Examples
```c
#include <stdint.h>
#include <stdbool.h>
#include <stdatomic.h>
#include <assert.h>

/* TEARING HAZARD on 32-bit MCU */
static uint64_t g_system_microseconds = 0;

void SysTick_Handler(void) {
    /* Emits two 32-bit writes on ARM Cortex-M3/M4! */
    g_system_microseconds += 1000;
}

uint64_t get_time_torn_hazard(void) {
    /* If SysTick interrupts between loading low and high words, reads garbage! */
    return g_system_microseconds;
}

/* IMMUNE TO TEARING: C11 Atomic uint64_t */
static atomic_uint_fast64_t g_atomic_system_us;

uint64_t get_time_safe(void) {
    /* Guaranteed indivisible load: tearing is physically impossible */
    return atomic_load_explicit(&g_atomic_system_us, memory_order_relaxed);
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- Reading a torn value of a non-atomic variable is a manifestation of a Data Race, resulting in Undefined Behavior.

## Edge Cases and Failure Modes
- **Timer Roll-over Glitches:** A torn read on a microsecond timer during roll-over from `0x00000000FFFFFFFF` to `0x0000000100000000` causes the system to jump forward or backward by 4.29 seconds for a single frame, bricking PID control loops.

## Embedded Implications
- **64-Bit Flash Timers in MCUs:** Very common bug in 32-bit ARM Cortex-M firmware when maintaining 64-bit millisecond/microsecond epoch clocks accessed across ISR boundaries.

## Firmware Review Angle
- Audit all 64-bit integer variables accessed across interrupt or thread boundaries on 32-bit processors: are they declared `_Atomic` or read within an interrupt-disabled critical section?
- Ensure packed structures do not cause variables to become misaligned across 4-byte boundaries.

## Compiler, ABI, and Toolchain Implications
- On ARM Cortex-M, the compiler uses `LDREXD`/`STREXD` for atomic 64-bit types if the hardware supports it, guaranteeing tear-free execution.

## Performance, Memory, Timing, and Power
- Preventing tearing via atomics avoids expensive manual interrupt masking (`__disable_irq()`).

## Verification / Debugging
- Inject stress-test interrupts during timer rollover tests to expose tearing vulnerabilities.

## Safety, Security, and Reliability
- Eliminates sensor corruption and timer calculation glitches in safety-critical automotive systems (ISO 26262).

## Trade-offs and Alternatives
- **Atomic 64-bit vs Critical Section:** `atomic_load` on 64-bit types is non-blocking; disabling interrupts around a 64-bit load is an acceptable fallback on architectures lacking 64-bit atomics.

## Staff-Level Takeaway
On 32-bit microcontrollers, 64-bit variables tear when accessed across thread or interrupt boundaries. Never read or write a 64-bit timestamp or metric concurrently without declaring it `_Atomic` or protecting the access inside an interrupt-disabled critical section.

## Related Concepts
- `01_Threads_and_shared_objects`
- `02_Data_races`
- `../22_C_Concurrency_Atomics/02_Atomic_load_store`
