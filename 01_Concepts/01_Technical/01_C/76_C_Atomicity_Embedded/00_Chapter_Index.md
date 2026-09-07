# Atomicity at the Hardware Boundary

## Chapter purpose
A deep-reference chapter in the C language knowledge base. Use it to understand the rule, reason about compiler and ABI effects, and apply it safely in embedded firmware.

## Topics
- [[01_Naturally_atomic_widths|Naturally atomic widths]]
- [[02_Bus_transaction_size|Bus transaction size]]
- [[03_Read_modify_write_races|Read-modify-write races]]
- [[04_Interrupt_atomicity|Interrupt atomicity]]
- [[05_Peripheral_register_semantics|Peripheral register semantics]]
- [[06_Bit_banding_history|Bit-banding history]]
- [[07_Critical_section_fallback|Critical-section fallback]]
- [[08_LL_SC_vs_CAS_concepts|LL/SC vs CAS concepts]]
- [[09_Atomic_MMIO_caveats|Atomic MMIO caveats]]
- [[10_DMA_races|DMA races]]
- [[11_Multicore_device_access|Multicore device access]]
- [[12_Atomicity_checklist|Atomicity checklist]]

## Review prompts
- What is guaranteed by ISO C?
- What depends on the implementation, ABI, compiler, libc, or target?
- What failure mode would appear on an embedded system?
- What test or inspection would prove the behavior?
