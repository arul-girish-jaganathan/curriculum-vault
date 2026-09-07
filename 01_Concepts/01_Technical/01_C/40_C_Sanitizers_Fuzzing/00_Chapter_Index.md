# Sanitizers and Fuzzing

## Chapter purpose
A deep-reference chapter in the C language knowledge base. Use it to understand the rule, reason about compiler and ABI effects, and apply it safely in embedded firmware.

## Topics
- [[01_AddressSanitizer|AddressSanitizer]]
- [[02_UndefinedBehaviorSanitizer|UndefinedBehaviorSanitizer]]
- [[03_ThreadSanitizer|ThreadSanitizer]]
- [[04_LeakSanitizer|LeakSanitizer]]
- [[05_Integer_sanitization|Integer sanitization]]
- [[06_Coverage_guided_fuzzing|Coverage-guided fuzzing]]
- [[07_Harness_design|Harness design]]
- [[08_Corpus_management|Corpus management]]
- [[09_Minimization|Minimization]]
- [[10_Embedded_target_limitations|Embedded-target limitations]]
- [[11_Host_target_differential_testing|Host-target differential testing]]
- [[12_Sanitizer_triage|Sanitizer triage]]

## Review prompts
- What is guaranteed by ISO C?
- What depends on the implementation, ABI, compiler, libc, or target?
- What failure mode would appear on an embedded system?
- What test or inspection would prove the behavior?
