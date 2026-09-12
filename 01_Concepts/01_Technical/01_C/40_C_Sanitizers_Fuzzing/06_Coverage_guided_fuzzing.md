# Coverage-guided fuzzing

## Definition
**Coverage-guided fuzzing (CGF)** repeatedly executes a test harness with mutated inputs and uses code-coverage feedback to retain inputs that reach new program paths. Modern fuzzers combine mutation, corpus evolution, execution feedback, and crash/timeout detection.

## Scope and boundaries
Fuzzing is an automated input-exploration technique, not a proof of correctness. Coverage is an imperfect proxy for behavior: high line coverage can still miss important value combinations, state transitions, concurrency schedules, and hardware interactions.

## Mechanism and language rules
A conceptual loop is:

```text
seed corpus -> mutate -> execute -> observe coverage
                 |                 |
                 +-- new path -----+-> corpus
                 +-- crash/timeout -> artifact
```

For C, sanitizer instrumentation is often paired with fuzzing so an unusual input produces an actionable memory or undefined-behavior report.

## Embedded implications
Excellent targets include packet decoders, command interpreters, file formats, boot metadata parsers, configuration loaders, and serialization code. Hardware dependencies should be abstracted so the parser can execute rapidly on a host.

For target-specific fuzzing, inputs may be injected through UART, CAN, USB, network, flash images, or a custom transport, but execution speed and observability are usually much worse than host fuzzing.

## Edge cases and failure modes
- Harness does not reach meaningful code.
- Fuzzer optimizes for shallow coverage rather than semantic states.
- Invalid inputs are rejected before interesting parser logic.
- Global state is not reset between iterations.
- Timeouts are ignored or treated as ordinary slow cases.

## Verification / debugging
Combine CGF with ASan/UBSan where practical. Save every crash, timeout, and reproducer. Measure coverage growth and corpus quality. Make the harness deterministic enough that a saved input reproduces the same defect.

## Performance, memory, timing and power
Fuzzing benefits from millions of executions, so process startup and heavyweight initialization should be minimized. Sanitizers increase per-input cost but greatly improve bug detection. Target fuzzing is slower but can expose hardware-specific behavior.

## Staff-level takeaway
A productive fuzzing program is a **system**, not a command line: high-quality harness, sanitizer instrumentation, useful seed corpus, reproducible artifacts, coverage feedback, and disciplined triage are all required.