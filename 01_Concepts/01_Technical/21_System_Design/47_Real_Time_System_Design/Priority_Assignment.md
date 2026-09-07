# Priority Assignment

## Purpose
Develop a system-design level understanding of **Priority Assignment**: what problem it solves, where it belongs in the architecture, what assumptions it makes, and how the choice affects performance, safety, security, reliability, testability, cost, and lifecycle.

## Core Model
- **Responsibility:** define the exact responsibility owned by the component or mechanism.
- **Boundary:** identify what is inside the subsystem and what remains external.
- **State and data:** identify owned state, inputs, outputs, persistence, and flow.
- **Control path:** identify who triggers work, who owns decisions, and how control propagates.
- **Resources:** account for CPU, memory, bandwidth, storage, power, thermal margin, timing, and human/operational constraints.
- **Failure behavior:** define how faults are detected, contained, reported, recovered from, or allowed to degrade functionality.

## Requirements and Design Questions
1. What user, product, or system requirement drives the design?
2. Which quality attributes matter most and what are their budgets?
3. What interfaces must remain stable?
4. What are the dominant bottlenecks or failure domains?
5. Which assumptions are unverified and could invalidate the architecture?
6. What happens during startup, shutdown, overload, reset, update, and recovery?

## Architecture Options
Compare alternatives using explicit criteria:
- complexity;
- timing and throughput;
- memory and storage;
- power and thermal behavior;
- safety and security;
- fault containment;
- testability and observability;
- portability and reuse;
- manufacturing and field-service impact;
- lifecycle and migration cost.

## Interface Contracts
Define:
- inputs and outputs;
- ownership and lifetime;
- sequencing;
- concurrency expectations;
- timing and timeout behavior;
- error semantics;
- versioning and compatibility;
- security/safety conditions at the boundary.

## Failure Modes
Consider:
- single-point failures;
- shared-resource contention;
- stale or corrupt state;
- timeout and retry storms;
- queue saturation;
- partial initialization;
- power loss and reset;
- communication loss;
- version skew;
- common-cause failures;
- security boundary violations;
- unsafe degraded modes.

## Performance and Resource Impact
Identify critical paths, queueing, data movement, cache behavior, synchronization, scheduling, I/O, memory footprint, code size, power states, thermal limits, and resource headroom. Separate average behavior from worst-case or tail requirements.

## Verification and Validation
Architecture should be testable through:
- requirement-to-design traceability;
- interface tests;
- simulation or modeling where useful;
- SIL/PIL/HIL or target testing;
- fault injection;
- performance measurements;
- safety/security verification;
- startup/recovery/update scenarios.

## Embedded / Systems Considerations
For embedded systems, explicitly evaluate MCU/SoC boundaries, boot flow, memory map, interrupts, DMA, MMIO, caches/coherency, RTOS/Linux integration, drivers/BSP, protocols, storage, power/thermal states, manufacturing, and field recovery as applicable.

## Evolution
A good architecture anticipates:
- hardware revisions;
- protocol and API versioning;
- feature variants;
- supplier or component replacement;
- firmware/software updates;
- security patching;
- lifecycle migration;
- deprecation and end of life.

## Common Mistakes
- Starting with technology instead of requirements.
- Treating diagrams as architecture without documenting contracts and rationale.
- Ignoring failure behavior and recovery.
- Designing only the nominal path.
- Sharing state across boundaries without clear ownership.
- Underestimating integration and bring-up complexity.
- Optimizing a subsystem without considering system-level bottlenecks.

## Staff-Level View
Make the architecture explainable, reviewable, evolvable, and evidence-driven. Explicitly record alternatives, tradeoffs, assumptions, risks, ownership, and verification strategy so that the design remains maintainable beyond the original implementation team.
