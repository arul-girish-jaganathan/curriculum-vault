# Unit Delay

## Purpose
Build a practical, engineering-grade understanding of **Unit Delay** for control-system design, estimation, and real-time embedded implementation.

## Core Model
- **Plant:** what physical process is being controlled and what dynamics dominate.
- **Controller:** what control law transforms reference/feedback into an actuator command.
- **Estimator:** what hidden state, bias, disturbance, or parameter must be inferred.
- **Measurement:** what sensors observe, including delay, noise, bias, bandwidth, and sampling.
- **Constraints:** actuator limits, sample rate, computation time, power, safety, and operating range.

## Key Questions
1. What is the control objective: tracking, regulation, disturbance rejection, stabilization, or optimization?
2. What model and assumptions are being used?
3. What are the dominant time constants, delays, poles, zeros, and nonlinearities?
4. What uncertainty and noise can invalidate the design?
5. Can the algorithm execute with deterministic timing on the target?

## Modeling
Start with the simplest model that explains the behavior:
- physical assumptions;
- inputs, outputs, and state variables;
- operating point;
- parameters;
- linearized or nonlinear dynamics;
- uncertainty and validation limits.

Separate model fidelity from model usefulness. A complex model that cannot be identified or executed reliably is not automatically a better engineering model.

## Stability and Performance
Evaluate:
- closed-loop stability;
- transient response;
- steady-state error;
- bandwidth;
- gain/phase margin;
- disturbance rejection;
- noise amplification;
- actuator effort;
- delay and jitter sensitivity.

For nonlinear systems, distinguish local conclusions around an operating point from global claims.

## Estimation
Where state is not directly measured, define:
- state vector;
- process model;
- measurement model;
- process-noise model;
- measurement-noise model;
- covariance assumptions;
- initialization;
- innovation/residual behavior;
- outlier and fault handling.

## Discrete-Time / Embedded Implementation
Account for:
- sample period;
- zero-order hold;
- computation delay;
- scheduling jitter;
- sensor timestamp;
- actuator update timing;
- quantization;
- fixed-point scaling;
- numerical conditioning;
- execution-time margin.

## Failure Modes
Consider:
- unstable tuning;
- sensor bias or drift;
- actuator saturation;
- integral windup;
- model mismatch;
- noisy derivative action;
- estimator divergence;
- covariance inconsistency;
- delayed measurements;
- missed deadlines;
- aliasing;
- quantization-induced limit cycles;
- calibration changes.

## Validation
Use progressively stronger evidence:
1. analytical checks;
2. simulation and model validation;
3. software tests;
4. SIL/PIL/HIL;
5. real-hardware measurement;
6. environmental and corner-case testing.

Use step, ramp, impulse, frequency-sweep, disturbance, saturation, noise, fault, and long-duration tests as appropriate.

## Performance and Resource Impact
Measure execution time, CPU load, memory, sensor/actuator bandwidth, DMA cost, numerical precision, power consumption, and worst-case timing. Distinguish algorithmic complexity from data-movement and scheduling cost.

## Safety / Robustness
Define safe behavior for sensor faults, actuator limits, estimator failure, communication loss, timing overruns, and invalid states. Do not rely on controller stability alone as the safety argument.

## Debugging
Correlate command, measurement, estimated state, control error, actuator output, timing, and physical waveforms. Timestamp the full loop so a control problem is not misdiagnosed as a purely mathematical problem.

## Common Mistakes
- Designing the controller before understanding the plant.
- Tuning against an invalid or overly narrow model.
- Ignoring actuator saturation and integral windup.
- Treating sample period as an implementation detail.
- Ignoring sensor delay and measurement filtering phase lag.
- Tuning Kalman covariances without checking innovation statistics.
- Validating only nominal operating conditions.

## Staff-Level View
Treat control and estimation as one cyber-physical loop: physics, sensing, modeling, algorithms, computation, timing, actuation, safety, calibration, and validation must close consistently. The objective is not merely a mathematically elegant controller, but predictable product behavior across operating conditions and lifecycle changes.
