# Deterministic C for Real-Time Systems

## Chapter purpose
A deep-reference chapter in the C language knowledge base. Use it to understand the rule, reason about compiler and ABI effects, and apply it safely in embedded firmware.

## Topics
- [[01_WCET_considerations|WCET considerations]]
- [[02_Bounded_loops|Bounded loops]]
- [[03_Bounded_allocation|Bounded allocation]]
- [[04_Deterministic_synchronization|Deterministic synchronization]]
- [[05_Jitter_sources|Jitter sources]]
- [[06_Cache_effects|Cache effects]]
- [[07_Compiler_variability|Compiler variability]]
- [[08_Floating_determinism|Floating determinism]]
- [[09_Logging_impact|Logging impact]]
- [[10_Failure_path_determinism|Failure-path determinism]]
- [[11_Timing_instrumentation|Timing instrumentation]]
- [[12_Real_time_coding_policy|Real-time coding policy]]

## Review prompts
- What is guaranteed by ISO C?
- What depends on the implementation, ABI, compiler, libc, or target?
- What failure mode would appear on an embedded system?
- What test or inspection would prove the behavior?
