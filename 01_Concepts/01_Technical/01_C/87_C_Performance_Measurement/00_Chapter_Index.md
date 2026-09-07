# Measurement and Profiling for C

## Chapter purpose
A deep-reference chapter in the C language knowledge base. Use it to understand the rule, reason about compiler and ABI effects, and apply it safely in embedded firmware.

## Topics
- [[01_Cycle_counters|Cycle counters]]
- [[02_Timestamp_sources|Timestamp sources]]
- [[03_Sampling_profilers|Sampling profilers]]
- [[04_Instrumentation|Instrumentation]]
- [[05_Trace_buffers|Trace buffers]]
- [[06_Cache_counters|Cache counters]]
- [[07_Branch_counters|Branch counters]]
- [[08_Memory_bandwidth_metrics|Memory bandwidth metrics]]
- [[09_Allocation_telemetry|Allocation telemetry]]
- [[10_Latency_histograms|Latency histograms]]
- [[11_Benchmark_design|Benchmark design]]
- [[12_Measurement_bias|Measurement bias]]

## Review prompts
- What is guaranteed by ISO C?
- What depends on the implementation, ABI, compiler, libc, or target?
- What failure mode would appear on an embedded system?
- What test or inspection would prove the behavior?
