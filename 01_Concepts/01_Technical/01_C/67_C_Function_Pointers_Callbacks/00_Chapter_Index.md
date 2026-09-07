# Function Pointers and Callback Design

## Chapter purpose
A deep-reference chapter in the C language knowledge base. Use it to understand the rule, reason about compiler and ABI effects, and apply it safely in embedded firmware.

## Topics
- [[01_Function_pointer_syntax|Function pointer syntax]]
- [[02_Typedef_callbacks|Typedef callbacks]]
- [[03_Callback_context|Callback context]]
- [[04_Registration_tables|Registration tables]]
- [[05_Event_callbacks|Event callbacks]]
- [[06_ISR_callbacks|ISR callbacks]]
- [[07_Stateful_callbacks|Stateful callbacks]]
- [[08_Function_pointer_arrays|Function pointer arrays]]
- [[09_Dispatch_tables|Dispatch tables]]
- [[10_ABI_calling_convention|ABI calling convention]]
- [[11_Lifetime_safety|Lifetime safety]]
- [[12_Callback_reentrancy|Callback reentrancy]]

## Review prompts
- What is guaranteed by ISO C?
- What depends on the implementation, ABI, compiler, libc, or target?
- What failure mode would appear on an embedded system?
- What test or inspection would prove the behavior?
