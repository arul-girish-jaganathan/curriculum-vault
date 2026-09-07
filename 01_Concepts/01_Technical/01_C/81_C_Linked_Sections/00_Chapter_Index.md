# Sections, Placement and Embedded Image Layout

## Chapter purpose
A deep-reference chapter in the C language knowledge base. Use it to understand the rule, reason about compiler and ABI effects, and apply it safely in embedded firmware.

## Topics
- [[01_text_data_bss|text/data/bss]]
- [[02_rodata|rodata]]
- [[03_custom_sections|custom sections]]
- [[04_section_attributes|section attributes]]
- [[05_linker_symbols|linker symbols]]
- [[06_copy_down_tables|copy-down tables]]
- [[07_noinit_regions|noinit regions]]
- [[08_retention_RAM|retention RAM]]
- [[09_bootloader_application_boundaries|bootloader/application boundaries]]
- [[10_CRC_checksum_regions|CRC/checksum regions]]
- [[11_vector_table_placement|vector table placement]]
- [[12_Section_map_debugging|Section map debugging]]

## Review prompts
- What is guaranteed by ISO C?
- What depends on the implementation, ABI, compiler, libc, or target?
- What failure mode would appear on an embedded system?
- What test or inspection would prove the behavior?
