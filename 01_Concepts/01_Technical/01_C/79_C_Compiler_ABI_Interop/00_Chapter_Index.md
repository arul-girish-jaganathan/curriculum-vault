# C Interoperability and ABI Boundaries

## Chapter purpose
A deep-reference chapter in the C language knowledge base. Use it to understand the rule, reason about compiler and ABI effects, and apply it safely in embedded firmware.

## Topics
- [[01_extern_C_relevance_conceptually|extern C relevance conceptually]]
- [[02_Calling_C_from_assembly|Calling C from assembly]]
- [[03_Calling_C_from_C|Calling C from C++]]
- [[04_Struct_ABI|Struct ABI]]
- [[05_Enum_ABI|Enum ABI]]
- [[06_Packing_boundaries|Packing boundaries]]
- [[07_Symbol_naming|Symbol naming]]
- [[08_Visibility|Visibility]]
- [[09_FFI_handles|FFI handles]]
- [[10_Versioned_interfaces|Versioned interfaces]]
- [[11_Shared_library_boundaries|Shared-library boundaries]]
- [[12_Cross_compiler_ABI_validation|Cross-compiler ABI validation]]

## Review prompts
- What is guaranteed by ISO C?
- What depends on the implementation, ABI, compiler, libc, or target?
- What failure mode would appear on an embedded system?
- What test or inspection would prove the behavior?
