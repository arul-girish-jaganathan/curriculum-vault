# Hosted-only assumptions

## Definition
A hosted C implementation provides the complete execution environment described by the hosted requirements of the C standard, including the required program startup model and standard library facilities. A freestanding implementation targets environments where those hosted assumptions do not hold. Hosted-only assumptions in application code include the existence of files, terminals, processes, environment variables, command execution, normal program termination, and the full hosted standard library.

## Scope and Boundaries
* **Covers:** hosted versus freestanding execution, `main`, standard streams, files, environment/process assumptions, and portability boundaries.
* **Does not cover:** a complete conformance analysis or OS-specific APIs.

## Why Does It Exist
C was designed to span both general-purpose systems and constrained embedded environments. The hosted/freestanding distinction lets the language remain useful where there is no operating system, filesystem, process model, or conventional application startup.

## Mechanism and language rules
Hosted programs have an implementation-defined startup environment consistent with the standard's requirements and a `main` entry point. The hosted library includes facilities such as I/O, memory allocation, time, environment access, and other services. A freestanding implementation has a smaller required library and does not promise the same execution environment.

This distinction is not identical to “desktop versus embedded”: an embedded RTOS system may provide many hosted-like facilities, while a small bare-metal MCU may provide only the subset needed by its firmware and toolchain.

### What to reason about
- A header existing in the compiler installation does not prove that every interface has the same semantics or quality on the target.
- C language conformance and libc completeness are separate dimensions.
- Startup code, linker script, runtime initialization, and `main` handling may be supplied by the toolchain rather than by the application.
- Calling a hosted-only facility in portable freestanding code requires an explicit target contract or abstraction.
- Compiler builtins and extensions can provide functions that look like standard interfaces but have target-specific behavior.

## Embedded implications
Typical embedded systems replace hosted facilities with board support, drivers, RTOS services, or application-specific abstractions. For example, `stdout` may map to UART, `malloc` may be prohibited, and `exit` may become a reset or safe-state transition.

### Firmware review angle
Create a target capability matrix identifying which standard headers/functions are available, thread-safe, ISR-safe, deterministic, and acceptable under the project's coding standard. Verify both the compiler and the linked C library rather than assuming the language standard alone answers the question.

## Edge cases and failure modes
- Code that compiles on a Linux host because `stdio`, filesystem, and process services exist may fail to link on a freestanding MCU.
- A stubbed implementation can compile successfully but have semantics unsuitable for production, such as `exit` never returning to a host because there is no host process.
- Test harnesses can accidentally make firmware appear hosted by supplying services unavailable on the actual target.
- Conditional compilation can hide API differences until a rarely built target is selected.
- Relying on POSIX behavior when the interface is only guaranteed by ISO C creates portability defects.

## Example pattern
```c
/* Keep application logic independent of the hosted environment. */
typedef struct {
    int (*write)(const void *data, unsigned long size);
} output_port_t;

static int emit_status(const output_port_t *port)
{
    static const char text[] = "OK\n";
    return (port != NULL && port->write != NULL)
         ? port->write(text, sizeof text - 1U)
         : -1;
}
```

The application depends on a narrow capability rather than assuming that `stdout` exists everywhere.

## Verification / debugging
Build every supported target in CI. Inspect compiler predefined macros and libc configuration, link maps, and startup objects. Maintain a conformance/capability test suite that exercises the standard interfaces actually used by the product.

## Staff-level takeaway
“Standard C” does not mean “every C library feature exists identically on every target.” A Staff engineer should define the hosted/freestanding boundary explicitly, isolate platform services behind narrow interfaces, and verify availability and semantics on each supported compiler/libc/MCU combination.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
[[54_C_Freestanding_Hosted_Conformance/00_Chapter_Index]]
