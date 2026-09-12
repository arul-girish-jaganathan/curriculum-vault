# 10: Hardware Memory Ordering

## Definition
Hardware memory ordering refers to the physical sequence in which a CPU core's memory execution pipeline commits read and write transactions to the system memory bus and cache hierarchy. On weakly ordered microprocessor architectures (e.g., ARM Cortex-A, Cortex-M7, RISC-V, PowerPC), the CPU hardware dynamically reorders memory transactions at runtime to maximize pipeline and bus throughput.

## Scope and Boundaries
Covers: Weakly ordered vs strongly ordered architectures, store buffers, out-of-order execution, hardware memory barriers (`DMB`, `DSB`, `ISB`), and cache coherency.
Does not cover: Software compiler reordering (see `09_Compiler_reordering`).

## Why Does It Exist
DRAM and system buses are hundreds of times slower than CPU arithmetic cores. To prevent the core from stalling on every memory write, CPUs utilize out-of-order execution pipelines, speculative execution, and asynchronous Store Buffers. While this maximizes single-threaded execution speed, it causes other CPU cores and DMA engines to observe memory operations out of order.

## Architecture Comparison
| Architecture | Memory Model | Loads Reordered with Loads? | Stores Reordered with Stores? | Overhead of Full Barrier |
| :--- | :--- | :--- | :--- | :--- |
| **x86 / x86_64** | Strongly Ordered (TSO) | No | No | Low (stores only: `MFENCE`) |
| **ARMv7-M / ARMv8-M** | Weakly Ordered | **Yes** | **Yes** | Medium (`DMB`) |
| **ARMv8-A (Multi-Core)**| Weakly Ordered | **Yes** | **Yes** | High (`DMB ISH`) |
| **RISC-V (RVWMO)** | Weakly Ordered | **Yes** | **Yes** | Medium (`FENCE`) |

## Examples
```c
#include <stdint.h>
#include <stdbool.h>

/* HARDWARE REORDERING HAZARD ON WEAKLY ORDERED HARDWARE (ARM / RISC-V) */
static int  g_telemetry_data = 0;
static bool g_telemetry_valid = false;

/* Multi-Core Processor: Core 0 */
void core0_producer(void) {
    g_telemetry_data = 1234;
    
    /* 
     * COMPILER BARRIER IS NOT ENOUGH HERE!
     * Even if compiler emits 'STR data' followed by 'STR valid',
     * the ARM hardware store buffer may commit 'valid' to the AXI bus
     * BEFORE 'data' finishes draining!
     */
    __asm__ __volatile__("" ::: "memory"); /* Compiler only! */
    
    /* HARDWARE BARRIER REQUIRED */
    #if defined(__arm__) || defined(__aarch64__)
    __asm__ volatile("dmb ish" ::: "memory"); /* Data Memory Barrier */
    #endif

    g_telemetry_valid = true;
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- Relying on sequential memory arrival on a weakly ordered CPU without hardware barriers produces race conditions and Undefined Behavior in ISO C.

## Edge Cases and Failure Modes
- **Store Buffer Bypassing:** A store instruction is placed into a local CPU store buffer while the core continues executing subsequent instructions. A neighboring core reads main memory before the store buffer flushes, observing stale data.

## Embedded Implications
- **ARM Memory Barriers:**
  - `DMB` (Data Memory Barrier): Ensures all prior memory transactions complete before subsequent memory transactions start.
  - `DSB` (Data Synchronization Barrier): Halts instruction execution until all prior memory accesses complete (essential before entering sleep or executing `SEV`).
  - `ISB` (Instruction Synchronization Barrier): Flushes CPU instruction prefetch pipeline (essential after updating MPU or vector tables).

## Firmware Review Angle
- Confirm that cross-core communication on multi-core microcontrollers (e.g., STM32H7 dual-core, RP2040) uses C11 atomics or explicit hardware memory barriers (`DMB`).
- Verify that DMA descriptors are finalized with `DSB` before triggering DMA channel start registers.

## Compiler, ABI, and Toolchain Implications
- When compiling C11 atomics (`acquire`, `release`, `seq_cst`), the compiler automatically emits the appropriate hardware memory barrier instructions (`DMB`) for the target architecture.

## Performance, Memory, Timing, and Power
- Hardware barriers stall execution pipelines for several clock cycles while bus queues drain. Use targeted acquire-release ordering to minimize barrier frequency.

## Verification / Debugging
- Hard to detect on simulators; test on silicon hardware under maximum bus stress (e.g., DMA saturated transfers).

## Safety, Security, and Reliability
- Critical for safety-critical multi-core embedded systems (ISO 26262 ASIL-D).

## Trade-offs and Alternatives
- **Manual Assembly Barriers vs C11 Atomics:** Writing inline assembly `dmb` is non-portable. C11 atomics automatically emit the exact, optimal hardware barrier for whatever chip you compile for.

## Staff-Level Takeaway
On weakly ordered CPUs (ARM, RISC-V), hardware store buffers and execution pipelines reorder memory bus transactions dynamically. Never rely on compiler barriers alone for inter-core communication. Use C11 atomics to emit the correct hardware memory barriers (`DMB`) automatically.

## Related Concepts
- `09_Compiler_reordering`
- `11_Volatile_is_not_synchronization`
- `../22_C_Concurrency_Atomics/06_acquire_release`
