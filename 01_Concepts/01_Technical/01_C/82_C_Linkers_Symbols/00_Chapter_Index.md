# Linker Symbols and Relocation Concepts

## Chapter purpose
A deep-reference chapter in the C language knowledge base. Use it to understand the rule, reason about compiler and ABI effects, and apply it safely in embedded firmware.

## Topics
- [[01_Symbol_tables|Symbol tables]]
- [[02_Relocations|Relocations]]
- [[03_Absolute_vs_relocatable_symbols|Absolute vs relocatable symbols]]
- [[04_Weak_resolution|Weak resolution]]
- [[05_Common_symbols|Common symbols]]
- [[06_Garbage_collection_of_sections|Garbage collection of sections]]
- [[07_Map_files|Map files]]
- [[08_Memory_regions|Memory regions]]
- [[09_Overlay_concepts|Overlay concepts]]
- [[10_Startup_symbols|Startup symbols]]
- [[11_Duplicate_definitions|Duplicate definitions]]
- [[12_Link_time_diagnostics|Link-time diagnostics]]

## Review prompts
- What is guaranteed by ISO C?
- What depends on the implementation, ABI, compiler, libc, or target?
- What failure mode would appear on an embedded system?
- What test or inspection would prove the behavior?
