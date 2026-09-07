# Fault Containment in C

## Chapter purpose
A deep-reference chapter in the C language knowledge base. Use it to understand the rule, reason about compiler and ABI effects, and apply it safely in embedded firmware.

## Topics
- [[01_Detecting_corruption|Detecting corruption]]
- [[02_Fail_fast_vs_fail_operational|Fail-fast vs fail-operational]]
- [[03_Error_domains|Error domains]]
- [[04_Containment_boundaries|Containment boundaries]]
- [[05_Watchdog_coordination|Watchdog coordination]]
- [[06_Safe_state_transitions|Safe-state transitions]]
- [[07_Redundant_checks|Redundant checks]]
- [[08_Sanity_guards|Sanity guards]]
- [[09_State_validation|State validation]]
- [[10_Recovery_handlers|Recovery handlers]]
- [[11_Persistent_fault_records|Persistent fault records]]
- [[12_Evidence_driven_recovery|Evidence-driven recovery]]

## Review prompts
- What is guaranteed by ISO C?
- What depends on the implementation, ABI, compiler, libc, or target?
- What failure mode would appear on an embedded system?
- What test or inspection would prove the behavior?
