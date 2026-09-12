# Error Handling and Failure Contracts

## Chapter purpose
A deep-reference chapter in the C language knowledge base. Use it to understand the rule, reason about compiler and ABI effects, and apply it safely in embedded firmware.

## Topics
- [[01_Return_code_conventions|Return-code conventions]]
- [[02_errno_semantics|errno semantics]]
- [[03_Sentinel_values|Sentinel values]]
- [[04_Optional_outputs|Optional outputs]]
- [[05_Out_parameters|Out-parameters]]
- [[06_Error_propagation|Error propagation]]
- [[07_Cleanup_on_failure|Cleanup on failure]]
- [[08_Resource_rollback|Resource rollback]]
- [[09_Assertions_vs_runtime_errors|Assertions vs runtime errors]]
- [[10_Fault_containment|Fault containment]]
- [[11_Embedded_degraded_modes|Embedded degraded modes]]
- [[12_API_failure_contracts|API failure contracts]]

## Review prompts
- What is guaranteed by ISO C?
- What depends on the implementation, ABI, compiler, libc, or target?
- What failure mode would appear on an embedded system?
- What test or inspection would prove the behavior?

## Chapter completion record
- Chapter 42 contains all 12 indexed topic notes.
- The topic notes were audited against the canonical chapter-note structure: definition, language/compiler mechanism, embedded implications, edge cases/failure modes, example pattern, verification/debugging, and Staff-level takeaway.
- Reference baseline: `01_C/13_C_Pointers/05_void_pointers.md`.
