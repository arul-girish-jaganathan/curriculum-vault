# MTTR

## Purpose
Develop an architecture-level understanding of **MTTR**: what problem it solves, what responsibilities it assigns, what boundaries it creates, and how it affects quality attributes and system evolution.

## Core Model
- **Responsibility:** what the architectural element owns and what it deliberately does not own.
- **Boundary:** module, process, task, service, hardware, security, safety, or deployment boundary involved.
- **State:** where authoritative state lives, who owns it, and how its lifetime is controlled.
- **Interaction:** synchronous/asynchronous communication, data flow, control flow, timing, and error semantics.
- **Constraints:** CPU, memory, storage, bandwidth, power, thermal, safety, security, portability, and lifecycle constraints.

## Architecture Questions
1. What architectural driver makes this mechanism necessary?
2. Which quality attributes improve or degrade because of the decision?
3. Where should the responsibility and enforcement point live?
4. What assumptions exist at the boundary?
5. What happens during startup, shutdown, overload, fault, recovery, update, and version skew?
6. How will this architecture be verified and observed?

## Interface and Contract
Define:
- inputs and outputs;
- ownership and lifetime;
- sequencing and concurrency;
- timing and timeout expectations;
- error and recovery semantics;
- security and safety conditions;
- versioning and backward compatibility.

## Failure Modes
Consider:
- single-point failures;
- shared-resource contention;
- stale/corrupt state;
- queue saturation and backpressure;
- partial initialization;
- reset and restart;
- communication loss;
- version skew;
- dependency failure;
- privilege or trust-boundary violations;
- timing deadline misses;
- common-cause failures.

## Quality Attributes
Evaluate the design against:
- performance and latency;
- throughput and capacity;
- reliability and availability;
- safety and security;
- testability and observability;
- maintainability and portability;
- power and thermal behavior;
- operational/serviceability impact.

## Verification
An architecture decision should be testable through appropriate evidence:
- architecture and interface reviews;
- requirements and traceability;
- prototypes or proofs of concept;
- component/integration/system tests;
- fault injection and recovery tests;
- performance measurements;
- security/safety analysis;
- production and field feedback.

## Evolution
Plan for:
- hardware revisions;
- protocol/API/schema changes;
- product variants;
- third-party dependency replacement;
- firmware/software update;
- security patching;
- migration and coexistence;
- deprecation and end of life.

## Common Mistakes
- Starting from a favorite pattern instead of the problem.
- Drawing boxes without defining responsibilities and contracts.
- Creating abstractions that leak hardware or operational assumptions.
- Sharing mutable state without explicit ownership.
- Ignoring failure and recovery paths.
- Optimizing locally without considering system-level quality attributes.
- Treating documentation as architecture while decisions remain implicit.

## Embedded / Systems Considerations
For embedded systems, evaluate MCU/SoC boundaries, RTOS/Linux integration, drivers/BSP/HAL, interrupt and DMA behavior, memory/cache/coherency, boot/update lifecycle, protocol timing, power states, hardware variants, diagnostics, and field recovery where relevant.

## Staff-Level View
Architecture is a set of durable decisions that control change. Make the rationale, alternatives, assumptions, risks, ownership, interfaces, quality-attribute consequences, and validation strategy explicit so the design survives beyond the original implementation team.
