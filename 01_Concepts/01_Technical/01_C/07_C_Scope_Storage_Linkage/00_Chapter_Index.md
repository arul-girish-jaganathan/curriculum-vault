# Scope, Storage Duration and Linkage

## Chapter purpose
A deep-reference chapter in the C language knowledge base. Use it to understand the rule, reason about compiler and ABI effects, and apply it safely in embedded firmware.

## Topics
- [[01_Block_scope|Block scope]]
- [[02_Function_scope|Function scope]]
- [[03_File_scope|File scope]]
- [[04_Function_prototype_scope|Function prototype scope]]
- [[05_Automatic_storage|Automatic storage]]
- [[06_Static_storage|Static storage]]
- [[07_Thread_storage|Thread storage]]
- [[08_External_linkage|External linkage]]
- [[09_Internal_linkage|Internal linkage]]
- [[10_No_linkage|No linkage]]
- [[11_Tentative_definitions|Tentative definitions]]
- [[12_Namespace_collision_control|Namespace collision control]]

## Review prompts
- What is guaranteed by ISO C?
- What depends on the implementation, ABI, compiler, libc, or target?
- What failure mode would appear on an embedded system?
- What test or inspection would prove the behavior?
