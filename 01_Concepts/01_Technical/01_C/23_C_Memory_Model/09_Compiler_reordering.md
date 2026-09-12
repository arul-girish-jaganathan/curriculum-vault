# 09: Compiler Reordering

## Definition
Compiler reordering is the aggressive optimization process wherein the compiler rearranges, merges, vectorizes, hoists, sinks, or eliminates memory read and write operations during code generation. Under the "as-if" rule (ISO C11 §5.1.2.3), the compiler is legally permitted to execute operations in any order it chooses, provided that the observable behavior of a single-threaded program remains identical.

## Scope and Boundaries
Covers: The as-if rule, optimization passes, register caching, instruction hoisting/sinking, compiler memory barriers (`asm volatile("" ::: "memory")`), and C11 atomic barriers.
Does not cover: Hardware CPU pipeline reordering (see `10_Hardware_ordering`).

## Why Does It Exist
Modern microprocessors execute instructions much faster than memory bus latency. Compilers reorder instructions to schedule memory loads early (hiding memory latency), maximize register utilization, keep arithmetic pipelines full, and eliminate redundant memory bus accesses.

## Mechanism and Language Rules
1. **The As-If Rule:** The compiler must preserve observable single-threaded behavior (I/O, volatile accesses, program outputs), but has complete freedom over non-observable memory ordering.
2. **Compiler Memory Barrier:** A compiler barrier prevents the compiler from moving memory operations across the barrier during optimization passes:
   `__asm__ __volatile__("" ::: "memory");` (GCC/Clang).
3. **Atomic Barriers Imply Compiler Barriers:** Every C11 atomic operation with `acquire`, `release`, or `seq_cst` semantics acts as an automatic, built-in compiler optimization barrier.

## Examples
```c
#include <stdbool.h>

/* COMPILER REORDERING HAZARD */
int  g_hardware_buffer = 0;
bool g_transfer_done = false;

void send_packet_buggy(void) {
    g_hardware_buffer = 0xAA; /* Write 1 */
    g_transfer_done = true;    /* Write 2 */
    
    /* 
     * COMPILER REORDERING:
     * The compiler sees that Write 1 and Write 2 access independent memory.
     * Under -O2 or -O3, the compiler is legally entitled to emit Write 2 FIRST!
     * If an interrupt fires after Write 2 but before Write 1, the receiver reads garbage!
     */
}

/* COMPLIANT FIX: Compiler memory barrier or C11 Atomic */
void send_packet_safe(void) {
    g_hardware_buffer = 0xAA;
    
    /* Compiler barrier: prevents hoisting or sinking memory operations across this point */
    __asm__ __volatile__("" ::: "memory");
    
    g_transfer_done = true;
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- Relying on source code statement ordering to guarantee memory write sequences in multi-threaded code invokes Undefined Behavior (Data Race).

## Edge Cases and Failure Modes
- **Loop Hoisting of Shared Variables:**
  ```c
  while (!g_stop_requested) { do_work(); }
  ```
  If `g_stop_requested` is non-atomic and non-volatile, the compiler hoists the read outside the loop: `if (!g_stop_requested) while(1) do_work();`, freezing the thread permanently.

## Embedded Implications
- **Peripheral DMA Triggering:** Setting up DMA configuration registers and then triggering the enable bit can be reordered by the compiler, starting DMA before memory addresses are configured.

## Firmware Review Angle
- Check that all multi-threaded communication points enforce compiler ordering using C11 atomics or explicit compiler barriers.
- Watch out for aggressive `-O3` and Link-Time Optimization (LTO) passes, which expose latent reordering bugs.

## Compiler, ABI, and Toolchain Implications
- Compiler barriers inform the compiler's intermediate representation (IR) scheduler that memory aliasing state is clobbered, forcing spilled registers to be written back to stack/RAM.

## Performance, Memory, Timing, and Power
- Compiler barriers cost ZERO CPU clock cycles and emit ZERO machine instructions; they restrict only compile-time instruction scheduling.

## Verification / Debugging
- Inspect generated assembly (`gcc -S -O2`) to verify whether instructions were reordered relative to the C source lines.

## Safety, Security, and Reliability
- Eliminates compiler optimization artifacts that break communication protocols in safety-critical systems.

## Trade-offs and Alternatives
- **Compiler Barrier vs CPU Barrier:** A compiler barrier (`::: "memory"`) stops only the *compiler* from reordering. On weakly ordered CPUs (ARM), the *hardware* can still reorder the writes unless a CPU barrier (`DMB`) is emitted. C11 atomics handle BOTH compiler and hardware barriers simultaneously.

## Staff-Level Takeaway
Source code order does not dictate compiler emission order. Compilers will aggressively rearrange independent memory writes under `-O2` and `-O3`. Use C11 atomics with acquire-release semantics to enforce both compile-time and run-time ordering across execution boundaries.

## Related Concepts
- `03_Happens_before`
- `10_Hardware_ordering`
- `11_Volatile_is_not_synchronization`
