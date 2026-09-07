# const, volatile, restrict and _Atomic

## Chapter purpose
A deep-reference chapter in the C language knowledge base. Use it to understand the rule, reason about compiler and ABI effects, and apply it safely in embedded firmware.

## Topics
- [[01_const_semantics|const semantics]]
- [[02_volatile_semantics|volatile semantics]]
- [[03_restrict_semantics|restrict semantics]]
- [[04_Atomic_qualifier|_Atomic qualifier]]
- [[05_Qualified_pointer_targets|Qualified pointer targets]]
- [[06_Qualified_pointers|Qualified pointers]]
- [[07_MMIO_qualification|MMIO qualification]]
- [[08_DMA_buffer_qualification|DMA buffer qualification]]
- [[09_Aliasing_promises|Aliasing promises]]
- [[10_Optimizer_interaction|Optimizer interaction]]
- [[11_Qualification_conversions|Qualification conversions]]
- [[12_Review_checklist|Review checklist]]

## Review prompts
- What is guaranteed by ISO C?
- What depends on the implementation, ABI, compiler, libc, or target?
- What failure mode would appear on an embedded system?
- What test or inspection would prove the behavior?
