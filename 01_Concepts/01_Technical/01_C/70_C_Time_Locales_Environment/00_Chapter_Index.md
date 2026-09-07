# Time, Locale and Environment Interfaces

## Chapter purpose
A deep-reference chapter in the C language knowledge base. Use it to understand the rule, reason about compiler and ABI effects, and apply it safely in embedded firmware.

## Topics
- [[01_time_t|time_t]]
- [[02_clock_t|clock_t]]
- [[03_timespec_concepts|timespec concepts]]
- [[04_Calendar_conversion|Calendar conversion]]
- [[05_strftime|strftime]]
- [[06_Locale_state|Locale state]]
- [[07_Character_classification|Character classification]]
- [[08_Environment_variables|Environment variables]]
- [[09_getenv|getenv]]
- [[10_Hosted_process_assumptions|Hosted process assumptions]]
- [[11_Determinism_concerns|Determinism concerns]]
- [[12_Embedded_alternatives|Embedded alternatives]]

## Review prompts
- What is guaranteed by ISO C?
- What depends on the implementation, ABI, compiler, libc, or target?
- What failure mode would appear on an embedded system?
- What test or inspection would prove the behavior?
