# 12: Macro Review Checklist

## Definition
The macro review checklist is a comprehensive engineering audit standard applied during code reviews and pull request sign-offs. It systematically validates macro definitions against syntactic, semantic, safety (MISRA C), and architectural requirements to prevent defect injection into production firmware.

## Scope and Boundaries
Covers: Production code review criteria, defensive syntax verification, concurrency and side-effect checks, MISRA compliance gates, and documentation standards.
Does not cover: Build system configuration or test harness scripting.

## Why Does It Exist
Macros bypass the compiler's semantic type checker and operate via textual substitution. Defects in macro definitions often produce obscure compiler errors far from the definition site, cause silent data corruption, or introduce severe race conditions. A formal checklist ensures that every macro is rigorously audited before merging.

## The Production Macro Review Checklist

### 1. Architectural Justification
- [ ] **Could this be a `static inline` function?** If it performs arithmetic, logic, or register manipulation, it MUST be an inline function unless macro features are mandatory.
- [ ] **Could this be an enumeration or `const` variable?** If it defines a scalar constant, prefer `enum { VAL = 100U }` or `static const`.

### 2. Naming & Namespacing
- [ ] **Is the macro name ALL_CAPS?** (e.g., `MODULE_CONFIG_TIMEOUT`).
- [ ] **Does the macro have a distinct module prefix?** (e.g., `HAL_UART_...`).
- [ ] **Are private helper macros in `.c` files `#undef`'d after use?**
- [ ] **Does the name avoid standard C reserved identifiers?** (No leading underscores followed by uppercase).

### 3. Parentheses & Precedence Discipline
- [ ] **Is EVERY parameter in the macro body wrapped in parentheses?** `((x) * 2)`
- [ ] **Is the overall macro replacement expression wrapped in outer parentheses?** `#define ADD(a, b) ((a) + (b))`
- [ ] **Are compound bitwise expressions explicitly grouped?** `(((reg) & (mask)) == (mask))`

### 4. Side Effects & Evaluation Safety
- [ ] **Are any parameters evaluated more than once?** If yes, verify that the macro cannot be invoked with side effects (`i++`, hardware reads).
- [ ] **Are multi-statement macros wrapped in `do { ... } while(0)`?**
- [ ] **Does the macro avoid control-flow keywords?** (`return`, `goto`, `break`, `continue` are forbidden inside macros).

### 5. Type & Literal Correctness
- [ ] **Do integer literals have explicit unsigned suffixes where appropriate?** (`U`, `UL`).
- [ ] **Are bit shifts protected against signed integer overflow?** `(1UL << 31U)`.
- [ ] **Does the macro avoid trailing semicolons in the `#define` directive?**

### 6. Variadic, Stringize & Token-Pasting Checks
- [ ] **Do stringification (`#`) and token-pasting (`##`) macros use two-tier indirection?**
- [ ] **Do variadic logging macros handle zero variable arguments portably?** (`__VA_OPT__` or `, ## __VA_ARGS__`).
- [ ] **Do disabled debug macros expand to `((void)0)`?**

### 7. MISRA C:2012 Compliance
- [ ] **Dir 4.9:** Functions used in preference to function-like macros.
- [ ] **Rule 20.7:** Macro parameter expressions enclosed in parentheses.
- [ ] **Rule 20.10:** `#` and `##` operators justified with documented safety deviations.

## Examples: Reviewing a Pull Request
```c
/* ================= DEFECTIVE MACRO IN PULL REQUEST ================= */
#define set_threshold(val)     hw_lock();     REG_THRES = val * 2;     hw_unlock();

/* CRITICAL DEFECTS FOUND DURING REVIEW:
 * 1. Lowercase name (violates naming convention).
 * 2. Missing module prefix (pollutes global namespace).
 * 3. Multi-statement macro NOT wrapped in do { ... } while(0).
 * 4. Missing parentheses around 'val' in 'val * 2'.
 * 5. Missing outer parentheses.
 * 6. Could and SHOULD be a static inline function!
 */

/* ================= REFACTORED & APPROVED IMPLEMENTATION ============= */
static inline void hal_sensor_set_threshold(uint32_t val) {
    hw_lock();
    REG_THRES = val * 2U;
    hw_unlock();
}
```

## Staff-Level Takeaway
Never approve a macro that could be implemented as a `static inline` function. When a macro is strictly necessary, execute this checklist line-by-line: enforce complete parenthesis isolation, mandate `do { ... } while(0)` wrappers, verify unsigned literal suffixes, and ensure strict module namespacing.

## Related Concepts
- `03_Parentheses_discipline`
- `04_Multiple_evaluation`
- `06_do_while_0_idiom`
- `10_Macro_namespaces`
- `11_When_inline_functions_are_safer`
