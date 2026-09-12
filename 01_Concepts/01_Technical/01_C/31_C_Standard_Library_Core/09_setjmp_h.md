# setjmp.h

> Canonical C topic note — chapter 31.

## Definition
`setjmp.h` provides `jmp_buf`, `setjmp`, and `longjmp` for saving an execution environment and later performing non-local control transfer. `setjmp` initially returns zero; a later `longjmp` causes execution to resume at the saved point with a nonzero value. The facility is ISO C, but the representation of `jmp_buf`, saved registers, stack state, ABI details, and implementation cost are platform-specific.

This is not normal function return. Intermediate C stack frames are abandoned and normal cleanup code in those frames is not executed. Therefore `setjmp`/`longjmp` should be treated as a specialized recovery mechanism rather than a general exception system.

## Mechanism and language rules
```c
#include <setjmp.h>

static jmp_buf env;

static void fail(void)
{
    longjmp(env, 1);
}

int operation(void)
{
    int rc = setjmp(env);
    if (rc == 0) {
        fail();
        return 0;
    }
    return -1;
}
```

`longjmp(env, value)` transfers control back to the invocation of `setjmp` associated with `env`. If `value` is zero, the resumed `setjmp` observes one. The saved environment becomes invalid once the function invocation containing the corresponding `setjmp` has returned.

### What to reason about
- `jmp_buf` is opaque; do not depend on its representation or size.
- `setjmp` has special language-level restrictions on where its invocation may appear.
- `longjmp` does not unwind intermediate functions and does not perform C++-style destruction.
- Automatic objects modified after `setjmp` have special rules; values of non-`volatile` automatic objects changed between the calls cannot safely be assumed to retain the changed value after `longjmp`.
- A jump into an expired function activation is invalid.
- Signal handling introduces additional restrictions and must not be confused with an RTOS or hardware exception context.
- The mechanism restores an execution environment, not an arbitrary system state: locks, peripherals, DMA, transactions, and ownership still require explicit recovery.

## Embedded implications
A saved environment may contain stack/register context whose size and implementation depend on the target ABI. This can consume RAM and complicate worst-case stack analysis. `jmp_buf` is not an RTOS task context and must not be used as a replacement for scheduler or interrupt context switching.

Non-local control flow can bypass cleanup such as releasing a software lock, disabling a peripheral transaction, returning a buffer to a pool, or restoring protocol state. In safety-oriented firmware, explicit error returns and state machines are normally easier to analyze.

### Firmware review angle
Review whether the jump:
- remains on the same task/stack and within the environment lifetime;
- can cross interrupt, exception, or scheduler boundaries;
- leaves critical sections, locks, DMA, or peripheral state inconsistent;
- behaves correctly with optimization, stack protection, CFI, and MPU features;
- makes fault diagnosis harder than an explicit error path.

## Edge cases and failure modes
A common mistake is expecting this to behave like returning through every intermediate function. Those functions are abandoned. Another is assuming a local variable retains a value assigned after `setjmp`.

```c
int x = 0;
if (setjmp(env) == 0) {
    x = 42;
    longjmp(env, 1);
}
/* Do not design around x necessarily being 42 here. */
```

Other hazards include jumping after the saved function has returned, using an environment from another task, assuming a particular `jmp_buf` layout, and skipping required cleanup. These errors can become optimization-sensitive and may manifest as apparently random crashes.

## Example pattern
Keep the jump boundary narrow and recovery explicit:

```c
int decode_packet(const void *buf)
{
    if (setjmp(env) != 0) {
        parser_reset();
        return -1;
    }

    return parse_packet(buf);
}
```

For most embedded designs, prefer ordinary error propagation:

```c
int rc = parse_header(buf);
if (rc != 0) {
    parser_reset();
    return rc;
}
```

## Verification / debugging
Test both initial and resumed `setjmp` paths and verify every resource remains consistent after recovery. Run debug and optimized builds. Inspect generated assembly when ABI behavior matters, and use compiler diagnostics, static analysis, sanitizers on host builds, and target fault instrumentation.

Staff-level questions:
- What cleanup can this jump bypass?
- Why is this better than an error return or state machine?
- Is the saved environment guaranteed to remain live?
- Which stack/task owns it?
- How is recovery proven under optimization and fault injection?

## Staff-level takeaway
`setjmp`/`longjmp` is powerful precisely because it escapes normal structured control flow. The engineering challenge is preserving lifetime, ABI correctness, resource ownership, compiler-visible state, and system invariants across that escape. In embedded firmware, use it only at a tightly controlled recovery boundary with explicit justification.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
