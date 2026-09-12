# 10: Enumerations

## Definition
An enumeration (`enum`) is a distinct scalar integer type in C whose values are defined by a list of named integer enumeration constants. In ISO C, enumeration constants have the type `int`, and each constant is associated with a specific signed or unsigned integer value.

## Scope and Boundaries
Covers: Enum syntax, explicit/implicit constant assignment, scoping rules, and state machine modeling.
Does not cover: C++ strongly typed scoped enums (`enum class`) or toolchain-specific packing attributes (see `11_Enum_portability`).

## Why Does It Exist
Enumerations provide semantic naming for discrete states, error codes, and configuration options. They eliminate magic numbers, enable compiler-level switch exhaustiveness checking, and improve debugging clarity.

## Mechanism and Language Rules
1. **Enumeration Constant Type:** In ISO C, all enumeration constants are strictly of type `int`. They are compile-time integer constant expressions.
2. **Implicit Numbering:** The first constant defaults to 0. Subsequent constants increment by 1 unless explicitly assigned.
3. **Shared Scope:** Enums share the ordinary identifier namespace. Two enums declared in the same scope cannot share constant names.
4. **Permissive Assignment:** In ISO C, an `enum` variable can be freely assigned any integer value without a cast, even if that value does not correspond to any declared enumeration constant.

## Examples
```c
#include <assert.h>

/* Explicit values for wire protocol and state stability */
typedef enum {
    SM_STATE_UNINITIALIZED = 0,
    SM_STATE_IDLE          = 10,
    SM_STATE_RUNNING       = 20,
    SM_STATE_FAULT         = 99
} StateMachineState;

static StateMachineState step_state_machine(StateMachineState current) {
    switch (current) {
        case SM_STATE_UNINITIALIZED:
            return SM_STATE_IDLE;
        case SM_STATE_IDLE:
            return SM_STATE_RUNNING;
        case SM_STATE_RUNNING:
            return SM_STATE_RUNNING;
        case SM_STATE_FAULT:
            return SM_STATE_IDLE;
        /* Omitting default allows -Wswitch to catch unhandled states */
    }
    return SM_STATE_FAULT;
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- **Permissive Out-of-Range Values:** Storing an integer value outside the range of declared constants into an enum variable is permitted by ISO C as long as the value fits in the underlying integer type.
- **Underlying Type Selection:** The compiler selects an implementation-defined integer type capable of representing all constant values (usually `int` or `unsigned int`).

## Edge Cases and Failure Modes
- **Namespace Pollution:** Because enum constants reside in the global/file scope, common names like `RESET`, `READY`, or `TIMEOUT` easily collide across header files.
- **Type Safety Illusion:** C does not prevent assigning an `ErrorStatus` enum to a `SensorState` enum variable without warnings, creating false expectations of type safety.

## Embedded Implications
- **State Machines:** Enums are the primary mechanism for implementing deterministic Finite State Machines (FSMs) in embedded controllers.
- **Switch Table Optimization:** Contiguous enum values starting at 0 allow compilers to generate dense, single-cycle branch tables (`TBH` / `TBB` instructions on ARM) instead of sequential comparison branches.

## Firmware Review Angle
- Check that `switch` statements over enums omit the `default:` branch during internal state transitions to allow `-Wswitch` to flag missing states at compile time.
- Enforce unique prefix naming conventions (e.g., `MODULE_STATE_*`) to avoid identifier namespace collisions.

## Compiler, ABI, and Toolchain Implications
- By default, standard C ABI treats enums as 4-byte `int` types, even if the maximum constant is 1.

## Performance, Memory, Timing, and Power
- Dense enum sequences (0, 1, 2, 3...) produce compact jump tables, reducing branch mispredictions and code footprint.
- Large gaps (0, 1000, 50000) force compilers to emit nested conditional branches instead of jump tables, increasing execution latency.

## Verification / Debugging
- Enable `-Wswitch -Wswitch-enum` to enforce total switch coverage.
- Debuggers display symbolic names (e.g., `SM_STATE_IDLE`) instead of raw numbers.

## Safety, Security, and Reliability
- MISRA C:2012 Rule 10.1: Operands shall not be used in expressions which result in inappropriate essential type categories.
- MISRA C:2012 Rule 10.3: The value of an expression shall not be assigned to an object with a narrower essential type or different essential type category.

## Trade-offs and Alternatives
- **Enum vs. `#define`:** Enums provide symbolic debugger visibility, scoping boundaries, and compiler switch checking, whereas `#define` macros lack type metadata and debugger symbols.

## Staff-Level Takeaway
Use enums for state machines and configuration sets. Always prefix constants with module tags to prevent namespace pollution. Keep values contiguous to enable optimal compiler jump-table generation, and omit `default` in internal switch statements to enforce compile-time exhaustiveness.

## Related Concepts
- `00_Chapter_Index`
- `11_Enum_portability`
