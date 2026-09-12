# Variadic macros

## Definition
A variadic macro is a C preprocessor macro that accepts a variable number of arguments. It is commonly declared with `...` and uses `__VA_ARGS__` to substitute the variable argument sequence.

Example:

```c
#define LOG(fmt, ...) log_impl(fmt, __VA_ARGS__)
```

C99 standardized variadic macros. C23 additionally provides `__VA_OPT__`, which allows a macro to conditionally emit tokens when the variable argument sequence is non-empty.

## Scope and Boundaries
* **Covers:** `...`, `__VA_ARGS__`, empty argument lists, `__VA_OPT__`, comma handling, expansion, and embedded logging patterns.
* **Does not cover:** runtime variadic functions, which use `<stdarg.h>` and are covered in [[01_va_list]]–[[07_printf_like_APIs]].

## Why Does It Exist
Macros operate before C compilation and can capture source-level context that a function cannot, such as `__FILE__`, `__LINE__`, `__func__`, compile-time feature flags, or optional arguments.

Variadic macros are particularly useful for debug logging, assertions, tracing, and lightweight wrappers around runtime variadic functions.

## Mechanism and Language Rules
A simple C99 macro is:

```c
#define TRACE(fmt, ...) trace_impl(__FILE__, __LINE__, fmt, __VA_ARGS__)
```

The preprocessor substitutes the variable arguments into the replacement list. This is not the same operation as a runtime `va_list`; no runtime argument traversal is performed by the macro itself.

C23's `__VA_OPT__` provides a standard solution to the trailing-comma problem:

```c
#define LOG(fmt, ...) log_impl(fmt __VA_OPT__(,) __VA_ARGS__)
```

With no variable arguments, the comma inside `__VA_OPT__` disappears; with one or more, it remains.

### What to reason about
- Is the macro expansion syntactically valid for zero and non-zero variable arguments?
- Does each argument appear exactly once, or can macro expansion duplicate side effects?
- Is the result a single statement when used in control flow?
- Are arguments safely parenthesized?
- Does the macro depend on C99/C23 or compiler extensions?
- Is the runtime function behind the macro type-checked as a printf-like interface?

## Examples

### Statement-safe wrapper
```c
#define LOG_INFO(fmt, ...) \
    log_impl("INFO", __FILE__, __LINE__, fmt, __VA_ARGS__)
```

For portable handling of empty variable arguments across modern C versions, prefer a design compatible with the language version used by the project; in C23, `__VA_OPT__` is the cleanest standard mechanism.

### C23 form
```c
#define LOG(fmt, ...) \
    log_impl(fmt __VA_OPT__(,) __VA_ARGS__)
```

## Undefined, Unspecified, and Implementation-Defined Behavior
* Macro expansion follows preprocessing rules rather than runtime C evaluation rules.
* The handling of an empty `__VA_ARGS__` sequence in older C versions can require careful syntax; many historical solutions rely on compiler extensions such as GNU comma swallowing.
* Token-pasting and stringification change expansion behavior and can produce surprising results if the macro argument is itself another macro.
* A macro can expand to syntactically invalid C even though its definition is accepted; correctness depends on each invocation context.

## Edge Cases and Failure Modes
* **Dangling `else`:** a multi-statement macro without a `do { ... } while (0)` wrapper can break an enclosing `if/else`.
* **Multiple evaluation:** `MAX(x++, y++)`-style macros can execute arguments more than once.
* **Comma expressions:** commas inside macro arguments are protected by parentheses, but the preprocessor's argument parsing is not the same as C's runtime comma operator.
* **Empty variadic arguments:** portability differs across language versions and compiler extensions.
* **Format safety:** the macro does not magically validate a format string; the underlying function needs compiler-aware checking.
* **Side effects:** `LOG("x=%d", expensive())` still executes `expensive()` unless the macro is compiled out in a way that prevents expansion/evaluation.

## Embedded Implications
Variadic logging macros can add source-level context without requiring every call site to manually pass file and line information. They can also compile to nothing in production builds when designed carefully.

However, macros can make code size and timing difficult to reason about because each invocation expands independently. A high-rate logger may therefore duplicate formatting call sites and constants throughout the image.

### Firmware Review Angle
Define explicit build-time behavior for disabled logging. Verify that disabled macros do not evaluate arguments with side effects. Ensure logging from ISRs does not invoke blocking runtime formatting.

Avoid compiler-extension-only comma tricks in portable product code unless the compiler/toolchain is deliberately fixed and the dependency is documented.

## Compiler, ABI, and Toolchain Implications
The preprocessor expands macros before the compiler sees them. Consequently, ABI issues belong to the expanded runtime call, while macro correctness belongs to preprocessing/token rules.

Use compiler-specific format attributes on the runtime logger where available so that calls through the macro still receive format checking. Inspect preprocessor output (`-E` on GCC/Clang) when debugging expansion problems.

## Performance, Memory, Timing, and Power
Macro expansion itself has no runtime cost, but it can duplicate code and constants. If a macro expands to a function call, the function call's cost remains.

Disabled logging can be nearly free when the preprocessor removes the complete expression, but a poorly designed disabled macro can still evaluate expensive arguments or retain string literals.

## Verification / Debugging
Compile representative invocations with zero, one, and many variable arguments. Test use inside `if/else`, loops, and nested macros. Inspect preprocessor output for complicated wrappers.

For embedded builds, compare map files with logging enabled and disabled, and verify that disabled calls produce no unexpected references or flash-resident strings.

## Safety, Security, and Reliability
Macros are not type-safe and can hide control flow. Keep them small, document language-version requirements, and avoid macro interfaces where an inline function can express the same behavior.

Never let macro-generated logging turn attacker-controlled text into a format string.

## Trade-offs and Alternatives
* **Use:** compile-time logging, assertions, source-location injection, optional diagnostics.
* **Avoid:** complex logic, resource management, or interfaces that can be ordinary functions.
* **Alternatives:** `static inline` functions, C23 `__VA_OPT__`, `_Generic`, typed event APIs, and compiler-supported tracing facilities.

## Staff-Level Takeaway
A variadic macro is a preprocessor interface, not a variadic function. A Staff engineer should separate preprocessing semantics from runtime argument semantics, control side effects and empty-argument behavior, verify the expanded code, and define exactly which C/compiler versions the macro contract supports.

## Related Concepts
* [[00_Chapter_Index]]
* [[01_va_list]]
* [[05_Default_argument_promotions]]
* [[06_Format_strings]]
* [[07_printf_like_APIs]]
* [[09_ABI_details]]
