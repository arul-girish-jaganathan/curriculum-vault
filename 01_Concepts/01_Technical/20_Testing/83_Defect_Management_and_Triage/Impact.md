# Impact

## Purpose
Build a practical, engineering-grade understanding of **Impact** and use it to create tests that expose meaningful defects with reproducible evidence.

## Core Model
- **Test object:** identify the function, component, subsystem, system, interface, timing behavior, hardware boundary, or lifecycle state being evaluated.
- **Stimulus:** define inputs, events, environment, configuration, faults, and timing.
- **Oracle:** define how correctness is judged, including tolerances, invariants, temporal properties, or reference behavior.
- **Evidence:** capture enough information to explain pass/fail outcomes and reproduce failures.

## Test Design Questions
1. What requirement, risk, behavior, or failure mode is being tested?
2. What inputs and environmental conditions can change the result?
3. Which boundaries and negative paths matter?
4. What oracle distinguishes correct behavior from merely plausible behavior?
5. What evidence is required to trust the result?

## Execution Model
A durable test normally separates:
- setup and preconditions;
- stimulus;
- observation and synchronization;
- assertions/oracle evaluation;
- cleanup and reset;
- artifact capture.

## Failure Modes
Consider:
- incorrect implementation;
- incorrect requirement or test oracle;
- environment defects;
- instrumentation/measurement errors;
- timing and concurrency races;
- stale configuration or test data;
- hardware variation;
- flaky or nondeterministic execution;
- tests that pass without exercising the intended behavior.

## Reproducibility
Capture the build, source revision, compiler/toolchain, target identity, configuration, test data, random seed, environment, timing-relevant settings, and relevant logs/traces. A failure should be reducible to a useful minimum scenario whenever practical.

## Coverage
Coverage may refer to requirements, features, code structures, states, transitions, faults, interfaces, combinations, timing windows, or operational scenarios. Coverage percentage alone does not demonstrate correctness; identify meaningful gaps and untested risk.

## Embedded / Systems Considerations
Consider interrupts, DMA, MMIO ordering, cache coherency, RTOS scheduling, Linux behavior, boot/reset states, watchdogs, power/thermal conditions, peripheral faults, communication timing, nonvolatile storage, and board-to-board variation where applicable.

## Automation
Automate repeatable setup, execution, synchronization, artifact capture, and result interpretation. Keep the harness deterministic and versioned. Avoid retries that hide real defects; treat unexplained retries as a test-health problem.

## Evidence and Acceptance
A strong test result includes:
- explicit pass/fail criteria;
- captured execution evidence;
- environment and configuration identity;
- traceability to a requirement, risk, or intended behavior;
- reproducibility for failures;
- reviewable results.

## Common Mistakes
- Testing only the happy path.
- Using a weak or ambiguous oracle.
- Overfitting tests to implementation details.
- Confusing code coverage with behavior coverage.
- Ignoring environment reliability.
- Allowing flaky tests to accumulate.
- Changing multiple variables while diagnosing a failure.
- Treating a green suite as proof that no defect exists.

## Staff-Level View
Treat testing as an engineering system: requirements, risk, architecture, testability, automation, evidence, lab infrastructure, CI feedback, defect triage, and lifecycle maintenance should work together to produce justified release confidence.
