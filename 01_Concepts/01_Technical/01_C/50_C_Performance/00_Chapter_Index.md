# Performance Engineering in C

## Chapter purpose
A deep-reference chapter in the C language knowledge base. Use it to understand the rule, reason about compiler and ABI effects, and apply it safely in embedded firmware.

## Topics
- [[01_Hot_paths|Hot paths]]
- [[02_Cost_models|Cost models]]
- [[03_Instruction_count|Instruction count]]
- [[04_Branch_behavior|Branch behavior]]
- [[05_Cache_locality|Cache locality]]
- [[06_Memory_bandwidth|Memory bandwidth]]
- [[07_Allocation_cost|Allocation cost]]
- [[08_Inlining_tradeoffs|Inlining tradeoffs]]
- [[09_Data_layout|Data layout]]
- [[10_Vectorization|Vectorization]]
- [[11_Profiling_methodology|Profiling methodology]]
- [[12_Performance_regression_control|Performance regression control]]

## Review prompts
- What is guaranteed by ISO C?
- What depends on the implementation, ABI, compiler, libc, or target?
- What failure mode would appear on an embedded system?
- What test or inspection would prove the behavior?
