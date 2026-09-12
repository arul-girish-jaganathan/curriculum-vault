# Bit Manipulation and Masks

## Chapter purpose
A deep-reference chapter in the C language knowledge base. Use it to understand the rule, reason about compiler and ABI effects, and apply it safely in embedded firmware.

## Topics
- [[01_Masks|Masks]]
- [[02_Shifts|Shifts]]
- [[03_Bit_set_clear_toggle|Bit set/clear/toggle]]
- [[04_Extract_and_insert|Extract and insert]]
- [[05_Rotations|Rotations]]
- [[06_Population_count|Population count]]
- [[07_Leading_trailing_zeros|Leading/trailing zeros]]
- [[08_Sign_extension|Sign extension]]
- [[09_Saturating_arithmetic_patterns|Saturating arithmetic patterns]]
- [[10_Register_helpers|Register helpers]]
- [[11_Bitfield_free_protocol_code|Bitfield-free protocol code]]
- [[12_Constant_time_bit_operations|Constant-time bit operations]]

## Review prompts
- What is guaranteed by ISO C?
- What depends on the implementation, ABI, compiler, libc, or target?
- What failure mode would appear on an embedded system?
- What test or inspection would prove the behavior?

## Chapter completion record
- Chapter 43 contains all 12 indexed topic notes.
- The topic notes were audited against the canonical chapter-note structure: definition, language/compiler mechanism, embedded implications, edge cases/failure modes, example pattern, verification/debugging, and Staff-level takeaway.
- Reference baseline: `01_C/13_C_Pointers/05_void_pointers.md`.
