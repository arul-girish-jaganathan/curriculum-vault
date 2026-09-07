# Derivative Noise

## Purpose
Develop a practical, engineering-grade understanding of **Derivative Noise** for digital signal processing in embedded and real-time systems.

## Core Model
- **Signal:** define the physical/derived quantity, sampling rate, units, dynamic range, and expected signal statistics.
- **Algorithm:** identify the mathematical operation and assumptions.
- **Data path:** describe sample movement, buffering, transforms, filtering, and output timing.
- **Numerical model:** distinguish floating-point, fixed-point, quantized, saturated, and implementation-specific behavior.
- **System constraint:** identify latency, throughput, memory, power, accuracy, and determinism requirements.

## Key Questions
1. What signal bandwidth and sampling rate are required?
2. Which operation dominates computation or memory traffic?
3. What aliasing, quantization, leakage, numerical, or stability risks exist?
4. What latency/jitter and buffer constraints apply?
5. What reference model or measurement proves the implementation is correct?

## Signal and Data Path
Trace:
- sensor/ADC or upstream input;
- sample buffering;
- preprocessing;
- DSP kernel;
- intermediate state;
- output filtering/reconstruction;
- DAC/actuator or downstream consumer.

Make ownership, buffer lifetime, sample ordering, and timing explicit.

## Numerical and Stability Issues
Consider finite word length, coefficient quantization, roundoff, overflow, saturation, scaling, dynamic range, floating-point special values, filter pole sensitivity, accumulated error, and block-to-block state continuity.

## Failure Modes
Common DSP failures include:
- aliasing;
- wrong sampling rate assumptions;
- spectral leakage misinterpretation;
- incorrect frequency/bin scaling;
- filter instability;
- coefficient/state overflow;
- buffer overrun or underrun;
- timing deadline misses;
- excessive latency;
- numerical drift;
- calibration errors;
- unexpected signal noise or interference.

## Testing and Validation
Use:
- analytical reference results;
- impulse and step responses;
- swept-frequency tests;
- known-tone tests;
- random/noise inputs;
- corner amplitudes and frequencies;
- fixed-vs-floating reference comparison;
- golden vectors;
- hardware measurements.

Measure appropriate error metrics such as magnitude/phase error, SNR, THD, RMSE, detection rate, or frequency-response deviation.

## Performance
Evaluate cycles/sample, block latency, throughput, memory bandwidth, cache behavior, MAC count, SIMD utilization, DMA efficiency, and power per sample. Measure both average and worst-case behavior when real-time constraints apply.

## Embedded Consequences
Consider ADC/DAC timing, timer triggers, DMA, ping-pong/ring buffers, cache coherency, alignment, RTOS scheduling, interrupt load, SIMD/vector instructions, scratchpad/TCM memory, accelerator offload, and power/thermal states.

## Application Context
DSP choices depend strongly on the application: audio, vibration, sensing, control, communications, imaging, or measurement may prioritize different combinations of latency, phase accuracy, noise rejection, memory, and computational cost.

## Common Mistakes
- Choosing a filter before defining the signal bandwidth and sampling constraints.
- Treating FFT bins as exact signal frequencies without considering record length/windowing.
- Ignoring scaling and overflow in fixed-point implementations.
- Using a mathematically correct algorithm that misses the real-time deadline.
- Measuring only average performance.
- Comparing hardware and floating-point reference results without accounting for quantization/tolerance.
- Assuming more taps or higher FFT size always improves the product.

## Staff-Level View
Treat DSP as a system pipeline rather than an isolated formula: sampling, analog interface, numerical representation, algorithm, data movement, scheduling, hardware acceleration, validation, power, and field robustness must fit together. Optimize the complete signal chain against explicit product requirements.
