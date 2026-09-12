# Harness design

> Canonical C topic note — chapter 40.

## Definition
A fuzz or sanitizer harness is a small adapter that converts raw test input into a controlled call to the code under test and defines what constitutes failure.

## Mechanism and language rules
A strong harness initializes required state, bounds input, avoids global nondeterminism, calls one meaningful entry point, and releases resources. It should be cheap enough for millions of executions.

```c
int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size)
{
    parser_feed(data, size);
    return 0;
}
```

The exact API is framework-specific; the engineering principles are general.

## Embedded implications
Wrap protocol and algorithm modules around fake clocks, deterministic storage, bounded allocators, and simulated peripherals. Avoid bringing the entire RTOS/driver stack into every fuzz execution.

## Edge cases and failure modes
- Harness bugs mistaken for product bugs.
- Global state leaking between iterations.
- Unbounded allocations or recursion.
- Failure oracles that detect only crashes and miss invalid state.

## Verification / debugging
Unit-test the harness itself, enforce time/input limits, reset state between cases, and add assertions for invariants. Run with sanitizers and deterministic seeds when reproducing failures.

## Staff-level takeaway
The harness is part of the test architecture. Its fidelity, determinism, and failure oracle determine what the fuzzer can actually prove.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
