# Noreturn

> Canonical C topic note — chapter 35.

## Definition
A non-returning function is a function whose execution does not return to its caller. C23 provides the standard `[[noreturn]]` attribute. Earlier C versions commonly rely on implementation extensions such as compiler-specific `noreturn` attributes or `<stdnoreturn.h>` conventions where available.

The attribute is a semantic promise to the compiler and a documentation contract for reviewers; it is not an instruction that magically prevents a function from returning.

## Mechanism and language rules
A typical C23 declaration is:
```c
[[noreturn]] void panic(const char *reason);
```
A correctly implemented non-returning function normally loops forever, terminates the process, transfers control to a reset/fault mechanism, or otherwise never reaches its caller.

The optimizer can exploit the contract. If a function is declared non-returning but actually returns, behavior is not something a program should rely on; implementations may diagnose violations and optimize surrounding control flow based on the promise. Declaration consistency across translation units is therefore critical.

### What to reason about
- The attribute describes control-flow behavior, not error severity.
- Verify that every reachable path truly does not return.
- Keep declarations consistent between headers and definitions.
- Distinguish standard C23 syntax from GCC/Clang/MSVC or RTOS-specific extensions.

## Embedded implications
Non-returning functions are common for `panic`, watchdog failure, fatal assertion handlers, bootloader handoff, and unrecoverable hardware faults. Marking them correctly can eliminate dead paths and improve diagnostics while preventing misleading compiler warnings.

A firmware panic routine may disable interrupts, capture registers, persist a compact crash record, kick or deliberately expire the watchdog, and enter a reset loop. These operations must be designed for the execution context.

### Firmware review angle
Check startup/fault paths under optimization. Inspect generated control flow when a compiler believes a call cannot return. Ensure watchdog servicing, debug halts, and production reset behavior are intentional rather than accidental.

## Edge cases and failure modes
Do not mark a function `noreturn` merely because it normally fails. A function that can return on one error path must not be declared non-returning. Avoid placing cleanup after an unconditional non-returning call unless the design deliberately changes that contract.

Cross-module declaration mismatches are especially dangerous because the compiler may optimize each translation unit under a different assumption.

## Example pattern
```c
[[noreturn]] static void fatal_error(uint32_t code)
{
    record_fault(code);
    system_reset();
    for (;;) {
        /* Defensive fallback if reset unexpectedly returns. */
    }
}
```

## Verification / debugging
Compile with aggressive warnings and inspect control-flow diagnostics. Unit-test fatal handlers through an injectable backend rather than trying to return from them. On target, verify the actual reset/fault path and inspect disassembly around callers when optimizer behavior matters.

## Staff-level takeaway
`noreturn` is a control-flow contract. Use it only when the architecture truly guarantees non-return, because compilers can legitimately use the contract to transform code around the call.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
