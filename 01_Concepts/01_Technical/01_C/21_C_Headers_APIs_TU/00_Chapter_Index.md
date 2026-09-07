# Headers, APIs and Translation Units

## Chapter purpose
A deep-reference chapter in the C language knowledge base. Use it to understand the rule, reason about compiler and ABI effects, and apply it safely in embedded firmware.

## Topics
- [[01_Public_headers|Public headers]]
- [[02_Private_headers|Private headers]]
- [[03_Include_guards|Include guards]]
- [[04_External_declarations|External declarations]]
- [[05_Definition_ownership|Definition ownership]]
- [[06_Opaque_interfaces|Opaque interfaces]]
- [[07_Header_self_sufficiency|Header self-sufficiency]]
- [[08_Dependency_direction|Dependency direction]]
- [[09_Circular_include_avoidance|Circular include avoidance]]
- [[10_API_versioning|API versioning]]
- [[11_Linkage_hygiene|Linkage hygiene]]
- [[12_Embedded_module_boundaries|Embedded module boundaries]]

## Review prompts
- What is guaranteed by ISO C?
- What depends on the implementation, ABI, compiler, libc, or target?
- What failure mode would appear on an embedded system?
- What test or inspection would prove the behavior?
