# 12: Memory Model Debugging

## Definition
Memory model debugging is the systematic methodology for detecting, diagnosing, and eliminating concurrency defects—such as data races, memory visibility failures, store buffer reordering glitches, and deadlocks—in multi-threaded and interrupt-driven software systems.

## Scope and Boundaries
Covers: Dynamic analysis with ThreadSanitizer (`TSan`), static analysis tools, disassembly barrier inspection, and hardware execution trace.
Does not cover: High-level OS memory leak detection (Valgrind Memcheck).

## Why Does It Exist
Concurrency bugs are notoriously non-deterministic ("heisenbugs"): they appear once in 10,000 cycles, vanish when a debugger is attached or printfs are added, and fail unpredictably under temperature or bus contention stress. Defeating them requires toolchain-assisted mathematical verification and systematic hardware tracing.

## Diagnostic Toolkit
1. **ThreadSanitizer (TSan):** Host-based instrumentation tool (`-fsanitize=thread`) that tracks memory access timestamps and vector clocks, reporting the exact source lines of unsynchronized concurrent accesses.
2. **Disassembly Barrier Auditing:** Inspecting assembly output (`objdump -d`) to verify that the compiler emitted required hardware barriers (`DMB`, `DSB`) for atomic release/acquire operations.
3. **Hardware Instruction Trace (ETM / ITM):** Using embedded hardware trace probes to capture exact cycle-by-cycle memory transactions without altering execution timing.

## Examples
```bash
# 1. Compile host test harness with ThreadSanitizer
gcc -fsanitize=thread -g -O1 -pthread test_concurrency.c -o test_concurrency

# 2. Run test to capture race reports
./test_concurrency

# Example TSan Diagnostic Output:
# ==================
# WARNING: ThreadSanitizer: data race (pid=4521)
#   Write of size 4 at 0x7fff5fbff688 by thread T1:
#     #0 worker_task test_concurrency.c:24 (test_concurrency+0x1234)
#   Previous Read of size 4 at 0x7fff5fbff688 by thread T2:
#     #0 monitor_task test_concurrency.c:38 (test_concurrency+0x5678)
#   Location is global 'g_telemetry_val' of size 4 at 0x7fff5fbff688
# ==================

# 3. Disassembly Barrier Verification for ARM Cortex-M4
arm-none-eabi-objdump -d build/firmware.elf | grep -B 2 -A 2 "dmb"
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- TSan works by intercepting POSIX pthread and C11 atomics; attempting to run TSan on code that uses raw inline assembly without compiler memory annotations can produce false negatives.

## Edge Cases and Failure Modes
- **The Printf Masking Trap:** Adding `printf()` or logging statements to debug a race condition changes cache line timing and inserts full I/O barriers, masking the bug during debugging sessions.
- **Simulator False Sense of Security:** Running tests on an x86 host hides weakly ordered memory bugs that trigger only on physical ARM/RISC-V silicon.

## Embedded Implications
- **Hardware Trace (ETM):** On microcontrollers where TSan cannot run directly in bare-metal ROM, Embedded Trace Macrocell (ETM) hardware streams instruction flow to an external debugger (e.g., SEGGER J-Trace) without adding a single cycle of probe overhead.

## Firmware Review Angle
- Confirm that multi-threaded modules are compiled and executed under `-fsanitize=thread` on PC simulator test suites as part of the automated CI/CD pipeline.
- Ensure that debug logging is NOT added to suspected race condition paths during diagnosis.

## Compiler, ABI, and Toolchain Implications
- `-fsanitize=thread` increases binary size by ~2x and execution time by ~2-5x, requiring dedicated simulation builds.

## Performance, Memory, Timing, and Power
- Eliminating race conditions prevents hard faults, watchdog resets, and intermittent bus stalls in deployed products.

## Verification / Debugging
- Automate concurrency stress loops in CI: run test cases in 100,000-iteration loops under randomized thread preemption delays (`usleep(rand() % 100)`).

## Safety, Security, and Reliability
- Compliance with ISO 26262 Part 6 requires rigorous evidence of race-free concurrency in ASIL-D certified firmware.

## Trade-offs and Alternatives
- **Dynamic Sanitizers vs Formal Proofs:** Sanitizers catch defects that actually execute; combining TSan with formal code reviews against the C11 memory model ensures complete coverage.

## Staff-Level Takeaway
Never attempt to debug concurrency bugs by adding printfs—it masks the timing bug you are hunting. Compile your logic for host simulation with `-fsanitize=thread`, verify ARM disassembly for proper `DMB` barrier emission, and utilize non-intrusive hardware trace (ETM) on physical silicon.

## Related Concepts
- `02_Data_races`
- `03_Happens_before`
- `10_Hardware_ordering`
- `../22_C_Concurrency_Atomics/12_Atomic_API_design`
