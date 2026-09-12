# Function declarators

## Core idea
A function declarator specifies a function's return type and parameter type structure. The parameter-list form matters: a prototype with explicit parameter types provides substantially stronger checking than an old-style declaration with an unspecified parameter list.

## ABI boundary
A function declaration is an ABI contract when the function crosses translation-unit, library, bootloader, plugin, or interrupt boundaries. Return type, parameter types, variadic status, calling convention extensions, and attributes can all affect generated calls.

## Embedded consequences
Callback APIs, ISR registration, RTOS hooks, driver interfaces, and boot/runtime entry points depend on exact function types. A mismatched function-pointer type can compile with a cast yet fail at runtime because argument registers, stack layout, return registers, or preserved registers do not match the actual ABI.

## Failure modes
- Calling through an incompatible function-pointer type.
- Omitting prototypes and relying on implicit historical assumptions.
- Assuming a cast makes an incompatible callback safe.
- Mixing compiler calling-convention extensions without documenting them.

## Verification
Keep function prototypes in shared headers, enable incompatible-pointer-type warnings, inspect generated calls for critical boundaries, and validate vendor/RTOS callback signatures directly against their documented ABI.

## Staff-level takeaway
Function type compatibility is stronger than “the call looks right.” At a binary boundary, the declaration must match the actual calling convention.
