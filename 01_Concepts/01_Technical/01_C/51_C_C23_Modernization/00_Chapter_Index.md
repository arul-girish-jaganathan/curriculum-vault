# Modern C23 Features

## Chapter purpose
A deep-reference chapter in the C language knowledge base. Use it to understand the rule, reason about compiler and ABI effects, and apply it safely in embedded firmware.

## Topics
- [[01_nullptr_constant|nullptr constant]]
- [[02_typeof_and_typeof_unqual|typeof and typeof_unqual]]
- [[03_constexpr_objects_functions|constexpr objects/functions]]
- [[04_BitInt_overview|_BitInt overview]]
- [[05_stdbit_facilities|stdbit facilities]]
- [[06_checked_integer_arithmetic|checked integer arithmetic]]
- [[07_reproducible_style_concepts|reproducible attribute concepts]]
- [[08_Attributes|Attributes]]
- [[09_Empty_initializers|Empty initializers]]
- [[10_New_header_library_additions|New header/library additions]]
- [[11_C23_portability_strategy|C23 portability strategy]]
- [[12_Migration_from_C17|Migration from C17]]

## Review prompts
- What is guaranteed by ISO C?
- What depends on the implementation, ABI, compiler, libc, or target?
- What failure mode would appear on an embedded system?
- What test or inspection would prove the behavior?
