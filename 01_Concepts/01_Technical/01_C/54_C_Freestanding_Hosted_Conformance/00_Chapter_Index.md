# Freestanding, Hosted and Conformance Profiles

## Chapter purpose
A deep-reference chapter in the C language knowledge base. Use it to understand the rule, reason about compiler and ABI effects, and apply it safely in embedded firmware.

## Topics
- [[01_Hosted_implementation|Hosted implementation]]
- [[02_Freestanding_implementation|Freestanding implementation]]
- [[03_Required_headers|Required headers]]
- [[04_Startup_responsibilities|Startup responsibilities]]
- [[05_Environment_assumptions|Environment assumptions]]
- [[06_Library_subsets|Library subsets]]
- [[07_Embedded_libc_variants|Embedded libc variants]]
- [[08_Conformance_claims|Conformance claims]]
- [[09_Extension_inventories|Extension inventories]]
- [[10_Qualification_testing|Qualification testing]]
- [[11_Cross_toolchain_differences|Cross toolchain differences]]
- [[12_Portable_freestanding_design|Portable freestanding design]]

## Review prompts
- What is guaranteed by ISO C?
- What depends on the implementation, ABI, compiler, libc, or target?
- What failure mode would appear on an embedded system?
- What test or inspection would prove the behavior?
