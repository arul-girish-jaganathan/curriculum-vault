# C File I/O and Buffering in Depth

## Chapter purpose
A deep-reference chapter in the C language knowledge base. Use it to understand the rule, reason about compiler and ABI effects, and apply it safely in embedded firmware.

## Topics
- [[01_FILE_objects|FILE objects]]
- [[02_Modes_and_flags|Modes and flags]]
- [[03_fread_fwrite|fread/fwrite]]
- [[04_fgets_fputs|fgets/fputs]]
- [[05_fseek_ftell|fseek/ftell]]
- [[06_Binary_portability|Binary portability]]
- [[07_Buffering_modes|Buffering modes]]
- [[08_fflush_semantics|fflush semantics]]
- [[09_Error_and_EOF_handling|Error and EOF handling]]
- [[10_Large_file_interfaces|Large-file interfaces]]
- [[11_Embedded_libc_differences|Embedded libc differences]]
- [[12_When_stdio_is_inappropriate|When stdio is inappropriate]]

## Review prompts
- What is guaranteed by ISO C?
- What depends on the implementation, ABI, compiler, libc, or target?
- What failure mode would appear on an embedded system?
- What test or inspection would prove the behavior?
