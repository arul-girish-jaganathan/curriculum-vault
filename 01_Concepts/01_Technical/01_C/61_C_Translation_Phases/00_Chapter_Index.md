# Translation Phases and Source Encoding

## Chapter purpose
A deep-reference chapter in the C language knowledge base. Use it to understand the rule, reason about compiler and ABI effects, and apply it safely in embedded firmware.

## Topics
- [[01_Phase_1_source_mapping|Phase 1 source mapping]]
- [[02_Trigraph_history|Trigraph history]]
- [[03_Line_splicing|Line splicing]]
- [[04_Comment_replacement|Comment replacement]]
- [[05_Preprocessing_tokens|Preprocessing tokens]]
- [[06_String_literal_concatenation|String literal concatenation]]
- [[07_Escape_processing|Escape processing]]
- [[08_Header_name_tokens|Header-name tokens]]
- [[09_Macro_rescanning|Macro rescanning]]
- [[10_Conditional_preprocessing|Conditional preprocessing]]
- [[11_Phase_ordering_hazards|Phase ordering hazards]]
- [[12_Source_encoding_portability|Source encoding portability]]

## Review prompts
- What is guaranteed by ISO C?
- What depends on the implementation, ABI, compiler, libc, or target?
- What failure mode would appear on an embedded system?
- What test or inspection would prove the behavior?
