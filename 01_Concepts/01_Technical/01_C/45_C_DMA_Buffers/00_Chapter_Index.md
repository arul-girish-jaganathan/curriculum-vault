# DMA Buffers and C Memory Interfaces

## Chapter purpose
A deep-reference chapter in the C language knowledge base. Use it to understand the rule, reason about compiler and ABI effects, and apply it safely in embedded firmware.

## Topics
- [[01_DMA_ownership|DMA ownership]]
- [[02_Cache_maintenance|Cache maintenance]]
- [[03_Alignment|Alignment]]
- [[04_Scatter_gather_descriptors|Scatter-gather descriptors]]
- [[05_Ring_buffers|Ring buffers]]
- [[06_Zero_copy_buffers|Zero-copy buffers]]
- [[07_Producer_consumer_ownership|Producer-consumer ownership]]
- [[08_Memory_barriers|Memory barriers]]
- [[09_Volatile_DMA_status|Volatile DMA status]]
- [[10_Descriptor_lifetime|Descriptor lifetime]]
- [[11_IOMMU_facing_pointers|IOMMU-facing pointers]]
- [[12_DMA_debugging|DMA debugging]]

## Review prompts
- What is guaranteed by ISO C?
- What depends on the implementation, ABI, compiler, libc, or target?
- What failure mode would appear on an embedded system?
- What test or inspection would prove the behavior?

## Chapter completion record
- Chapter 45 contains all 12 indexed topic notes.
- The topic notes were audited against the canonical chapter-note structure: definition, language/compiler mechanism, embedded implications, edge cases/failure modes, example pattern, verification/debugging, and Staff-level takeaway.
- Reference baseline: `01_C/13_C_Pointers/05_void_pointers.md`.
