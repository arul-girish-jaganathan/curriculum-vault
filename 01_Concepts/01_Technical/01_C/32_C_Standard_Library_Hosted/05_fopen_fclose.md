# fopen/fclose

## Definition
`fopen` and `fclose` establish and terminate a C standard I/O stream. `fopen` takes a pathname and mode string and returns a `FILE *` on success or `NULL` on failure. `fclose` flushes pending output and releases the stream resources, returning zero on success and `EOF` on failure. The C interface is portable; pathname syntax, permissions, device mapping, and filesystem behavior are implementation-specific.

## Scope and Boundaries
* **Covers:** `fopen`, `fclose`, mode strings, update streams, append semantics, failure handling, and ownership/lifetime of `FILE *`.
* **Does not cover:** OS-specific file descriptors or filesystem internals.

## Why Does It Exist
These functions provide a standardized lifetime boundary for file streams. `fopen` establishes the library-managed stream state and `fclose` provides the corresponding cleanup and output-flush operation.

## Mechanism and language rules
Common modes include `r`, `w`, `a`, and update forms such as `r+`, `w+`, and `a+`; `b` requests binary mode where the implementation distinguishes it from text mode. `w` can truncate an existing file, while `a` writes at the end according to the stream's append semantics. The optional implementation-defined mode characters must not be assumed portable.

The returned pointer owns a stream resource. Once `fclose` succeeds, the `FILE *` must no longer be used. All operations that depend on it must finish before closing it.

### What to reason about
- `fopen` failure must be handled before dereferencing or passing the returned pointer to stream operations.
- `w` can destroy existing contents; use it only when truncation is intentional.
- Update streams have sequencing requirements when switching between reading and writing.
- `fclose` can fail because final buffered output cannot be committed; ignoring its return value can hide data loss.
- A process can exhaust its implementation's limit on simultaneously open streams even when RAM appears available.
- `fclose(NULL)` is not a portable way to perform conditional cleanup; test the pointer first.

## Embedded implications
An embedded implementation may map `fopen` to flash filesystems, SD cards, USB storage, or a vendor virtual filesystem. Opening a file can allocate buffers, acquire locks, scan metadata, and perform storage transactions. Closing may perform the most important write because buffered data is flushed at that point.

### Firmware review angle
Document who owns every `FILE *`, who closes it on every failure path, and whether close latency is acceptable. Avoid opening/closing repeatedly in a high-rate loop when the filesystem has expensive metadata or erase operations. For persistent configuration, use a purpose-built transactional storage layer when power-loss consistency matters.

## Edge cases and failure modes
- `fopen("config.bin", "w")` can truncate a valid configuration before the new data has been safely written.
- Returning early after `fopen` without `fclose` leaks a stream resource.
- Double-closing a stream or using it after close violates its lifetime contract.
- A successful `fwrite` followed by a failed `fclose` means the application cannot necessarily claim durable output.
- `a+` read/write positioning behavior is subtle; do not assume that every read/write leaves the position where an OS-level file descriptor would.
- Mode strings are not permission specifications in the POSIX sense; platform-specific access-control behavior is outside ISO C.

## Example pattern
```c
#include <stdio.h>

static int write_record(const char *path)
{
    FILE *f = fopen(path, "wb");
    if (f == NULL) {
        return -1;
    }

    if (fputs("record\n", f) == EOF) {
        (void)fclose(f);
        return -2;
    }

    return (fclose(f) == 0) ? 0 : -3;
}
```

## Verification / debugging
Test every `fopen` mode with existing, missing, read-only, full, and corrupted media. Inject failures during both write and close. Use static analysis to verify resource ownership and error-path closure. On embedded systems, measure open/close latency and inspect filesystem traces to see when actual flash programming occurs.

## Staff-level takeaway
`fopen`/`fclose` are resource-lifetime APIs, not just convenience calls. The Staff-level concern is ownership, failure atomicity, latency, and persistence semantics. If closing a stream can lose data or block a control path, the storage abstraction needs an explicit contract rather than casual stdio usage.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
[[04_File_I_O]]
