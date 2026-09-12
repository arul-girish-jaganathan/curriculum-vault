# setjmp

> Canonical C topic note — chapter 34.

## Definition
`setjmp()` from `<setjmp.h>` establishes a non-local control-flow recovery point. It saves execution context into a `jmp_buf`; a later `longjmp()` can transfer control back to that point.

The critical rule is that `setjmp()` is not an ordinary function whose return value simply identifies success. It returns once when the context is initially established and appears to return again after `longjmp()`. The standard tightly restricts where the `setjmp()` invocation may appear.

## Mechanism and language rules
Typical control flow:

```text
setjmp(jb)
   │
   ├── initial return 0 ──> execute protected region
   │                         │
   │                         └── longjmp(jb, value)
   │                                  │
   └── resumed return ────────────────┘
                                      nonzero value
```

The saved environment represents enough implementation state to resume execution at the `setjmp` point. The exact contents of `jmp_buf` are opaque.

The invocation has strict syntactic restrictions. In portable C, `setjmp()` should be used directly in the controlling expression of an allowed `if`/`switch`, in a relational/equality comparison with an integer constant expression, or as the complete expression statement, as specified by the standard. Wrapping it in an arbitrary function call, assignment, arithmetic expression, or macro-generated expression can violate the rule.

### What to reason about
- `jmp_buf` is an opaque array type supplied by the implementation.
- The saved context can include control-flow and machine state; do not inspect or copy its representation manually.
- The context is valid only while the function invocation that established the environment is still active.
- `setjmp()` does not establish a C exception object, unwind C++ destructors, or automatically restore application resources.
- Automatic local variables changed after `setjmp()` may have indeterminate values after `longjmp()` unless they have `volatile`-qualified type, subject to the exact standard rule.
- The call site restriction exists because the implementation may need compiler cooperation to implement the unusual control-flow semantics.

## Embedded implications
On an MCU, `setjmp()` may save registers, stack/frame state, status information, and ABI-specific context. That can be expensive in code size and execution time, and `longjmp()` can bypass ordinary cleanup paths.

The mechanism may be useful for narrowly bounded recovery from a parser or transaction-like operation, but it is usually a poor fit for safety-critical firmware because resource ownership and control-flow reasoning become harder.

### Firmware review angle
Measure:
- context-save cost;
- stack consumption;
- interrupt/exception interactions;
- compiler optimization behavior;
- whether the RTOS scheduler state can be crossed safely;
- whether locks, DMA, peripherals, or power-state transitions are left active.

## Edge cases and failure modes
Major hazards:
- jumping into a function that has already returned;
- assuming all automatic variables retain their latest values;
- leaking locks, heap allocations, peripheral ownership, or transactions;
- crossing an RTOS task boundary;
- using a `jmp_buf` after its establishing function has returned;
- placing `setjmp()` in a forbidden expression context;
- assuming `longjmp()` performs structured cleanup.

A particularly dangerous pattern is using `longjmp()` as a universal error return mechanism across many stack frames. The resulting control-flow graph becomes non-local and resource ownership becomes difficult to prove.

## Example pattern
```c
#include <setjmp.h>

static jmp_buf recovery;

static void risky_operation(void)
{
    /* On a detected recoverable condition: */
    longjmp(recovery, 1);
}

int run(void)
{
    int status = setjmp(recovery);
    if (status == 0) {
        risky_operation();
        return 0;
    }

    /* Recovery path. */
    return -1;
}
```

The `jmp_buf` is deliberately owned by the active `run()` invocation.

## Verification / debugging
Compile with high warning levels and test at multiple optimization levels. Inspect the generated assembly when ABI behavior matters. Test every path for resource cleanup and use static analysis to identify non-local exits.

Staff-level questions:
- What resources are live when `longjmp()` occurs?
- Can every resource be safely abandoned or restored?
- Does the target ABI/RTOS permit this context transfer?
- Would explicit error propagation make the control flow easier to verify?

## Staff-level takeaway
`setjmp()` is a compiler-supported non-local control-flow primitive with real lifetime and optimization consequences. Use it only inside a tightly bounded recovery design where every bypassed cleanup and context boundary has been explicitly analyzed.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
