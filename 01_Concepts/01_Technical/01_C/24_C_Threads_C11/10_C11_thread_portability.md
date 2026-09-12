# 10: C11 Thread Portability

## Definition
C11 Thread Portability refers to the cross-platform applicability, runtime support, and interoperability constraints of `<threads.h>`. While C11 standardized multithreading into ISO C, implementation support varies significantly across POSIX operating systems, Microsoft Windows, embedded RTOSes, and compiler runtime libraries (glibc, musl, MSVC, newlib).

## Scope and Boundaries
- **Covers:** `<threads.h>` availability, `__STDC_NO_THREADS__` macro, POSIX mapping, Win32 mapping, and toolchain divergence.
- **Does not cover:** Platform-specific threading extensions (pthread attributes, processor affinity), or freestanding embedded details ([[11_Freestanding_limitations]]).

## Why Does It Exist
Before C11, writing multithreaded C code required fragmented `#ifdef _WIN32` and `#ifdef __unix__` wrappers. The C11 threading specification was designed to provide a uniform, standard abstraction layer. However, because threads were made an **optional** language feature, understanding portability boundaries is critical for production engineering.

## Mechanism and Language Rules
- **The Feature-Test Macro:** ISO C11 defines `__STDC_NO_THREADS__`. If the implementation defines this macro to integer constant `1`, `<threads.h>` is **not** provided by the compiler/runtime.
  ```c
  #if defined(__STDC_NO_THREADS__) && __STDC_NO_THREADS__ == 1
  #error "ISO C11 threads are not supported on this platform!"
  #endif
  ```
- **Historical Support Matrix:**
  - **Linux (glibc):** Supported natively since glibc 2.28 (2018).
  - **Linux (musl):** Supported natively since musl 1.1.18.
  - **FreeBSD / OpenBSD / NetBSD:** FreeBSD supports via native `libstdthreads` or base libc; others may require wrappers.
  - **Apple macOS / iOS:** Apple's Darwin libc famously **omits** `<threads.h>` even in modern macOS releases, defining `__STDC_NO_THREADS__`. Portable software must use wrapper libraries (like `c11threads` over pthreads) on macOS.
  - **Microsoft Windows (MSVC):** MSVC added native `<threads.h>` support in recent Visual Studio releases (VS 2019 / VS 2022 conforming to C11/C17).
  - **Embedded (newlib / picolibc):** Usually defines `__STDC_NO_THREADS__` unless explicitly ported onto FreeRTOS/Zephyr.

## Examples
```c
/* Portable abstraction header: threads_compat.h */
#ifndef THREADS_COMPAT_H
#define THREADS_COMPAT_H

#if !defined(__STDC_NO_THREADS__)
    /* Native ISO C11 Threads available */
    #include <threads.h>
#elif defined(__unix__) || defined(__APPLE__)
    /* Fallback: Map POSIX pthreads to C11 signatures */
    #include <pthread.h>
    #include <time.h>
    
    typedef pthread_t thrd_t;
    typedef pthread_mutex_t mtx_t;
    typedef pthread_cond_t cnd_t;
    typedef void (*thrd_start_t)(void *);

    enum { thrd_success = 0, thrd_error = 1, thrd_nomem = 2, thrd_busy = 3 };
    enum { mtx_plain = 0, mtx_recursive = 1 };

    static inline int thrd_create(thrd_t *thr, int (*func)(void *), void *arg) {
        return pthread_create(thr, NULL, (void *(*)(void *))func, arg) == 0 ? thrd_success : thrd_error;
    }
    static inline int thrd_join(thrd_t thr, int *res) {
        void *ret;
        if (pthread_join(thr, &ret) != 0) return thrd_error;
        if (res) *res = (int)(intptr_t)ret;
        return thrd_success;
    }
#elif defined(_WIN32)
    #include <windows.h>
    /* Win32 fallback implementation omitted for brevity */
#else
    #error "No threading support available for target platform."
#endif

#endif /* THREADS_COMPAT_H */
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- **Underlying Type Mapping:** ISO C does not specify whether `thrd_t` is a scalar integer, an opaque pointer, or a struct. Code assuming `thrd_t` can be cast to `int` or compared with `==` is non-portable (use `thrd_equal()`).
- **Clock Resolution Differences:** `thrd_sleep` and `cnd_timedwait` rely on `struct timespec`. System timer granularities vary between 100 microseconds (Linux) and 15 milliseconds (Windows default tick), affecting sleep precision.

## Edge Cases and Failure Modes
- **macOS Compilation Failure:** Attempting to `#include <threads.h>` in standard C code on macOS fails immediately because Apple refuses to ship `<threads.h>` in the Apple SDK, requiring third-party shims.
- **Type Signature Incompatibility:** POSIX thread routines return `void *`; C11 thread routines return `int`. Direct casting without wrappers violates function pointer calling conventions.
- **Thread Attributes Missing:** C11 does not specify how to configure thread stack size, CPU affinity, or scheduling policies (FIFO/Round Robin). Systems needing real-time prioritization must drop down to OS-specific APIs.

