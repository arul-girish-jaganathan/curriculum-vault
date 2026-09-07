# Property Based and Adversarial Testing Performance and Reliability

## Purpose
Explain observer effect, overhead, latency, memory impact, and how debugging changes can mask or expose a defect.

## Core Model
- **Object of observation:** the program, thread, task, driver, hardware block, or system boundary being inspected.
- **Key state:** registers, memory, control flow, scheduling state, I/O state, or external conditions that can influence the symptom.
- **Causal question:** what event or invariant violation could transform a healthy state into the observed failure?

## Practical Debugging Questions
1. What exactly failed, and how is it measured?
2. What evidence existed immediately before the failure?
3. Which hypotheses explain all observed evidence rather than one symptom?
4. What experiment would most efficiently distinguish the leading hypotheses?
5. What observation would falsify the current theory?

## Failure Signatures
- Crash, assertion, exception, hang, corruption, wrong output, timeout, missed deadline, or degraded performance.
- Intermittent versus deterministic behavior should be separated explicitly.
- A symptom may be downstream of the root cause; avoid stopping at the first visible fault.

## Evidence to Capture
- Exact build and symbols.
- Inputs, configuration, firmware/software version, target identity, and timing context.
- Logs, trace events, call stacks, register state, relevant memory, thread/task state, and recent changes.

## Debug Workflow
1. Freeze the known-good baseline.
2. Reproduce with the smallest useful scenario.
3. Capture evidence before changing the system.
4. Form ranked hypotheses.
5. Run the smallest discriminating experiment.
6. Confirm the mechanism, not merely the symptom.
7. Add a regression test or observability improvement.

## Tooling
- Symbolic debugger: GDB/LLDB where applicable.
- Sanitizers and dynamic analysis for supported builds.
- Trace/profiling tools for timing and concurrency problems.
- Hardware probes, logic analyzers, protocol analyzers, or board telemetry for hardware-bound failures.

## Edge Cases
- Compiler optimization can change stepping, variable visibility, and control flow.
- Instrumentation can alter timing and memory layout.
- Heisenbugs may disappear under a debugger; compare intrusive and low-intrusion evidence.

## Embedded / Systems Notes
- Consider interrupts, DMA, cache/coherency, MMIO ordering, reset causes, watchdog behavior, power transitions, and external peripherals when they are in the causal path.

## Prevention
- Convert the confirmed root cause into a test, assertion, invariant, static check, trace point, code review rule, or design constraint.

## Staff-Level View
- Prefer repeatable evidence over intuition.
- Make debugging artifacts reproducible and shareable.
- Push recurring failures upstream into design, build, test, observability, or architecture improvements.
