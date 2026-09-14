# Debugging C Programs

## Chapter purpose

A deep-reference chapter in the C language knowledge base. Each topic is written to separate ISO C guarantees from compiler/ABI behavior and embedded hardware behavior.

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

## Reference baseline

`01_C/13_C_Pointers/05_void_pointers.md`

## Review prompts

- What is guaranteed by ISO C?
- What depends on the implementation, ABI, compiler, libc, or target?
- What failure mode would appear on an embedded system?
- What evidence would prove the behavior?
