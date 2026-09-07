# Interrupt-facing C and ISRs

## Chapter purpose
A deep-reference chapter in the C language knowledge base. Use it to understand the rule, reason about compiler and ABI effects, and apply it safely in embedded firmware.

## Topics
- [[01_ISR_constraints|ISR constraints]]
- [[02_Volatile_MMIO|Volatile MMIO]]
- [[03_Atomic_flags|Atomic flags]]
- [[04_Minimal_ISR_work|Minimal ISR work]]
- [[05_Deferred_processing|Deferred processing]]
- [[06_Interrupt_safe_APIs|Interrupt-safe APIs]]
- [[07_Reentrancy|Reentrancy]]
- [[08_Nested_interrupts|Nested interrupts]]
- [[09_Critical_sections|Critical sections]]
- [[10_ISR_stack_usage|ISR stack usage]]
- [[11_Latency_budgeting|Latency budgeting]]
- [[12_ISR_review_checklist|ISR review checklist]]

## Review prompts
- What is guaranteed by ISO C?
- What depends on the implementation, ABI, compiler, libc, or target?
- What failure mode would appear on an embedded system?
- What test or inspection would prove the behavior?
