# Alignment and Object Representation

## Chapter purpose
A deep-reference chapter in the C language knowledge base. Use it to understand the rule, reason about compiler and ABI effects, and apply it safely in embedded firmware.

## Topics
- [[01_Alignment_requirements|Alignment requirements]]
- [[02_Alignof|_Alignof]]
- [[03_Alignas|_Alignas]]
- [[04_Object_representation|Object representation]]
- [[05_Unsigned_char_inspection|Unsigned char inspection]]
- [[06_Padding_bytes|Padding bytes]]
- [[07_Trap_representations|Trap representations]]
- [[08_Copying_representations|Copying representations]]
- [[09_Serialization_hazards|Serialization hazards]]
- [[10_DMA_alignment|DMA alignment]]
- [[11_Cache_line_alignment|Cache-line alignment]]
- [[12_ABI_and_packing|ABI and packing]]

## Review prompts
- What is guaranteed by ISO C?
- What depends on the implementation, ABI, compiler, libc, or target?
- What failure mode would appear on an embedded system?
- What test or inspection would prove the behavior?
