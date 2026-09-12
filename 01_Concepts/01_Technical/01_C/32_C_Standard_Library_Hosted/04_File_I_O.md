# File I/O

## Definition
C file I/O is the portable stream-based interface in `<stdio.h>` for opening, reading, writing, positioning, and closing external files. It is centered on `FILE *` and functions such as `fopen`, `fclose`, `fread`, `fwrite`, `fgetc`, `fputc`, `fgets`, `fputs`, `fseek`, `ftell`, `rewind`, `fflush`, `remove`, and `rename`. The C standard defines the abstract stream behavior; pathname syntax, permissions, filesystem semantics, device nodes, atomicity, and durability are platform-specific.

## Scope and Boundaries
* **Covers:** sequential and random stream I/O, binary versus text mode, positioning, short reads/writes, EOF/error state, and file-operation contracts.
* **Does not cover:** OS-specific system calls such as POSIX `open/read/write`, filesystem driver internals, or persistent-storage wear algorithms.

## Why Does It Exist
The stream API allows portable applications to manipulate external storage without coupling application code to a particular operating system or filesystem. It also provides a buffering layer that can reduce expensive external I/O operations.

## Mechanism and language rules
`fopen` creates or associates a stream with an external file and returns a `FILE *` or `NULL` on failure. Mode strings determine whether the stream is read, write, append, or update oriented and whether text/binary behavior applies. `fread` and `fwrite` transfer a specified number of objects, returning the number actually transferred rather than simply a Boolean success value.

Positioning functions operate on the stream's file position indicator. `fseek` and `ftell` have constraints based on the stream and mode; arbitrary byte offsets should not be assumed portable for text streams. Binary streams are the appropriate abstraction when exact byte representations and positions matter.

### What to reason about
- A successful `fread(ptr, size, count, stream)` can return less than `count`; inspect `feof` and `ferror` to determine why.
- A successful `fwrite` can also perform a short transfer; treating the return value as automatically equal to `count` is unsafe.
- `fflush` concerns output buffers; it is not a universal filesystem durability primitive.
- Text streams may translate characters or have implementation-defined positioning behavior.
- `fseek`/`ftell` are not a portable replacement for a filesystem-specific 64-bit file-offset API when files may exceed the implementation's range.
- File position, EOF/error indicators, buffering, and external storage state are separate concepts.

## Embedded implications
On embedded targets, file I/O may mean an SD card, NOR/NAND flash filesystem, USB mass storage, or a vendor virtual filesystem. Latency can vary by orders of magnitude, and writes can trigger erase/program operations, garbage collection, wear leveling, or power-loss windows.

### Firmware review angle
Never infer real-time behavior from the simple-looking `fwrite` call. Establish the worst-case latency, RAM buffering, stack usage, filesystem locking, reentrancy model, and failure behavior when media is removed or full. For safety-critical persistence, define what “written” means: copied into a libc buffer, handed to a driver, committed to media, or made power-fail safe.

## Edge cases and failure modes
- Reading into an undersized destination with `fread` causes memory corruption.
- A partial read is not necessarily an error; it may simply indicate EOF.
- `feof()` becomes true only after an operation encounters end-of-file.
- Using `fseek` on a stream where the requested operation is not supported can fail; always check the return value.
- Writing a C struct directly to a file can bake in padding, alignment, endianness, ABI layout, and version assumptions.
- Assuming `fflush` makes flash storage power-loss safe is a platform-specific and often incorrect assumption.

## Example pattern
```c
#include <stdio.h>

static int copy_bytes(FILE *in, FILE *out)
{
    unsigned char buf[128];
    size_t n;

    do {
        n = fread(buf, 1, sizeof buf, in);
        if (n != 0 && fwrite(buf, 1, n, out) != n) {
            return -1;
        }
    } while (n != 0);

    return ferror(in) ? -2 : 0;
}
```

## Verification / debugging
Test empty files, partial reads, full media, permission failures, removed media, interrupted writes, and large files. Use fault injection in the storage layer where possible. On embedded systems, correlate application events with filesystem-driver traces and measure worst-case write latency under fragmented/full-media conditions.

Review the linker map when enabling file I/O because filesystem and stdio support can pull in substantial code and buffers.

## Staff-level takeaway
File I/O is an abstraction over a potentially complex and failure-prone storage stack. A Staff engineer must separate C stream semantics from filesystem and durability guarantees, define exact persistence requirements, and prevent blocking storage operations from leaking into real-time control paths.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
[[28_C_Endianness_Serialization/00_Chapter_Index]]
