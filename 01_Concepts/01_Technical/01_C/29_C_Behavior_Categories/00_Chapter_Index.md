# Defined, Implementation-defined, Unspecified and Undefined Behavior

## Chapter purpose
A deep-reference chapter in the C language knowledge base. Use it to understand the rule, reason about compiler and ABI effects, and apply it safely in embedded firmware.

## Topics
- [[01_Defined_behavior|Defined behavior]]
- [[02_Implementation_defined_behavior|Implementation-defined behavior]]
- [[03_Unspecified_behavior|Unspecified behavior]]
- [[04_Undefined_behavior|Undefined behavior]]
- [[05_Constraint_violations|Constraint violations]]
- [[06_Annex_J_style_thinking|Annex J style thinking]]
- [[07_Optimizer_exploitation|Optimizer exploitation]]
- [[08_Compiler_diagnostics|Compiler diagnostics]]
- [[09_Portable_defensive_coding|Portable defensive coding]]
- [[10_Embedded_UB_examples|Embedded UB examples]]
- [[11_Static_analysis_review|Static-analysis review]]
- [[12_Behavior_classification_workflow|Behavior classification workflow]]

## Review prompts
- What is guaranteed by ISO C?
- What depends on the implementation, ABI, compiler, libc, or target?
- What failure mode would appear on an embedded system?
- What test or inspection would prove the behavior?
