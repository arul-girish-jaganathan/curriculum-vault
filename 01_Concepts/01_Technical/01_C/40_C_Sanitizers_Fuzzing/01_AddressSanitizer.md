# AddressSanitizer

> Canonical C topic note — chapter 40.

## Definition
AddressSanitizer (ASan) is a compiler/runtime instrumentation technique for detecting many memory-safety errors, including out-of-bounds accesses and use-after-free. It is primarily a development/test tool, not a replacement for a production memory-safety strategy.

## Mechanism and language rules
Instrumentation surrounds memory accesses and uses shadow metadata to identify poisoned red zones and invalid regions. Reports typically identify the access, stack trace, allocation/free history, and memory region.

## Embedded implications
ASan is often easiest on a host build because embedded targets may lack RAM, address-space, runtime, or debugger support. Host testing can still exercise protocol parsing, state machines, serializers, allocators, and other target-independent logic.

## Edge cases and failure modes
ASan does not prove absence of all UB, does not model every hardware register, and may not catch bugs outside its instrumentation coverage. Instrumentation changes memory layout and timing, so an ASan firmware image is not timing-equivalent to production.

## Verification / debugging
Run deterministic reproductions under ASan, preserve the first useful stack trace, and reduce the input. Combine with UBSan, static analysis, fuzzing, and targeted hardware tests. Never “fix” a report by suppressing it before understanding the lifetime/bounds contract.

## Staff-level takeaway
Use ASan as a high-sensitivity memory bug detector in a layered verification strategy, with host/target boundaries explicitly documented.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
