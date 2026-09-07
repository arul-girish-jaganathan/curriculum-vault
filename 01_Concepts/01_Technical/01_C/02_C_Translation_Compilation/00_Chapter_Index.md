# Translation Units, Compilation and Linking

## Chapter purpose
A deep-reference chapter in the C language knowledge base. Use it to understand the rule, reason about compiler and ABI effects, and apply it safely in embedded firmware.

## Topics
- [[01_Source_to_translation_unit|Source to translation unit]]
- [[02_Preprocessing_phase|Preprocessing phase]]
- [[03_Tokenization|Tokenization]]
- [[04_Parsing_and_semantic_analysis|Parsing and semantic analysis]]
- [[05_Constant_expressions|Constant expressions]]
- [[06_Object_code_generation|Object code generation]]
- [[07_Assembly_inspection|Assembly inspection]]
- [[08_Compiler_driver_stages|Compiler driver stages]]
- [[09_Linking_overview|Linking overview]]
- [[10_Static_vs_dynamic_libraries|Static vs dynamic libraries]]
- [[11_LTO_and_whole_program_optimization|LTO and whole-program optimization]]
- [[12_Reproducible_builds|Reproducible builds]]

## Review prompts
- What is guaranteed by ISO C?
- What depends on the implementation, ABI, compiler, libc, or target?
- What failure mode would appear on an embedded system?
- What test or inspection would prove the behavior?
