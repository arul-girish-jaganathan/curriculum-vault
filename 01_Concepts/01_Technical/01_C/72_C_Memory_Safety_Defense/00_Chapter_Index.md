# Memory Safety Defensive Engineering

## Chapter purpose
A deep-reference chapter in the C language knowledge base. Use it to understand the rule, reason about compiler and ABI effects, and apply it safely in embedded firmware.

## Topics
- [[01_Bounds_metadata|Bounds metadata]]
- [[02_Length_aware_APIs|Length-aware APIs]]
- [[03_Checked_copies|Checked copies]]
- [[04_Integer_overflow_before_size_math|Integer overflow before size math]]
- [[05_Pointer_validation|Pointer validation]]
- [[06_Lifetime_ownership|Lifetime ownership]]
- [[07_Double_free_detection|Double-free detection]]
- [[08_Canaries|Canaries]]
- [[09_Guard_regions|Guard regions]]
- [[10_MPU_assisted_isolation|MPU-assisted isolation]]
- [[11_Fuzzing_memory_APIs|Fuzzing memory APIs]]
- [[12_Production_diagnostics|Production diagnostics]]

## Review prompts
- What is guaranteed by ISO C?
- What depends on the implementation, ABI, compiler, libc, or target?
- What failure mode would appear on an embedded system?
- What test or inspection would prove the behavior?
