# Signals, setjmp and Non-local Control Flow

## Chapter purpose
A deep-reference chapter in the C language knowledge base. Use it to understand the rule, reason about compiler and ABI effects, and apply it safely in embedded firmware.

## Topics
- [[01_signal_model|signal model]]
- [[02_Signal_handlers|Signal handlers]]
- [[03_Async_signal_safety|Async-signal-safety]]
- [[04_Volatile_sig_atomic_t|Volatile sig_atomic_t]]
- [[05_raise_abort|raise/abort]]
- [[06_setjmp|setjmp]]
- [[07_longjmp|longjmp]]
- [[08_sigsetjmp_style_concepts|sigsetjmp-style concepts]]
- [[09_ISR_vs_signal_distinctions|ISR vs signal distinctions]]
- [[10_Recovery_boundaries|Recovery boundaries]]
- [[11_Control_flow_hazards|Control-flow hazards]]
- [[12_Embedded_alternatives|Embedded alternatives]]

## Review prompts
- What is guaranteed by ISO C?
- What depends on the implementation, ABI, compiler, libc, or target?
- What failure mode would appear on an embedded system?
- What test or inspection would prove the behavior?
