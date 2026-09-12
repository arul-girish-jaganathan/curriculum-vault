# Harness design

## Definition
A **fuzzing harness** is the controlled adapter that turns arbitrary input bytes into an invocation of the code under test. Good harness design determines whether a fuzzer explores meaningful behavior or merely exercises initialization and input rejection.

## Scope and boundaries
The harness should be small, deterministic, resettable, and faithful to the real API contract. It should not “fix” malformed input before the target parser sees it, because that can remove the very cases fuzzing is intended to explore.

## Mechanism and language rules
A conceptual harness is:

```c
int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size)
{
    parser_reset();
    parser_consume(data, size);
    return 0;
}
```

The exact fuzzing API is tool-specific, but the principles are general: bounded input, clean state, deterministic behavior, and no dependence on persistent process state unless that state is intentionally part of the test model.

## Embedded implications
For firmware modules, isolate hardware behind interfaces. A parser harness can replace UART, flash, clock, allocator, or transport dependencies with deterministic fakes. For stateful protocols, define how a fuzz iteration begins and ends and whether a sequence of messages is itself the fuzz input.

## Edge cases and failure modes
- State from one iteration contaminates the next.
- Harness leaks memory or file descriptors.
- Randomness makes crashes difficult to reproduce.
- Input is copied into a fixed buffer without checking size.
- Expensive initialization dominates execution.
- Assertions or logging terminate exploration prematurely without preserving the input.

## Verification / debugging
First write ordinary unit tests for valid and invalid cases, then fuzz the same harness. Ensure every discovered failure can be rerun from the saved input. Add assertions about parser invariants and use ASan/UBSan for memory/arithmetic defects.

## Performance, memory, timing and power
A harness should minimize per-input overhead. Avoid heap churn when possible and reuse deterministic state carefully. Fast reset strategies can improve fuzz throughput dramatically, but they must not hide lifecycle bugs.

## Staff-level takeaway
The harness is the **experimental boundary**. Its quality determines what behavior is actually being tested; treat its assumptions and reset model as production-level test infrastructure.