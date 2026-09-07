# Lifetime, Effective Type and Aliasing

## Chapter purpose
A deep-reference chapter in the C language knowledge base. Use it to understand the rule, reason about compiler and ABI effects, and apply it safely in embedded firmware.

## Topics
- [[01_Object_lifetime|Object lifetime]]
- [[02_Storage_duration|Storage duration]]
- [[03_Dangling_pointers|Dangling pointers]]
- [[04_Use_after_free|Use-after-free]]
- [[05_Effective_type|Effective type]]
- [[06_Strict_aliasing|Strict aliasing]]
- [[07_Character_type_access|Character-type access]]
- [[08_Union_aliasing_nuances|Union aliasing nuances]]
- [[09_restrict_and_alias_analysis|restrict and alias analysis]]
- [[10_Pointer_provenance_concerns|Pointer provenance concerns]]
- [[11_Lifetime_safe_APIs|Lifetime-safe APIs]]
- [[12_Sanitizer_backed_review|Sanitizer-backed review]]

## Review prompts
- What is guaranteed by ISO C?
- What depends on the implementation, ABI, compiler, libc, or target?
- What failure mode would appear on an embedded system?
- What test or inspection would prove the behavior?
