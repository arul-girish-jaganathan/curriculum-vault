# Embedded C Test Harness Architecture

## Chapter purpose
A deep-reference chapter in the C language knowledge base. Use it to understand the rule, reason about compiler and ABI effects, and apply it safely in embedded firmware.

## Topics
- [[01_Host_harness|Host harness]]
- [[02_Target_harness|Target harness]]
- [[03_Dependency_seams|Dependency seams]]
- [[04_Hardware_abstraction_seams|Hardware abstraction seams]]
- [[05_Synthetic_inputs|Synthetic inputs]]
- [[06_Golden_vectors|Golden vectors]]
- [[07_Fault_injection|Fault injection]]
- [[08_Timing_tests|Timing tests]]
- [[09_Power_cycle_tests|Power-cycle tests]]
- [[10_Reset_persistence_tests|Reset persistence tests]]
- [[11_Coverage_collection|Coverage collection]]
- [[12_Continuous_regression|Continuous regression]]

## Review prompts
- What is guaranteed by ISO C?
- What depends on the implementation, ABI, compiler, libc, or target?
- What failure mode would appear on an embedded system?
- What test or inspection would prove the behavior?
