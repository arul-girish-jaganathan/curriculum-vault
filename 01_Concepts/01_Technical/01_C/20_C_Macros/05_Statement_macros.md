# 05: Statement Macros

## Definition
A statement macro is a function-like macro designed to execute one or more imperative statements (assignments, function calls, control flow) rather than evaluating to an expression value. Naive statement macros that use simple braced blocks (`{ ... }`) introduce severe syntax and control-flow bugs when integrated into C conditional statements.

## Scope and Boundaries
Covers: Multi-statement macros, dangling-else bugs, semicolon swallowing, and control-flow jumps (`return`, `goto`) inside macros.
Does not cover: The `do { ... } while(0)` solution (see `06_do_while_0_idiom`) or expression macros.

## Why Does It Exist
Developers use statement macros to encapsulate common multi-step sequences—such as clearing a fault flag, logging an error, and releasing a mutex—under a single concise identifier.

## Mechanism and Language Rules
1. **Expression vs Statement:** In C grammar, an expression can yield a value and can appear inside `if (expr)`, whereas statements control execution flow and terminate with semicolons.
2. **Compound Statements (`{ ... }`):** A compound statement encloses multiple statements in braces. Crucially, a compound statement does NOT permit a trailing semicolon when used as the body of an `if` statement with an `else` branch.
3. **Control Flow Invariance:** Statements like `return` or `goto` inside macros alter caller execution flow silently, violating developer expectations.

## Examples
```c
#include <stdbool.h>

/* NAIVE ANTI-PATTERN 1: Sequential statements separated by commas */
#define NAIVE_RESET_1()    disable_irq(), reset_hw(), enable_irq()

/* NAIVE ANTI-PATTERN 2: Braced compound block */
#define NAIVE_RESET_2()     {         disable_irq();         reset_hw();         enable_irq();     }

/* HAZARDOUS CONTROL FLOW: Macro hiding a return statement */
#define CHECK_STATUS(ret)     do {         if ((ret) != 0) {             return (ret); /* Hidden return statement! */         }     } while(0)

static void test_dangling_else(bool condition) {
    /* DANGLING-ELSE COMPILATION FAILURE */
    if (condition)
        NAIVE_RESET_2(); /* Expands to: { ... }; -> The trailing ';' is an empty statement! */
    else
        enable_irq();
    /* Compiler Error: 'else' without a previous 'if' 
     * Because the semicolon after NAIVE_RESET_2() terminates the if statement before 'else'!
     */
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- Placing a semicolon after a braced compound macro inside an `if-else` construct violates C grammar, causing a compilation failure.

## Edge Cases and Failure Modes
- **The Semicolon Swallowing Syntax Error:**
  ```c
  if (flag)
      NAIVE_RESET_2(); /* Expands to: { disable_irq(); ... }; */
  else                 /* SYNTAX ERROR: 'else' has no matching 'if' */
      do_something();
  ```
- **Hidden Return Traps:** Macros containing `return` statements make it impossible to audit resource cleanup (e.g., a mutex remains permanently locked because the macro returned from the middle of the calling function).

## Embedded Implications
- **Lock Leaks in Critical Sections:** If a statement macro contains an early `return` or calls a fault handler that aborts execution, locks or interrupt-disable states acquired earlier in the caller are never restored, bricking the microcontroller.

## Firmware Review Angle
- Strictly forbid macros containing `return`, `goto`, `break`, or `continue`. Control flow must remain visible in the caller's source code.
- Check that all multi-statement macros are enclosed in `do { ... } while(0)`—reject simple braced blocks (`{ ... }`).

## Compiler, ABI, and Toolchain Implications
- Statement macros expand directly into the caller's AST block; variables declared inside compound macro blocks have block scope and are destroyed upon exiting the block.

## Performance, Memory, Timing, and Power
- Inlines statements directly into the function body. No function call overhead, but risks code bloat if the macro contains large blocks of logic.

## Verification / Debugging
- Debuggers cannot set breakpoints on individual statements inside a macro expansion; the debugger treats the entire macro as a single line of source code.

## Safety, Security, and Reliability
- Hidden control-flow changes violate MISRA C:2012 Rule 15.5 (functions should have a single point of exit) and Rule 14.3.

## Trade-offs and Alternatives
- **Statement Macro vs `static inline` Function:** A `static inline void` function handles multiple statements cleanly, respects trailing semicolons, allows local variable management, and can be single-stepped in a debugger.

## Staff-Level Takeaway
Never hide `return` or `goto` inside a macro. If a macro must execute multiple statements, wrap it exclusively using the `do { ... } while(0)` idiom. For complex multi-step sequences, always prefer `static inline void` functions to keep control flow explicit and debuggable.

## Related Concepts
- `02_Function_like_macros`
- `06_do_while_0_idiom`
- `11_When_inline_functions_are_safer`
