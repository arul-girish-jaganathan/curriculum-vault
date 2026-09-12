# stdio streams

## Definition
The `<stdio.h>` stream model provides C's standard buffered character I/O abstraction through `FILE *` objects. A stream connects a C program to an external file or device and maintains state such as buffering, position, orientation, and error/end-of-file indicators. Standard streams include `stdin`, `stdout`, and `stderr` in hosted environments. The C standard defines the stream interface and semantics, while the actual device, filesystem, terminal, buffering policy, and OS integration are implementation/platform concerns.

## Scope and Boundaries
* **Covers:** `FILE`, standard streams, character/block stream operations, stream state, text versus binary streams, buffering, EOF/error handling, and stream lifetime.
* **Does not cover:** the full formatted conversion language, filesystem-specific system calls, POSIX file descriptors, or C++ iostreams.

## Why Does It Exist
C needs a portable abstraction for sequential external I/O without requiring every program to understand a particular OS, device driver, or filesystem. `FILE *` lets the same application-level API target files, terminals, pipes, memory-backed implementations, or firmware-specific devices when the platform supplies the necessary layer.

## Mechanism and language rules
A `FILE *` is an opaque handle managed by the C library. Applications should not inspect or construct the object themselves. Typical interfaces include `fgetc`, `fputc`, `fread`, `fwrite`, `fgets`, `fputs`, `fflush`, `fseek`, `ftell`, `feof`, `ferror`, `clearerr`, and `fclose`.

A successful read returns data; end-of-file and I/O failure are represented through return values and stream status rather than by assuming that a particular byte value means EOF. Functions such as `fgetc` return `int` specifically so every `unsigned char` value plus the distinct `EOF` value can be represented.

### What to reason about
- A `FILE *` is not a raw file descriptor and must be used only with the operations defined for streams.
- Stream state includes buffering and EOF/error indicators; consuming input can change that state even when the application-visible payload appears unchanged.
- Text and binary streams can have different translation semantics on hosted implementations.
- Mixing input and output on an update stream requires the sequencing rules required by the relevant operation; do not assume arbitrary alternation is valid.
- Concurrent access to the same stream requires a documented synchronization model; the C language does not make an arbitrary shared `FILE *` design automatically race-free.
- `EOF` is a status value, not a character stored in the input stream.

## Embedded implications
Many bare-metal systems are freestanding and do not provide a complete hosted `<stdio.h>` environment. Where supplied, stdio may be retargeted to UART, USB CDC, semihosting, RTT, a filesystem, or a debugger console. This can add substantial flash/RAM cost and unpredictable latency.

`printf`-style logging may block while a UART drains, allocate internal buffers, acquire locks, or trigger device-driver activity. Calling stdio from an ISR is therefore generally inappropriate unless the platform explicitly documents an ISR-safe implementation.

### Firmware review angle
Determine what `FILE *` maps to on the target, whether the implementation is thread-safe, where buffers live, how large they are, and what happens when the physical transport stalls. Compare debug and production builds because logging retarget layers often change timing and memory usage dramatically.

## Edge cases and failure modes
- Testing `if (c == EOF)` is valid only when `c` can represent the full `unsigned char` range plus `EOF`; storing `fgetc()` directly into `char` can lose the distinction.
- `feof(stream)` does not predict that the next read will reach EOF; it reports that an EOF condition has already occurred.
- `ferror(stream)` is separate from EOF and must be checked when I/O failure matters.
- Ignoring `fclose()` failure can lose buffered output or conceal storage errors.
- Assuming `stdout` is immediately visible is incorrect when output is buffered.
- Using an invalid, closed, or otherwise stale `FILE *` violates the API contract and can lead to undefined behavior.

## Example pattern
```c
#include <stdio.h>

static int read_byte(FILE *stream, unsigned char *out)
{
    int c;

    if (stream == NULL || out == NULL) {
        return -1;
    }

    c = fgetc(stream);
    if (c == EOF) {
        return ferror(stream) ? -2 : 1; /* I/O error vs EOF */
    }

    *out = (unsigned char)c;
    return 0;
}
```

## Verification / debugging
On a hosted target, unit-test EOF, error, buffering, and close paths with controlled streams/files. On embedded targets, instrument the retarget layer and measure worst-case latency rather than assuming a `printf` call is cheap. Inspect the map file for libc pulls and test both normal and disconnected/stalled transports.

Useful review questions: What device owns this stream? Can it block? Where is buffering performed? What happens on power loss or transport failure? Is the API allowed in an ISR or high-priority task?

## Staff-level takeaway
Treat stdio as an abstraction boundary, not as a harmless convenience. A Staff engineer should identify the concrete implementation behind `FILE *`, its buffering and synchronization behavior, failure contract, and real-time cost. In embedded firmware, a small explicit driver interface is often preferable when deterministic latency and minimal footprint matter.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
