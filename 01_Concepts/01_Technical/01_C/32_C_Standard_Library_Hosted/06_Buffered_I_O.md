# Buffered I/O

## Definition
Buffered I/O allows the C standard library to accumulate input or output in memory so that application operations do not necessarily map one-for-one to external device operations. Stream buffering is controlled through `setbuf`, `setvbuf`, and implementation defaults; `fflush` requests output-buffer flushing. Common buffering modes are unbuffered, fully buffered, and line buffered.

## Scope and Boundaries
* **Covers:** stream buffers, buffering modes, `setvbuf`, `setbuf`, `fflush`, line buffering, and interaction with stream visibility and latency.
* **Does not cover:** filesystem cache coherency or OS kernel buffering unless needed to explain why `fflush` is not a durability guarantee.

## Why Does It Exist
External I/O can be much slower than memory operations. Buffering reduces the number of expensive device operations, improves throughput, and permits libraries to provide efficient character and block interfaces without forcing every application call to understand the physical transport.

## Mechanism and language rules
A stream can have an internal buffer whose lifetime and implementation details are managed by the C library. `setvbuf` can request a buffering mode and optionally provide a buffer, but it must be called at the correct point in the stream lifetime—before I/O has been performed on the stream, subject to the standard's requirements.

Line buffering generally attempts to transmit output when a newline is encountered, but its interaction with terminals and other streams is implementation-dependent. `fflush` on an output or update stream causes buffered output to be written to the associated external file as specified by the implementation; it does not establish a universal power-fail or physical-media durability guarantee.

### What to reason about
- Buffer size affects RAM footprint, throughput, and latency.
- A supplied buffer passed to `setvbuf` must remain valid for as long as the stream uses it.
- Do not use or modify a caller-provided stream buffer while the stream owns it.
- Input buffering means the library may have already fetched bytes from the underlying device even though the application has consumed only some of them.
- `fflush(stdin)` is not a portable way to discard pending input; the defined operation is primarily about output/update streams.
- Closing an output stream performs the final flush, but the close can still fail.

## Embedded implications
On embedded targets, buffering can be a deliberate performance/timing trade-off. A large UART/USB output buffer consumes RAM but reduces per-byte driver overhead. A small buffer saves RAM but may increase interrupt frequency and transport transactions.

### Firmware review angle
Choose buffering explicitly for real-time paths. Determine whether buffers live in DMA-capable memory, whether cache maintenance is needed, and whether the stream implementation uses locks. If a stream is retargeted to a UART, understand whether `fflush` waits for the UART hardware to finish or merely hands bytes to a driver buffer.

## Edge cases and failure modes
- Assuming a newline always makes output physically visible is not portable.
- Assuming `fflush` makes data survive power loss confuses libc buffering with storage durability.
- Supplying a stack buffer to `setvbuf` and returning from the function creates a lifetime violation.
- Changing or freeing a buffer while it is still owned by the stream can corrupt I/O state.
- Buffering can hide failures until a later flush or close, so error handling must include those operations.

## Example pattern
```c
#include <stdio.h>

static unsigned char io_buffer[256];

static int configure_output(FILE *stream)
{
    if (stream == NULL) {
        return -1;
    }

    return setvbuf(stream, (char *)io_buffer, _IOFBF, sizeof io_buffer);
}
```

The static storage duration of `io_buffer` makes its lifetime suitable for a stream that may retain it beyond the function call. The stream must be configured before ordinary I/O begins.

## Verification / debugging
Measure both throughput and worst-case latency with different buffer sizes. Verify output visibility at newline, explicit flush, and close boundaries. On embedded targets, inspect RAM usage and trace driver calls to determine whether `fflush` actually drains the physical transport or only an intermediate layer.

## Staff-level takeaway
Buffering is a performance optimization that changes timing and failure boundaries. A Staff engineer should treat buffer ownership, lifetime, size, flushing semantics, and transport durability as explicit design decisions—not hidden libc behavior.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
[[01_stdio_streams]]
[[05_fopen_fclose]]
