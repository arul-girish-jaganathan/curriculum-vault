# 07: assert.h

## Definition
`<assert.h>` provides the `assert` macro for expressing conditions that must hold at a particular program point during development or diagnostic builds. A failed assertion invokes the implementation-defined diagnostic/failure mechanism; when `NDEBUG` is defined before including the header, assertions are disabled.

## Scope and Boundaries
* **Covers:** `assert`, `NDEBUG`, expression evaluation, diagnostic behavior, and embedded use.
* **Does not cover:** contracts as a formal language feature, recovery-oriented error handling, or application logging frameworks.

## Why Does It Exist
Assertions document invariants that should be impossible to violate in a correctly functioning program. They turn hidden assumptions into executable checks during development, making failures local and easier to diagnose.

## Mechanism and Language Rules
1. `assert(condition)` evaluates the expression when assertions are enabled.
2. A false condition triggers the implementation-defined assertion failure behavior.
3. Defining `NDEBUG` before including `<assert.h>` disables assertions; the expression is still parsed by the compiler but is not evaluated by the standard macro definition's disabled form.
4. Assertion expressions therefore must not contain required side effects.
5. In C23, the assertion facilities were modernized, so the project's language mode should be checked before relying on newer forms.

## Examples
```c
#include <assert.h>
#include <stddef.h>

static int get_byte(const unsigned char *buffer, size_t length, size_t index)
{
    assert(buffer != NULL);
    assert(index < length);
    return buffer[index];
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
* Putting essential side effects inside `assert`, such as `assert(i++ < 4)`, creates debug/release semantic divergence because the expression may disappear with `NDEBUG`.
* Dereferencing an invalid pointer inside an assertion can itself invoke undefined behavior before the assertion can report anything.
* The exact diagnostic text and process termination mechanism are implementation-defined.
* An assertion is not a substitute for checking untrusted runtime input.

## Edge Cases and Failure Modes
* `assert(ptr && ptr->field)` may still be safe only if `ptr` is a valid pointer; non-null does not mean dereferenceable.
* Conditions that are expensive can distort performance measurements in debug builds.
* Assertions on normal external failures create fragile production behavior if they disappear entirely in release.
* Multiple translation units must agree on the intended `NDEBUG` policy.

## Embedded Implications
Assertions are valuable in firmware for catching corrupted state, invalid indexes, and broken internal invariants. On a production MCU, failed assertions may need to record fault context, reset, enter a safe state, or expose telemetry instead of simply writing to stderr. Flash/RAM and timing costs therefore matter.

## Firmware Review Angle
Separate **programmer errors/internal invariants** from **expected environmental failures**. Check that assertions do not protect memory safety against untrusted inputs in a way that disappears in release. Verify the production failure policy and the consistency of `NDEBUG` across all builds.

## Compiler, ABI, and Toolchain Implications
Compilers know that assertion code may disappear under `NDEBUG`, enabling different control-flow graphs in debug and release. Assertions can improve static reasoning by exposing predicates. In safety-oriented builds, compiler options and preprocessor configuration should be captured as build artifacts so the exact assertion policy is reproducible.

## Performance, Memory, Timing, and Power
Enabled assertions add conditional branches, reads, and potentially formatting/failure-reporting code. They can significantly affect timing in tight loops. They should not be benchmarked as though their debug overhead represents production behavior, and production-critical assertions should be designed with bounded fault-handling cost.

## Verification / Debugging
* Build with assertions enabled for unit and integration testing.
* Deliberately trigger key invariants and verify captured context.
* Build with `NDEBUG` and inspect the resulting assembly for accidental dependence on assertion side effects.
* Combine assertions with sanitizers and static analysis to detect the defect that violated the invariant.

## Safety, Security, and Reliability
Do not use assertions as input validation for attackers or unreliable hardware. A missing assertion in a release build must not turn a malformed packet into memory corruption. Internal invariants should be backed by explicit production checks when violation could cause unsafe behavior.

## Trade-offs and Alternatives
* **Use assertions:** for impossible states, internal invariants, and developer assumptions.
* **Use explicit error handling:** for recoverable runtime failures and untrusted inputs.
* **Use fail-safe mechanisms:** when invariant violation requires controlled shutdown or degraded operation.

## Staff-Level Takeaway
Assertions are executable documentation of invariants, not a general error-handling mechanism. A Staff engineer should classify every assertion as either a diagnostic aid or a production safety boundary and ensure the build configuration matches that intent.

## Related Concepts
* [[00_Chapter_Index]]
* [[../35_C_Assertions_Attributes/00_Chapter_Index]]
* [[../42_C_Error_Handling/00_Chapter_Index]]
* [[../39_C_Diagnostics_Static_Analysis/00_Chapter_Index]]
* [[../40_C_Sanitizers_Fuzzing/00_Chapter_Index]]

---
*Related: [[00_Chapter_Index]], [[../00_Complete_Topic_Map]]*