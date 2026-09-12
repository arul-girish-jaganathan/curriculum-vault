# 27_C_Alignment_Object_Representation: Chapter Index

## Overview
C Alignment and Object Representation governs how data types are aligned in memory hardware, how objects are structured bit-for-bit in bytes, and how compilers manage padding, alignment constraints, trap representations, and data serialization. This chapter provides a rigorous examination of memory alignment mechanics, C11 `_Alignof` and `_Alignas` (`<stdalign.h>`), object representations, padding bytes, hardware-level alignment requirements (DMA and cache lines), and ABI packing rules.

## Chapter Directory
- [[01_Alignment_requirements]] — Hardware alignment constraints, fundamental alignment, and strict alignment architectures
- [[02_Alignof]] — Querying alignment via `_Alignof` / `alignof` operator
- [[03_Alignas]] — Forcing alignment constraints via `_Alignas` / `alignas` specifier
- [[04_Object_representation]] — Scalar and aggregate bit layouts, value representations, and padding
- [[05_Unsigned_char_inspection]] — Examining raw object bytes safely via `unsigned char *` and `memcpy`
- [[06_Padding_bytes]] — Structural holes, alignment padding, and uninitialized diagnostic hazards
- [[07_Trap_representations]] — Invalid bit patterns, floating-point signaling NaNs, and integer trap values
- [[08_Copying_representations]] — Safe object copying via `memcpy` vs. unsafe union/pointer type-punning
- [[09_Serialization_hazards]] — Endianness, padding serialization bugs, and network protocol alignment
- [[10_DMA_alignment]] — Peripheral direct memory access (DMA) alignment and cache coherence requirements
- [[11_Cache_line_alignment]] — False sharing prevention, cache-line padding, and performance tuning
- [[12_ABI_and_packing]] — Packed structures (`#pragma pack`), ABI compatibility, and unaligned access penalties

## Related Chapters
- [[../00_Complete_Topic_Map]]
- [[../25_C_Dynamic_Memory]]
- [[../26_C_Lifetime_Aliasing]]
