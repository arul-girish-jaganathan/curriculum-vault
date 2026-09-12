# sigsetjmp-style concepts

> Canonical C topic note — chapter 34.

## Definition
`sigsetjmp()` and `siglongjmp()` are POSIX-style extensions associated with non-local control flow and signal-mask state. They are **not ISO C interfaces**. This note exists to explain the distinction because production embedded/Unix-like code often encounters them alongside `setjmp()` and `longjmp()`.

The key difference is that a POSIX environment can optionally save and restore the process signal mask along with the execution context. The exact behavior depends on the `savesigs` argument and implementation.

## Mechanism and language rules
Conceptually:

```c
if (sigsetjmp(env, 1) == 0) {
    /* protected region */
} else {
    /* resumed after siglongjmp */
}
```

With signal-mask saving enabled, `siglongjmp()` can restore both the saved execution context and the associated signal-mask state. This is valuable in code where asynchronous signal blocking is part of the recovery invariant.

Because these APIs are outside ISO C, portability requires an explicit platform layer.

### What to reason about
- `sigjmp_buf` is an opaque POSIX type.
- Signal-mask restoration is distinct from ordinary register/stack context restoration.
- `sigsetjmp()` has the same broad non-local-control-flow hazards as `setjmp()`.
- The environment must remain valid; jumping into a returned function is invalid.
- POSIX imposes additional rules concerning signal handlers and asynchronous contexts.
- Do not replace `sigsetjmp()` with ISO C `setjmp()` when signal-mask semantics are part of correctness.

## Embedded implications
A freestanding MCU normally has no POSIX signal mask, so these APIs are usually unavailable. If an embedded Linux/Unix-class system uses them, treat them as operating-system primitives rather than portable C.

The analogous embedded problem is often restoring interrupt-enable/mask state after an exceptional control transfer. That should be handled by the RTOS/CPU exception model or explicit cleanup, not by assuming POSIX signal-mask semantics exist.

### Firmware review angle
Ask whether the design really needs non-local control flow and whether the platform abstraction can preserve all relevant asynchronous state. Document which state is restored automatically and which state remains the caller's responsibility.

## Edge cases and failure modes
Hazards include:
- assuming `sigsetjmp()` is standard C;
- misunderstanding the `savesigs` parameter;
- restoring a signal mask that the caller no longer expects;
- using the saved environment after its owning stack frame has ended;
- combining signal-handler recovery with locks, allocation, or stdio;
- porting the code to a freestanding MCU where the entire facility is absent.

A particularly subtle issue is treating execution context and asynchronous-delivery state as one thing. They are separate pieces of system state and must both be modeled.

## Example pattern
```c
/* POSIX-style example; not ISO C. */
#include <setjmp.h>

static sigjmp_buf env;

static void recover(void)
{
    siglongjmp(env, 1);
}

static void run(void)
{
    if (sigsetjmp(env, 1) == 0) {
        /* Protected POSIX signal-aware operation. */
        recover();
    } else {
        /* Recovery after context and selected signal state are restored. */
    }
}
```

## Verification / debugging
On POSIX systems, test both `savesigs == 0` and `savesigs != 0` where relevant, and inspect the signal mask before and after recovery. On embedded ports, ensure the feature is isolated behind a platform abstraction and has a documented replacement or compile-time exclusion.

Staff-level questions:
- Which parts are ISO C and which are POSIX?
- Does signal-mask restoration form part of the correctness proof?
- What happens on the target platform where this API does not exist?
- Can explicit state propagation eliminate the non-local jump?

## Staff-level takeaway
`sigsetjmp`-style APIs are a reminder that **C syntax can hide operating-system contracts**. Keep POSIX-specific non-local control flow isolated, document the extra asynchronous state being restored, and never present it as portable ISO C.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
