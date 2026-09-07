# Small Angle Approximation

## Purpose
Build a practical engineering understanding of **Small Angle Approximation** and connect the mathematics to real embedded and systems decisions.

## Core Model
- **Quantity:** identify what is being measured, calculated, or estimated and its units.
- **Relationships:** define the equations, assumptions, dependencies, and limiting cases.
- **Scale:** understand order of magnitude, bounds, sensitivity, and whether a result is physically plausible.
- **Numerical behavior:** distinguish exact mathematics from finite precision, approximation, measurement noise, and implementation limits.
- **Engineering use:** connect the model to software, hardware, signals, control, performance, reliability, or system design.

## Key Questions
1. What physical or engineering quantity does this mathematics describe?
2. What assumptions make the model valid?
3. What changes most when inputs or parameters move?
4. What are the dominant sources of error or uncertainty?
5. How can the result be sanity-checked independently?

## Derivation and Reasoning
Prefer derivations from first principles where useful. Track units through equations and state assumptions explicitly. Use limiting cases, symmetry, conservation, monotonicity, or simple reference examples to validate the result.

## Numerical Considerations
Consider:
- finite precision;
- rounding and truncation;
- overflow and underflow;
- cancellation;
- conditioning and sensitivity;
- discretization;
- convergence;
- measurement uncertainty.

A mathematically correct formula can still produce a poor engineering result when implemented with unsuitable numerical methods.

## Engineering Applications
Typical applications include:
- embedded timing and resource budgets;
- sensor and actuator models;
- DSP and signal processing;
- control loops;
- thermal and power calculations;
- reliability and risk;
- performance and queueing;
- memory/storage sizing;
- communication and networking;
- system optimization.

## Validation
Use at least one independent check:
- dimensional analysis;
- order-of-magnitude estimate;
- limiting-case calculation;
- alternate formulation;
- numerical simulation;
- measurement against real hardware;
- reference implementation.

## Common Mistakes
- Dropping units during calculation.
- Treating a model assumption as a universal law.
- Using excessive precision without meaningful data precision.
- Ignoring correlation in uncertainty analysis.
- Confusing numerical stability with mathematical correctness.
- Extrapolating outside the validated range.
- Trusting a computed value that violates physical constraints.

## Embedded Consequences
Embedded implementations add quantization, fixed-width arithmetic, finite sampling, timing deadlines, sensor noise, actuator limits, memory constraints, and power/thermal constraints. These should be considered part of the mathematical model rather than afterthoughts.

## Tooling
Useful validation tools include calculator/symbolic algebra tools, Python/NumPy/SciPy, MATLAB/Octave, spreadsheets for simple sensitivity work, simulation/modeling tools, and on-target measurement.

## Staff-Level View
Use mathematics to make engineering tradeoffs explicit. The objective is not mathematical elegance alone, but a model that is simple enough to reason about, accurate enough for the decision, numerically safe enough to implement, and validated enough to trust.
