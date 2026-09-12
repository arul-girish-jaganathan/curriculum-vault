# 02: Atomic Load and Store

## Definition
Atomic load and atomic store operations are the fundamental one-way atomic memory access primitives defined in ISO C11. `atomic_load` atomically reads the value of an atomic object, while `atomic_store` atomically replaces it. Crucially, they prevent "word tearing" (reading a half-written value) and allow explicit specification of memory ordering constraints.

## Scope and Boundaries
Covers: `atomic_load()`, `atomic_store()`, `atomic_load_explicit()`, `atomic_store_explicit()`, tearing prevention, and memory order restrictions.
Does not cover: Atomic read-modify-write cycles (see `03_Read_modify_write`).

## Why Does It Exist
Ordinary assignments (`val = g_shared;` or `g_shared = val;`) are not guaranteed to be atomic by the C language standard. On an 8-bit bus or when accessing 64-bit integers on a 32-bit CPU, the compiler splits the operation into multiple machine instructions. An interrupt or thread preemption between these instructions reads a corrupt, partially updated word (torn read). Explicit atomic load/store primitives eliminate this vulnerability.

## Mechanism and Language Rules
1. **Memory Order Restrictions:**
   - `atomic_load_explicit()` accepts: `memory_order_relaxed`, `memory_order_consume`, `memory_order_acquire`, or `memory_order_seq_cst`. (Cannot use `release` or `acq_rel`).
   - `atomic_store_explicit()` accepts: `memory_order_relaxed`, `memory_order_release`, or `memory_order_seq_cst`. (Cannot use `acquire`, `consume`, or `acq_rel`).
2. **Indivisibility Guarantee:** The CPU executes the read or write as an indivisible bus transaction.
3. **No Intermediate Register Caching:** Compilers treat atomic loads as true memory accesses, preventing unsafe register caching across loop iterations.

## Examples
```c
#include <stdatomic.h>
#include <stdint.h>
#include <stdbool.h>

typedef struct {
    atomic_uint_fast32_t sequence_id;
    atomic_bool          sensor_fault;
} SystemTelemetry_t;

static SystemTelemetry_t g_telemetry;

/* Thread A: Sensor Publisher */
void telemetry_update(uint32_t seq, bool fault) {
    /* Explicit store with release semantics: guarantees prior non-atomic writes are visible */
    atomic_store_explicit(&g_telemetry.sensor_fault, fault, memory_order_relaxed);
    atomic_store_explicit(&g_telemetry.sequence_id, seq, memory_order_release);
}

/* Thread B: Monitor Consumer */
bool telemetry_check_healthy(uint32_t *out_seq) {
    /* Explicit load with acquire semantics: pairs with release store */
    uint32_t seq = atomic_load_explicit(&g_telemetry.sequence_id, memory_order_acquire);
    bool fault = atomic_load_explicit(&g_telemetry.sensor_fault, memory_order_relaxed);
    
    *out_seq = seq;
    return !fault;
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- Passing an illegal memory order (e.g., passing `memory_order_release` to `atomic_load`) invokes Undefined Behavior (§7.17.7.2).

## Edge Cases and Failure Modes
- **The Default Operator Trap:** Writing `g_val = x;` on an atomic variable invokes `atomic_store(&g_val, x)` with `memory_order_seq_cst` by default. On ARM, this emits expensive memory barriers (`DMB`), severely degrading real-time performance. Always use `atomic_store_explicit()` with the minimum required ordering.

## Embedded Implications
- **64-Bit Telemetry on 32-Bit MCUs:** Storing a 64-bit timestamp (`uint64_t`) on an ARM Cortex-M4 takes two 32-bit store instructions (`STRD`). Without `atomic_store`, an ISR interrupting between the two instructions reads an invalid timestamp.

## Firmware Review Angle
- Check that all atomic loads and stores use the `_explicit` variant with deliberate memory ordering.
- Verify that `atomic_load` never uses `release` ordering and `atomic_store` never uses `acquire` ordering.

## Compiler, ABI, and Toolchain Implications
- For naturally aligned 32-bit scalars on ARMv7-M, `atomic_load_explicit(relaxed)` emits a single `LDR` instruction, and `atomic_store_explicit(relaxed)` emits a single `STR` instruction.

## Performance, Memory, Timing, and Power
- Relaxed loads/stores execute with zero hardware cycle overhead compared to standard C assignments.

## Verification / Debugging
- ThreadSanitizer detects unsynchronized loads/stores.
- Disassembly inspection: Verify whether `DMB` barrier instructions are emitted.

## Safety, Security, and Reliability
- Eliminates silent torn-read bugs that cause catastrophic telemetry calculation errors or corrupted pointer reads in safety-critical systems.

## Trade-offs and Alternatives
- **Atomic Load/Store vs Disabling Interrupts:** Atomic operations synchronize access without blocking high-priority interrupts, preserving hard real-time latency.

## Staff-Level Takeaway
Always prefer `atomic_load_explicit()` and `atomic_store_explicit()` over bare assignment operators on atomic objects. Specify the minimum required memory order (`relaxed` or `acquire/release`) to avoid the heavy cycle penalties of default `seq_cst` barriers.

## Related Concepts
- `01_Atomic_objects`
- `05_memory_order_relaxed`
- `06_acquire_release`
- `../23_C_Memory_Model/08_Tearing_considerations`
