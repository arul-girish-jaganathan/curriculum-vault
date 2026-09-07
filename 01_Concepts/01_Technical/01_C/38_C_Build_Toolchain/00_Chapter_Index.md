# Build Systems and Toolchains

## Chapter purpose
A deep-reference chapter in the C language knowledge base. Use it to understand the rule, reason about compiler and ABI effects, and apply it safely in embedded firmware.

## Topics
- [[01_Compiler_selection|Compiler selection]]
- [[02_Cross_compiler|Cross compiler]]
- [[03_Target_triples|Target triples]]
- [[04_Assembler|Assembler]]
- [[05_Linker|Linker]]
- [[06_Linker_scripts|Linker scripts]]
- [[07_Archive_libraries|Archive libraries]]
- [[08_Dependency_graphs|Dependency graphs]]
- [[09_Compiler_flags|Compiler flags]]
- [[10_Warning_policy|Warning policy]]
- [[11_Reproducible_toolchains|Reproducible toolchains]]
- [[12_CI_build_matrices|CI build matrices]]

## Review prompts
- What is guaranteed by ISO C?
- What depends on the implementation, ABI, compiler, libc, or target?
- What failure mode would appear on an embedded system?
- What test or inspection would prove the behavior?
