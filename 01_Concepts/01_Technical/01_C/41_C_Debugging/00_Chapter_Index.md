# Debugging C Programs

## Chapter purpose
A deep-reference chapter in the C language knowledge base. Use it to understand the rule, reason about compiler and ABI effects, and apply it safely in embedded firmware.

## Topics
- [[01_Source_level_debugging|Source-level debugging]]
- [[02_Breakpoints|Breakpoints]]
- [[03_Watchpoints|Watchpoints]]
- [[04_Call_stacks|Call stacks]]
- [[05_Registers|Registers]]
- [[06_Memory_inspection|Memory inspection]]
- [[07_Optimized_code_debugging|Optimized-code debugging]]
- [[08_Core_dumps|Core dumps]]
- [[09_Post_mortem_analysis|Post-mortem analysis]]
- [[10_Fault_localization|Fault localization]]
- [[11_Debugger_scripting|Debugger scripting]]
- [[12_Debugging_production_firmware|Debugging production firmware]]

## Review prompts
- What is guaranteed by ISO C?
- What depends on the implementation, ABI, compiler, libc, or target?
- What failure mode would appear on an embedded system?
- What test or inspection would prove the behavior?

## Chapter completion record
- Chapter 41 contains all 12 indexed topic notes.
- The topic notes were audited against the canonical chapter-note structure: definition, language/compiler mechanism, embedded implications, edge cases/failure modes, example pattern, verification/debugging, and Staff-level takeaway.
- Reference baseline: `01_C/13_C_Pointers/05_void_pointers.md`.
