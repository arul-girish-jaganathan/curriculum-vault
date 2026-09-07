# Diagnostics and Static Analysis

## Chapter purpose
A deep-reference chapter in the C language knowledge base. Use it to understand the rule, reason about compiler and ABI effects, and apply it safely in embedded firmware.

## Topics
- [[01_Warnings|Warnings]]
- [[02_Warning_levels|Warning levels]]
- [[03_Treat_warnings_as_errors|Treat warnings as errors]]
- [[04_Static_analyzers|Static analyzers]]
- [[05_Dataflow_analysis|Dataflow analysis]]
- [[06_Defect_pattern_detection|Defect pattern detection]]
- [[07_MISRA_C_checking|MISRA-C checking]]
- [[08_CERT_C_checking|CERT C checking]]
- [[09_False_positives|False positives]]
- [[10_Suppression_discipline|Suppression discipline]]
- [[11_Baseline_management|Baseline management]]
- [[12_CI_quality_gates|CI quality gates]]

## Review prompts
- What is guaranteed by ISO C?
- What depends on the implementation, ABI, compiler, libc, or target?
- What failure mode would appear on an embedded system?
- What test or inspection would prove the behavior?
