# 04: Function Pointer Typedefs

## Definition
A function pointer `typedef` defines an alias for a pointer to a function with a specific return type and parameter signature. It de-obfuscates the notoriously complex and backwards declaration syntax of standard C function pointers, transforming nested callback signatures into readable, maintainable types.

## Scope and Boundaries
Covers: Function pointer alias syntax, callback architecture, jump tables, ISR vector tables, and signature validation.
Does not cover: Standard function declarations or non-standard calling convention keywords (unless specified by ABI).

## Why Does It Exist
Native C function pointer syntax is notoriously difficult to parse and write, especially when returning function pointers or declaring arrays of callbacks:
`void (*(*signal(int, void (*)(int)))(int));`
A `typedef` breaks this syntactic knot into clean, modular building blocks.

## Mechanism and Language Rules
1. **Declaration Syntax:** Place the `typedef` keyword before what would otherwise be a normal function pointer variable declaration:
   `typedef return_type (*alias_name_t)(param1_type, param2_type);`
2. **Type Compatibility:** Two function pointers are compatible if and only if their return types and parameter types are strictly compatible.
3. **Implicit Conversion:** In C, a function name decays implicitly into a pointer to that function (`&func` and `func` are equivalent).
4. **Invocation:** A function pointer variable can be invoked explicitly `(*fn)(arg)` or planarly `fn(arg)`.

## Examples
```c
#include <stdint.h>
#include <stdbool.h>

/* Clean function pointer typedefs */
typedef void (*button_callback_t)(uint8_t button_id, void *context);
typedef bool (*packet_handler_t)(const uint8_t *payload, uint16_t length);

/* Hardware Event Dispatch Table */
typedef void (*isr_vector_t)(void);

struct ButtonService {
    button_callback_t on_press;
    void             *user_context;
};

static void register_button(struct ButtonService *svc, button_callback_t cb, void *ctx) {
    if (svc) {
        svc->on_press = cb;
        svc->user_context = ctx;
    }
}

static void trigger_button(const struct ButtonService *svc, uint8_t btn) {
    if (svc && svc->on_press) {
        svc->on_press(btn, svc->user_context); /* Planar invocation */
    }
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- **Mismatched Signature Invocation:** Invoking a function pointer through an incompatible signature (e.g., casting a function expecting 3 parameters to a typedef expecting 1 parameter) invokes Undefined Behavior, typically causing stack corruption or register register misalignment.
- **Null Function Pointer Dereference:** Invoking a `NULL` function pointer triggers an immediate HardFault / Segfault.

## Edge Cases and Failure Modes
- **Casting Function Pointers:** Casting between function pointers and `void *` is undefined in ISO C (though required by POSIX for `dlsym`). On Harvard architecture MCUs, function pointers and data pointers have different sizes and address separate physical memories.
- **Omitting Context:** Declaring callbacks without a `void *context` parameter makes it impossible for the callback to access instance state without resorting to global variables.

## Embedded Implications
- **Interrupt Vector Tables:** Microcontroller startup code uses arrays of function pointer typedefs to define the hardware interrupt vector table:
  `const isr_vector_t g_pfnVectors[] __attribute__((section(".isr_vector"))) = { ... };`.
- **State Machines:** Function pointer typedefs form the core of table-driven state machine dispatchers.

## Firmware Review Angle
- Confirm that every callback typedef includes a `void *context` or `void *user_data` parameter.
- Ensure all function pointer invocations check for `NULL` prior to execution.
- Check that function pointers are never cast across mismatched signatures.

## Compiler, ABI, and Toolchain Implications
- ABI defines how function pointers are invoked: in ARM AAPCS, function pointers always have Bit 0 set to 1 to indicate Thumb mode execution. If Bit 0 is 0, executing it triggers an `INVSTATE` UsageFault.

## Performance, Memory, Timing, and Power
- Direct function calls use single-cycle branch instructions (`BL`). Function pointer calls require loading the address into a register and executing an indirect branch (`BLX R0`), which can induce branch predictor stalls.

## Verification / Debugging
- Static analysis checks for null dereferences and mismatched callback assignments.
- Debuggers can resolve function pointer addresses back to symbol names (`print cb` displays `&my_callback`).

## Safety, Security, and Reliability
- MISRA C:2012 Rule 11.1: Conversions shall not be performed between a pointer to a function and any other type.
- Unprotected function pointers in RAM are prime targets for Return-Oriented Programming (ROP) attacks and buffer overflow hijacking.

## Trade-offs and Alternatives
- **Function Pointers vs. Switch Dispatch:** Switch-case dispatch is fully inlinable, statically verifiable, and immune to pointer hijacking, but less modular than function pointer tables.

## Staff-Level Takeaway
Always use `typedef` to declare function pointers. Never design a callback typedef without an accompanying `void *context` argument. Treat function pointers in writable RAM as critical security surfaces and validate them against `NULL` before every call.

## Related Concepts
- `01_Basic_typedefs`
- `09_Readable_API_typedefs`
- `../12_Function_pointers`
