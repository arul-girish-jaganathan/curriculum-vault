# Maintainable Large C Codebases

## Chapter purpose
A deep-reference chapter in the C language knowledge base. Use it to understand the rule, reason about compiler and ABI effects, and apply it safely in embedded firmware.

## Topics
- [[01_Module_boundaries|Module boundaries]]
- [[02_Dependency_inversion_in_C|Dependency inversion in C]]
- [[03_Opaque_state|Opaque state]]
- [[04_Header_layering|Header layering]]
- [[05_Naming_conventions|Naming conventions]]
- [[06_Configuration_ownership|Configuration ownership]]
- [[07_Code_generation_boundaries|Code generation boundaries]]
- [[08_API_stability|API stability]]
- [[09_Refactoring_safely|Refactoring safely]]
- [[10_Technical_debt_control|Technical debt control]]
- [[11_Review_automation|Review automation]]
- [[12_Architecture_documentation|Architecture documentation]]

## Review prompts
- What is guaranteed by ISO C?
- What depends on the implementation, ABI, compiler, libc, or target?
- What failure mode would appear on an embedded system?
- What test or inspection would prove the behavior?
