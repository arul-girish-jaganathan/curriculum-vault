# 06: The `do { ... } while(0)` Idiom

## Definition
The `do { ... } while(0)` idiom is the standard C mechanism for encapsulating multi-statement macros into a single syntactically robust compound statement. It ensures that the macro behaves identically to a standard C function call, requiring a trailing semicolon and integrating safely into all control-flow constructs (such as single-line `if-else` blocks).

## Scope and Boundaries
Covers: Syntax mechanics of `do-while(0)`, dangling-else resolution, trailing semicolon absorption, local variable scoping, and compiler dead-code elimination.
Does not cover: Loop constructs intended for actual iteration.

## Why Does It Exist
In C grammar, multi-statement macros wrapped in simple braces `{ ... }` fail when invoked inside `if` statements with `else` branches because the trailing semicolon creates an extraneous empty statement. Wrapping the block in `do { ... } while(0)` forces the entire construct to be parsed as a single statement that *demands* a trailing semicolon.

## Mechanism and Language Rules
1. **Single Statement Grammar:** A `do-while` loop is grammatically a single statement.
2. **Mandatory Semicolon:** The C language specification requires a semicolon after the closing parenthesis of `while(condition);`. Thus, writing `MY_MACRO();` results in valid grammar.
3. **Guaranteed Single Execution:** Because the condition expression is the constant `0`, the loop body executes exactly once.
4. **Dead-Code Elimination:** Every modern optimizing compiler recognizes `while(0)` as a compile-time constant false condition and optimizes away the loop test and branch instructions entirely.

## Examples
```c
#include <stdint.h>
#include <stdbool.h>

/* ROBUST: The canonical do-while(0) macro pattern */
#define SAFE_TRANSMIT_LOG(dev, data, len)     do {         uart_lock(dev);         uart_write_bytes(dev, data, len);         uart_unlock(dev);     } while(0)

/* Safe with local scoping */
#define SWAP(a, b, type)     do {         type _tmp = (a);         (a) = (b);         (b) = _tmp;     } while(0)

static void process_packet(bool is_valid) {
    /* Seamless integration with single-line if-else */
    if (is_valid)
        SAFE_TRANSMIT_LOG(0, "OK", 2); /* Parses cleanly with ';' */
    else
        SAFE_TRANSMIT_LOG(0, "ERR", 3); /* Semicolon does NOT break 'else'! */
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- Compiling `while(0)` does not produce implementation-defined behavior; its semantics are fully standardized by ISO C (§6.8.5.2).

## Edge Cases and Failure Modes
- **Using `break` Inside the Macro:** If a macro using `do { ... } while(0)` contains a `break` statement, the `break` terminates the macro's dummy `do-while` loop, NOT the caller's enclosing loop! This is a dangerous trap.
- **Variable Shadowing:** Declaring local temporary variables inside the `do { ... }` block without unique prefix names can shadow caller variables.

## Embedded Implications
- **Critical Section Atomicity:** Embedded firmware universally uses `do { ... } while(0)` to package atomic read-modify-write sequences:
  ```c
  #define CRITICAL_EXECUTE(code)       do {           uint32_t _primask = __get_PRIMASK();           __disable_irq();           code;           __set_PRIMASK(_primask);       } while(0)
  ```

## Firmware Review Angle
- Confirm that every multi-statement macro is wrapped in `do { ... } while(0)`. Reject simple `{ ... }` blocks immediately.
- Verify that `while(0)` has no trailing semicolon in the `#define` directive—the caller must supply the semicolon: `MACRO();`.
- Audit macro bodies to ensure they do not contain `break` statements.

## Compiler, ABI, and Toolchain Implications
- With optimization enabled (`-O1`, `-O2`, `-Os`), GCC, Clang, and ARM Compiler emit zero loop overhead for `do-while(0)`. The assembly matches a flat sequence of instructions.

## Performance, Memory, Timing, and Power
- Zero instruction overhead. Zero execution cycle penalty.

## Verification / Debugging
- Check `-Wempty-body` and `-Wextra` compiler outputs to ensure clean AST generation.
- Use `gcc -E` to verify semicolon placement in expanded statements.

## Safety, Security, and Reliability
- MISRA C:2012 Rule 20.7 and Rule 14.3: `do { ... } while(0)` is explicitly recognized and permitted as a valid deviation for macro statement encapsulation.

## Trade-offs and Alternatives
- **`do { ... } while(0)` vs `static inline` Function:** While `do-while(0)` solves the syntax problem, `static inline` functions provide superior type safety and avoid variable shadowing risks.

## Staff-Level Takeaway
Whenever a macro contains multiple statements, `do { ... } while(0)` is the only grammatically correct wrapper in ISO C. It guarantees safe semicolon consumption, resolves dangling-else syntax failures, and optimizes to zero overhead in machine code.

## Related Concepts
- `02_Function_like_macros`
- `05_Statement_macros`
- `11_When_inline_functions_are_safer`