## Embedded Implications
- **RTOS Layering:** On embedded platforms running FreeRTOS, Zephyr, or ThreadX, `<threads.h>` is rarely provided natively. Embedded engineers typically build a lightweight C11 wrapper over native RTOS task queues and semaphores.

## Firmware Review Angle
- **Verify `__STDC_NO_THREADS__` Handling:** Ensure projects have a defined configuration fallback or build-time error for platforms without native C11 threading.
- **Enforce `thrd_equal()`:** Check code for invalid `thread1 == thread2` comparisons; require `thrd_equal(thread1, thread2)`.
- **Examine Real-Time Needs:** If a thread requires strict priority assignment, confirm whether C11 threads provide enough control or if native RTOS primitives are mandatory.

## Compiler, ABI, and Toolchain Implications
- **Linker Requirements:** On GCC/Clang under Linux, compiling C11 threads still requires passing `-pthread` to the linker to bind `libpthread` symbols.
- **ABI Stability:** Mixing objects compiled with different thread models (e.g., MSVC C11 threads vs Windows Win32 API directly) can cause ABI mismatch issues if thread handles are passed across DLL boundaries.

## Performance, Memory, Timing, and Power
- **Wrapper Overhead:** Thin inline shims (like the example above) compile down to direct underlying OS calls with zero runtime CPU overhead.
- **Feature Parity:** Underneath the hood, C11 threads map directly to the same kernel primitives as pthreads or Win32 threads.

## Verification / Debugging
- **CI Matrix Validation:** Test builds across Linux (glibc and musl), Windows (MSVC), and macOS to detect platform-specific header omissions early.
- **Static Assertions:** Validate alignment and sizes when mapping platform primitives:
  `_Static_assert(sizeof(thrd_t) <= sizeof(pthread_t), "Type size mismatch");`

## Safety, Security, and Reliability
- **Security Implications:** Platform divergences in thread stack guards (canaries) between Windows, Linux, and RTOSes mean stack overflow vulnerabilities behave differently across targets.
- **Standardized Semantics:** Using standard C11 abstractions isolates core application logic from OS API deprecations.

## Trade-offs and Alternatives
- **ISO C11 Threads vs. POSIX Threads (pthreads):**
  - *C11 Threads:* Standard, clean, portable across Windows and Linux without third-party libraries; lacks stack sizing, priority, affinity, and cancellation.
  - *Pthreads:* Rich feature set (priorities, barriers, read-write locks, cancellation, affinity); non-native on Windows, not part of ISO C standard.

## Staff-Level Takeaway
C11 threads provide an elegant, standardized API, but treating them as universally portable is a trap. Always check `__STDC_NO_THREADS__`. For cross-platform desktop and server software, maintain a battle-tested compatibility shim for macOS and legacy environments. For high-reliability embedded systems, use C11 threads for agnostic business logic, but keep hardware scheduling and stack allocations in the RTOS layer.

## Related Concepts
- [[00_Chapter_Index]]
- [[01_thrd_create]]
- [[11_Freestanding_limitations]]
- [[12_Thread_safe_module_design]]
