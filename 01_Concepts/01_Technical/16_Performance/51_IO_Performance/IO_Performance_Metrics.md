# IO Performance Metrics

## Purpose
Build a precise mental model for **IO Performance Metrics** and use it to make performance decisions based on evidence rather than intuition.

## Core Model
- **What is measured:** identify the observable quantity and its units.
- **Causal path:** identify the software, hardware, scheduling, I/O, memory, or power mechanisms that can change the measurement.
- **Bottleneck:** determine which constrained resource limits the observed result.
- **Scope:** separate microbenchmark, component, subsystem, and end-to-end effects.

## Key Questions
1. What exact metric is changing?
2. Is the workload representative, steady, cold-start, bursty, or worst case?
3. Which resource is saturated or on the critical path?
4. What evidence distinguishes CPU, memory, I/O, synchronization, thermal, power, and software causes?
5. Does the optimization improve the target metric without moving the bottleneck elsewhere?

## Measurement
Capture:
- baseline and comparison build/version
- workload and input characteristics
- CPU frequency and affinity where relevant
- memory and cache state where relevant
- concurrency and queue depth
- timing method and sampling/instrumentation overhead
- repetitions, distribution, and tail percentiles
- environmental conditions such as thermal state and background activity

## Analysis Workflow
1. Define the performance objective.
2. Establish a trusted baseline.
3. Characterize the workload.
4. Measure end to end before drilling into a subsystem.
5. Identify the dominant bottleneck.
6. Form a mechanism-based hypothesis.
7. Change one meaningful variable.
8. Re-measure with the same harness and conditions.
9. Check for bottleneck migration and regressions.
10. Record the causal explanation and validation evidence.

## Failure Modes
- Optimizing a non-critical path.
- Reporting averages when tail latency is the real requirement.
- Comparing cold and warm runs.
- Ignoring frequency, thermal, or scheduler state.
- Confusing correlation with causation.
- Letting profiling overhead change the workload.
- Treating a microbenchmark result as proof of system-level improvement.

## Embedded / Systems Considerations
Consider interrupts, DMA, cache coherency, memory bandwidth, MMIO, RTOS scheduling, Linux scheduling, driver queues, power states, DVFS, thermal throttling, boot sequencing, and peripheral contention where they are part of the causal path.

## Validation
A performance change is credible when:
- the benchmark is repeatable;
- the measured effect exceeds expected noise;
- the mechanism matches the observed counters or traces;
- the benefit appears on representative workloads;
- functionality and resource budgets remain acceptable;
- the result survives a clean independent run.

## Trade-offs
Performance may trade against code size, RAM, power, thermal margin, determinism, maintainability, portability, or safety. Optimize the system objective, not an isolated metric.

## Staff-Level View
Treat performance as an engineering system: requirements, budgets, workload models, measurement infrastructure, bottleneck analysis, regression gates, and architectural choices should connect end to end. The goal is not merely a faster function; it is a predictable and sustainable system.
