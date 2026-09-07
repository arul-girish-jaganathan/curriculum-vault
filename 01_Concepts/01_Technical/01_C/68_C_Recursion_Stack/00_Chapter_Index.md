# Recursion and Stack Behavior

## Chapter purpose
A deep-reference chapter in the C language knowledge base. Use it to understand the rule, reason about compiler and ABI effects, and apply it safely in embedded firmware.

## Topics
- [[01_Recursive_calls|Recursive calls]]
- [[02_Stack_frame_basics|Stack frame basics]]
- [[03_Tail_call_optimization|Tail-call optimization]]
- [[04_Recursion_depth|Recursion depth]]
- [[05_Mutual_recursion|Mutual recursion]]
- [[06_Re_entrancy|Re-entrancy]]
- [[07_ISR_interaction|ISR interaction]]
- [[08_RTOS_task_stacks|RTOS task stacks]]
- [[09_Static_analysis|Static analysis]]
- [[10_Converting_recursion_to_iteration|Converting recursion to iteration]]
- [[11_Stack_watermarking|Stack watermarking]]
- [[12_Embedded_policy|Embedded policy]]

## Review prompts
- What is guaranteed by ISO C?
- What depends on the implementation, ABI, compiler, libc, or target?
- What failure mode would appear on an embedded system?
- What test or inspection would prove the behavior?
