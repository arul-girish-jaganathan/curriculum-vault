# longjmp

> Canonical C topic note — chapter 34.

## Definition
`longjmp()` restores a previously saved execution environment and transfers control to the corresponding `setjmp()` invocation. It is a **non-local jump**: intermediate function returns do not occur normally.

The second argument is delivered as the resumed `setjmp()` result. If that argument is zero, `setjmp()` behaves as though it returned a nonzero value, so callers must understand the normalization rule and normally pass a nonzero recovery code.

## Mechanism and language rules
The conceptual sequence is:

```text
A() -> B() -> C()
        setjmp(jb) in B
              ^
              │ longjmp(jb, code) from C
              │
A() -> B() resumes at setjmp with nonzero result
```

The stack frames between the `longjmp()` caller and the saved environment are abandoned as control transfers. Their normal automatic cleanup does not happen because C has no general destructor mechanism.

The target environment must still be active. Jumping to an environment belonging to a function invocation that has already returned produces undefined behavior.

### What to reason about
- `longjmp()` does not return to its caller.
- The saved `jmp_buf` must have been established by an active `setjmp()` invocation in the same execution context allowed by the implementation.
- Automatic objects changed between `setjmp()` and `longjmp()` can have indeterminate values unless protected by the applicable `volatile` rule.
- Resources are not automatically released: locks, allocations, open transactions, DMA ownership, peripheral configuration, and other application state require explicit design.
- Signal interactions can add additional constraints; do not assume POSIX `siglongjmp` semantics from ISO C `longjmp`.

## Embedded implications
`longjmp()` can bypass layered error-handling paths in firmware. That may be attractive for parser recovery but dangerous for drivers and RTOS code where every layer owns resources.

On targets with separate CPU modes, privilege levels, stack pointers, floating-point state, or RTOS scheduler context, verify whether the implementation saves/restores everything required. A conforming C implementation can define the exact machine context in ways that differ across ABIs.

### Firmware review angle
Map every resource that may be live at the jump site:

```text
resource acquired -> possible longjmp -> who releases/restores it?
```

Pay particular attention to mutexes, interrupt masks, critical sections, clock changes, watchdog servicing, DMA descriptors, cache state, and transactional hardware state.

## Edge cases and failure modes
Common defects:
- `longjmp()` after the target function returned;
- jumping across a resource owner without cleanup;
- assuming local variables have their post-`setjmp` values;
- passing zero and accidentally selecting the same value as the initial return;
- jumping across an execution context that the RTOS/ABI does not permit;
- using a stale or overwritten `jmp_buf`;
- invoking non-local recovery from a signal handler without understanding the signal-specific rules.

A `longjmp()` can make static control-flow analysis harder because the transfer edge is not visible as a normal call/return relationship.

## Example pattern
```c
#include <setjmp.h>

static jmp_buf env;

static void fail(void)
{
    longjmp(env, 42);
}

static int operation(void)
{
    if (setjmp(env) == 0) {
        fail();
        return 0; /* Not reached after longjmp. */
    }
    return -1;
}
```

A production design should ensure that `operation()` owns all state that can be abandoned by this jump.

## Verification / debugging
Test recovery paths with faults injected at every resource-acquisition boundary. Static analysis should flag `longjmp()` sites for manual review. At the target level, inspect stack pointers and register state around the jump if diagnosing ABI/runtime problems.

Staff-level questions:
- What exactly is being abandoned?
- Which cleanup obligations are bypassed?
- Is the jump target guaranteed to be active?
- Can a normal error return or explicit state machine express the same recovery more safely?

## Staff-level takeaway
`longjmp()` is best viewed as **control-flow teleportation with no automatic cleanup**. Its correctness depends as much on resource ownership and lifetime reasoning as on the CPU context restoration itself.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
