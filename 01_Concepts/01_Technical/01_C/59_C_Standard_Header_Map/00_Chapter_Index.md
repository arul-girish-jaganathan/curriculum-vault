# Standard Header Map and API Selection

## Chapter purpose
A deep-reference chapter in the C language knowledge base. Use it to understand the rule, reason about compiler and ABI effects, and apply it safely in embedded firmware.

## Topics
- [[01_Header_to_facility_map|Header-to-facility map]]
- [[02_assert_h|<assert.h>]]
- [[03_ctype_h|<ctype.h>]]
- [[04_errno_h|<errno.h>]]
- [[05_inttypes_h|<inttypes.h>]]
- [[06_math_h|<math.h>]]
- [[07_setjmp_h|<setjmp.h>]]
- [[08_signal_h|<signal.h>]]
- [[09_stdatomic_h|<stdatomic.h>]]
- [[10_stdio_h|<stdio.h>]]
- [[11_stdlib_h|<stdlib.h>]]
- [[12_string_h|<string.h>]]

## Review prompts
- What is guaranteed by ISO C?
- What depends on the implementation, ABI, compiler, libc, or target?
- What failure mode would appear on an embedded system?
- What test or inspection would prove the behavior?
