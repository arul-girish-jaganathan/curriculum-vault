# 10: Atomicity Limitations

## Definition
Atomicity limitations in bit fields refer to the architectural impossibility of modifying a single bit field within a shared storage unit without reading and rewriting the adjacent bit fields residing in that same unit. In concurrent, multi-threaded, or interrupt-driven environments, this causes silent, catastrophic data races.

## Scope and Boundaries
Covers: Shared storage-unit races, Read-Modify-Write concurrency hazards, thread-safety boundaries, ISR preemption, and memory barriers.
Does not cover: C11 `_Atomic` operations on entire full-width scalar objects.

## Why Does It Exist
Modern microprocessors cannot address individual bits on the memory bus; they address bytes, half-words, or words. To modify a single bit, the processor must load the entire enclosing memory word, mutate the bit in a CPU register, and store the entire word back to RAM.

## Mechanism and Language Rules
1. **Memory Location Definition (ISO C11 §3.14):** A memory location is either an object of scalar type or a maximal sequence of adjacent bit fields. Consecutive bit fields form a single memory location.
2. **C11 Data Race Rule (§5.1.2.4):** Concurrent access to the same memory location by two threads, where at least one access is a modification, constitutes a Data Race and results in Undefined Behavior.
3. **No Bit-Level Locks:** Standard atomic primitives cannot protect a single bit field; synchronization must lock the entire enclosing structure.

## Examples
```c
#include <stdint.h>
#include <stdbool.h>

struct SharedState {
    unsigned int task_ready    : 1; /* Modified by Main Thread */
    unsigned int isr_triggered : 1; /* Modified by Interrupt Service Routine */
    unsigned int fault_code    : 6;
};

volatile struct SharedState g_state;

/* Main Thread Execution */
void main_thread_loop(void) {
    /* 
     * Loads 32-bit word, sets bit 0, writes back 32-bit word.
     * If pre-empted between read and write by ISR, the ISR's write to 
     * isr_triggered will be OVERWRITTEN and permanently lost!
     */
    g_state.task_ready = 1;
}

/* Interrupt Handler (ISR) */
void SysTick_Handler(void) {
    g_state.isr_triggered = 1; /* Data race on adjacent bit field! */
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- Concurrently mutating adjacent bit fields from separate execution contexts (threads, RTOS tasks, or ISRs) without locks invokes Undefined Behavior (Data Race under C11).

## Edge Cases and Failure Modes
- **Phantom State Losses:** An ISR sets a hardware flag on an adjacent bit field. The main thread, unaware of the ISR, writes back its modified copy of the word, silently erasing the ISR's update.
- **Lock-Free Illusions:** Developers assume that because two threads modify distinct named fields (`task_ready` vs `isr_triggered`), no lock is required. Because they share a storage unit, it is a single shared memory location.

## Embedded Implications
- **Interrupt Corruption:** This is one of the most common causes of intermittent, irreproducible heisenbugs in bare-metal embedded systems.
- **Bit-Banding Solution:** On ARM Cortex-M3/M4 cores, the hardware bit-band engine maps individual bits to discrete 32-bit word addresses, allowing atomic single-bit writes:
  `*(volatile uint32_t *)BITBAND_ADDR = 1;`.

## Firmware Review Angle
- Check every struct containing bit fields for concurrent access: Are different bit fields in the same struct modified by both an ISR and thread code?
- Enforce critical sections (`__disable_irq()` / `__enable_irq()`) or mutex locks around any bit-field mutations shared across contexts.

## Compiler, ABI, and Toolchain Implications
- Compilers cannot generate atomic instructions (like `LDREX`/`STREX`) for sub-byte bit fields without locking the entire word container.
- C11 `_Atomic` cannot be applied directly to a bit field: `_Atomic unsigned int flag : 1;` is a constraint violation.

## Performance, Memory, Timing, and Power
- Protecting bit fields with critical sections or mutexes introduces locking latency and interrupts masking overhead, completely negating the memory-saving benefits of bit fields.

## Verification / Debugging
- ThreadSanitizer (`TSan`) flags data races on bit fields in host-simulated environments.
- Hardware trace tools (ETM/SWO) can capture corrupted memory words caused by ISR preemption.

## Safety, Security, and Reliability
- Silent loss of interrupt events due to bit-field data races can cause state machine lockups and safety shutdown failures in industrial systems.

## Trade-offs and Alternatives
- **Separate Variables vs. Bit Fields:** Allocating independent `uint8_t` or `uint32_t` variables for each state flag costs slightly more RAM, but makes each variable an independent memory location that can be updated concurrently without data races.

## Staff-Level Takeaway
Adjacent bit fields share a single memory location. Never allocate flags in the same bit-field struct across different threads or interrupt contexts without explicit synchronization. When concurrency is required, use separate scalar variables or atomic word masks.

## Related Concepts
- `01_Bit_field_declaration`
- `08_MMIO_bit_fields`
- `09_Mask_and_shift_alternatives`
