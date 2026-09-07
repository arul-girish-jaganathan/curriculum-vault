# C Runtime Startup and Program Entry

## Chapter purpose
A deep-reference chapter in the C language knowledge base. Use it to understand the rule, reason about compiler and ABI effects, and apply it safely in embedded firmware.

## Topics
- [[01_Reset_entry|Reset entry]]
- [[02_Stack_initialization|Stack initialization]]
- [[03_Data_copy|Data copy]]
- [[04_BSS_zeroing|BSS zeroing]]
- [[05_SystemInit_style_hooks|SystemInit-style hooks]]
- [[06_Constructor_boundaries_conceptually|Constructor boundaries conceptually]]
- [[07_argc_argv_hosted_startup|argc/argv hosted startup]]
- [[08_main_contract|main contract]]
- [[09_Exit_handlers|Exit handlers]]
- [[10_Early_hardware_access|Early hardware access]]
- [[11_Faults_before_main|Faults before main]]
- [[12_Startup_verification|Startup verification]]

## Review prompts
- What is guaranteed by ISO C?
- What depends on the implementation, ABI, compiler, libc, or target?
- What failure mode would appear on an embedded system?
- What test or inspection would prove the behavior?
