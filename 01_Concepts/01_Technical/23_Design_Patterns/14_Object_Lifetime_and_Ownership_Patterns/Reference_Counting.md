# Reference Counting

## Purpose
Understand **Reference Counting** as a reusable design mechanism: the problem it addresses, the forces that shape the choice, the structure of the solution, and the consequences it introduces.

## Intent and Context
Identify the recurring design problem, the context in which it appears, and the conditions under which the pattern is actually justified.

## Structure
Describe:
- responsibilities;
- participants;
- ownership and lifecycle;
- interfaces and contracts;
- collaboration and control flow;
- state and data movement;
- extension points.

## Forces and Tradeoffs
Evaluate:
- coupling and cohesion;
- runtime and memory cost;
- compile-time complexity;
- testability and observability;
- concurrency and timing;
- reliability, safety, and security;
- portability and maintainability.

## Implementation Guidance
Choose an implementation that preserves the pattern's intent without copying incidental structure from examples. Keep ownership explicit and make failure behavior part of the design.

## Failure Modes
Watch for:
- pattern applied outside its context;
- accidental indirection;
- hidden dependencies;
- lifecycle bugs;
- reentrancy or concurrency hazards;
- excessive configuration;
- performance overhead;
- pattern combinations that create emergent complexity.

## Testing
Test the behavior that the pattern is meant to guarantee:
- interface contracts;
- lifecycle;
- error paths;
- concurrency;
- timing;
- resource exhaustion;
- variant behavior;
- failure recovery where applicable.

## Performance and Resource Impact
Measure before optimizing. Consider allocations, dispatch cost, cache behavior, queue depth, locking, wakeups, copies, code size, and instrumentation overhead as applicable.

## Embedded / Systems Consequences
For embedded systems, explicitly consider interrupts, DMA, MMIO, RTOS scheduling, boot/lifecycle state, watchdogs, power modes, hardware variants, driver boundaries, and deterministic resource limits.

## Alternatives and Anti Patterns
A pattern should earn its complexity. Prefer a simpler direct implementation when the variation, indirection, or coordination that the pattern provides is not actually needed.

## Staff-Level Reasoning
Explain not only how the pattern works, but why it is the right abstraction for the system, what risks it introduces, how it interacts with neighboring patterns, and when the team should deliberately avoid it.
