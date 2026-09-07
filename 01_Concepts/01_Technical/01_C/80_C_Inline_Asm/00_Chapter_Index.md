# Inline Assembly and Compiler Contracts

## Chapter purpose
A deep-reference chapter in the C language knowledge base. Use it to understand the rule, reason about compiler and ABI effects, and apply it safely in embedded firmware.

## Topics
- [[01_asm_syntax_concepts|asm syntax concepts]]
- [[02_Input_constraints|Input constraints]]
- [[03_Output_constraints|Output constraints]]
- [[04_Clobbers|Clobbers]]
- [[05_Volatile_asm|Volatile asm]]
- [[06_Memory_clobber|Memory clobber]]
- [[07_Register_allocation|Register allocation]]
- [[08_Barrier_semantics|Barrier semantics]]
- [[09_Instruction_selection|Instruction selection]]
- [[10_Portability_isolation|Portability isolation]]
- [[11_Disassembly_validation|Disassembly validation]]
- [[12_Inline_asm_review|Inline-asm review]]

## Review prompts
- What is guaranteed by ISO C?
- What depends on the implementation, ABI, compiler, libc, or target?
- What failure mode would appear on an embedded system?
- What test or inspection would prove the behavior?
