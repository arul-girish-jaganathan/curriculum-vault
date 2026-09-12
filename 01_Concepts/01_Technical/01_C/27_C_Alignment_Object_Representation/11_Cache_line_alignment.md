# 11: Cache Line Alignment

## Definition
Cache line alignment refers to aligning data structures and variables to the size of a processor CPU cache line (typically 64 bytes on modern x86_64 and ARM processors, or 32/128 bytes on specialized architectures). Aligning data to cache lines maximizes cache hit efficiency and prevents *false sharing* in multi-threaded concurrent applications.

## Scope and Boundaries
- **Covers:** CPU cache architecture, cache line sizes (64 bytes), false sharing, thread-local data separation, and performance optimization.
- **Does not cover:** DMA buffer alignment ([[10_DMA_alignment]]), fundamental ABI alignment ([[01_Alignment_requirements]]), or virtual memory paging.

## Why Does It Exist
Modern CPUs do not fetch individual bytes from RAM; they fetch memory in fixed-size blocks called cache lines:
- **False Sharing:** Occurs when two separate threads running on different CPU cores modify independent variables that happen to reside within the *same* 64-byte cache line. Even though the variables are logically independent, the hardware cache coherence protocol (MESI) bounces the entire cache line back and forth between core caches, causing severe performance degradation.
- **Cache Hit Optimization:** Aligning hot data structures to cache line boundaries ensures that object fetches load cleanly into single cache lines without spanning cross-line boundaries.

## Mechanism and Language Rules
- **Using `alignas` for Cache Lines:** Apply `alignas(64)` to shared counter arrays or concurrent work queues to ensure each thread's state occupies exclusive cache lines.
- **Padding to Cache Line Size:** Ensuring that structure sizes are integer multiples of the cache line size prevents adjacent allocations from sharing cache lines.

## Examples
```c
#include <stdio.h>
#include <stdalign.h>
#include <stdint.h>

#define CACHE_LINE_SIZE 64

/* Prevent false sharing by forcing each thread's counter onto its own cache line */
struct alignas(CACHE_LINE_SIZE) worker_metrics {
    uint64_t operations_completed;
    uint64_t errors_encountered;
    uint8_t  padding[CACHE_LINE_SIZE - 16]; /* Pad to exact cache line size */
};

int main(void) 
{
    struct worker_metrics worker1;
    struct worker_metrics worker2;

    printf("Worker 1 address: %p (diff: %zd)\n", (void *)&worker1, (char *)&worker2 - (char *)&worker1);
    printf("Worker 2 address: %p\n", (void *)&worker2);
    
    _Static_assert(sizeof(struct worker_metrics) == CACHE_LINE_SIZE, "Metrics size mismatch");

    return 0;
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- **Implementation-Defined:** Exact cache line sizes vary across CPU architectures (e.g., 64 bytes on most x86/ARM, 128 bytes on certain server chips). Hardcoding 64 bytes should be conditioned on target architecture profiles.

## Edge Cases and Failure Modes
- **Array Contiguity Assumption:** Allocating an array of cache-aligned structs (`struct worker_metrics workers[4];`) guarantees each element starts on a cache line, but if `sizeof(struct worker_metrics)` is not a multiple of the cache line size, subsequent elements can cross lines.

## Embedded Implications
- **Multi-Core MCUs:** Modern multi-core microcontrollers (e.g., dual-core ARM Cortex-R5, dual-core Cortex-M7 / ESP32 dual-core Xtensa) suffer from false sharing in shared global status flags if cache line alignment is ignored.

## Firmware Review Angle
- **Audit Multi-Threaded Globals:** Check multi-threaded and multi-core firmware architectures for shared status structures; apply `alignas(64)` to prevent cross-core cache invalidation storms.

## Compiler, ABI, and Toolchain Implications
- **Alignment Enforcement:** Compilers respect `alignas(64)` and emit appropriate instructions, but developers must ensure struct padding matches cache line boundaries explicitly.

## Performance, Memory, Timing, and Power
- **Throughput Boost:** Eliminating false sharing can improve multi-threaded concurrent throughput by several hundred percent in high-performance lock-free queues.

## Verification / Debugging
- **Performance Profiling:** Use hardware performance counters (Linux `perf c2c` - cache-to-cache) to detect false sharing hot spots in production binaries.

## Safety, Security, and Reliability
- **Determinism:** Prevents unpredictable multi-core execution stalls and latency jitter in real-time concurrent systems.

## Trade-offs and Alternatives
- **Memory Overhead:** Padding small variables to 64-byte cache lines wastes RAM space; use cache-line alignment strictly for highly contended multi-threaded variables and performance-critical shared queues.

## Staff-Level Takeaway
Cache line alignment is the secret weapon of high-performance concurrent systems engineering. In multi-core environments, hardware false sharing will quietly destroy concurrency scaling unless explicitly neutralized with `alignas(64)` cache line separation.

## Related Concepts
- [[00_Chapter_Index]]
- [[01_Alignment_requirements]]
- [[03_Alignas]]
- [[10_DMA_alignment]]
