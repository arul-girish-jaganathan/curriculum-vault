# Staff-Level C Architecture and Technical Decisions

## Chapter purpose
A deep-reference chapter in the C language knowledge base. Use it to understand the rule, reason about compiler and ABI effects, and apply it safely in embedded firmware.

## Topics
- [[01_Requirement_decomposition|Requirement decomposition]]
- [[02_Hazard_analysis|Hazard analysis]]
- [[03_Trade_off_matrices|Trade-off matrices]]
- [[04_API_lifecycle|API lifecycle]]
- [[05_Concurrency_architecture|Concurrency architecture]]
- [[06_Memory_strategy|Memory strategy]]
- [[07_Performance_budgets|Performance budgets]]
- [[08_Portability_strategy|Portability strategy]]
- [[09_Tool_qualification|Tool qualification]]
- [[10_Verification_strategy|Verification strategy]]
- [[11_Risk_based_review|Risk-based review]]
- [[12_Decision_records|Decision records]]

## Review prompts
- What is guaranteed by ISO C?
- What depends on the implementation, ABI, compiler, libc, or target?
- What failure mode would appear on an embedded system?
- What test or inspection would prove the behavior?
