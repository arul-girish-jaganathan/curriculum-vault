# 32.09 Producer-consumer

## Scope

This is the canonical note for **Producer-consumer** within **Concurrency in Embedded Systems**. The explanation belongs here; other notes should link to this topic rather than duplicate it.

## Core model

Concurrent embedded software includes interrupts, RTOS tasks, DMA engines and multiple cores. Each is an independent actor that can change state outside the current function's control flow.

## Canonical mental model

```text
Task A ----shared state---- Task B
                  ^
             synchronization
```

The diagram/code is only a starting point. Trace the state, ownership and timing through the complete system rather than treating the local operation as isolated.

## What to understand

### Mechanism
Identify the actual state machine behind the feature. For hardware-facing topics, identify registers/signals, sequencing, timing and completion conditions. For software topics, identify data ownership, execution context and error propagation.

### Invariants
Write down what must remain true:
- resource ownership is unambiguous;
- every state transition has a valid predecessor and successor;
- buffers have a single clear producer/consumer rule;
- timing assumptions are explicit;
- error recovery leaves the system in a known state.

### Boundary cases
Study reset, initialization, empty/minimum/maximum values, timeout, partial transfer, repeated invocation, power loss, concurrency and hardware faults where applicable.

### Failure modes
A useful failure description names:
1. trigger;
2. violated invariant;
3. observable symptom;
4. containment;
5. recovery;
6. evidence needed to prove the root cause.

### Debugging
Use the narrowest evidence that can distinguish causes:
- register snapshots;
- fault status;
- trace timestamps;
- logic-analyzer traces;
- bus captures;
- stack snapshots;
- task state;
- memory maps;
- PMU/profiling data;
- power/thermal measurements.

Do not confuse the last visible symptom with the first violated invariant.

### Performance and resource budget

Consider:
- CPU utilization;
- worst-case latency;
- RAM/flash;
- DMA/bus bandwidth;
- stack usage;
- power;
- thermal margin;
- interrupt interference.

Measure the actual product path. A driver that is fast in isolation can still miss a deadline because of bus arbitration, cache state, interrupt masking or competing DMA.

### Verification

Use the appropriate layer:
- static analysis and compile-time checks;
- unit tests with mocks/fakes;
- integration tests;
- target tests;
- fault injection;
- hardware-in-loop;
- production diagnostics.

The more hardware-dependent the behavior, the more important target-level evidence becomes.

## Design review

Ask:
- Who owns the hardware resource?
- Who initializes it?
- Who services its interrupt?
- Who owns each buffer?
- What happens on timeout?
- What happens on reset during the operation?
- Can the operation be retried?
- What happens if the expected device never responds?
- Is the behavior deterministic enough for the product?

## Embedded systems implication

A robust embedded implementation connects the local mechanism to product-level behavior: startup, normal operation, degraded operation, update, shutdown, and recovery.

## Staff-level checkpoint

Be able to explain the requirement, architecture, mechanism, worst-case resource behavior, failure modes, observability and verification evidence for **Producer-consumer** without relying on vendor-specific folklore.

## Related

- [[../01_Embedded_Systems_Foundations/00_Chapter_Index|Embedded Systems Foundations]]
- [[../28_Interrupts/00_Chapter_Index|Interrupts]]
- [[../35_RTOS_Fundamentals/00_Chapter_Index|RTOS Fundamentals]]
- [[../45_Device_Drivers/00_Chapter_Index|Device Drivers]]
- [[../60_Debugging/00_Chapter_Index|Debugging]]
- [[../88_Embedded_Architecture/00_Chapter_Index|Embedded Architecture]]
- [[../90_Staff_Embedded/00_Chapter_Index|Staff-Level Embedded]]

## Source backbone

This knowledge base follows broad embedded-system curriculum themes documented by GeeksforGeeks, including hardware/software/firmware composition, embedded architectures, microprocessors/microcontrollers, peripherals, RTOS, memory, low-power techniques and debugging/testing. citeturn951996search0turn951996search2turn951996search3turn951996search10

Primary references:
- https://www.geeksforgeeks.org/computer-organization-architecture/introduction-of-embedded-systems-set-1/
- https://www.geeksforgeeks.org/computer-organization-architecture/architecture-of-an-embedded-system-set-3/
- https://www.geeksforgeeks.org/electronics-engineering/embedded-c/
