# 10: Atomic Pointers

## Definition
An atomic pointer (`_Atomic(T*)` or `atomic_uintptr_t`) is a pointer whose address value can be read, written, and swapped atomically. It provides the mechanism for safely publishing dynamic memory blocks, exchanging buffer ownership, and constructing lock-free linked lists, queues, and hazard pointer systems.

## Scope and Boundaries
Covers: Atomic pointer declaration, address swapping, publishing patterns, memory reclamation hazards, and the ABA problem.
Does not cover: Atomic access to the data *pointed to* by the pointer.

## Why Does It Exist
Multi-threaded and real-time systems frequently pass buffers between threads (e.g., passing a completed network frame buffer to an application parser). Swapping a pointer atomically transfers ownership in $O(1)$ time with zero memory copying.

## Mechanism and Language Rules
1. **Pointer Atomicity:** The pointer variable itself is atomic; the object it points to is standard, non-atomic memory.
2. **Pointer Arithmetic:** C11 supports atomic pointer arithmetic (`atomic_fetch_add` on pointers advances by `sizeof(*ptr)` bytes).
3. **Publishing Contract:** Setting an atomic pointer with `memory_order_release` ensures that all data written into the pointed-to buffer is visible to any thread that reads the pointer with `memory_order_acquire`.

## Examples
```c
#include <stdatomic.h>
#include <stdint.h>
#include <stddef.h>

typedef struct {
    uint32_t sample_id;
    float    voltage;
} SensorData_t;

/* Double-buffering architecture using atomic pointers */
static SensorData_t s_buffer_a;
static SensorData_t s_buffer_b;

static _Atomic(SensorData_t *) g_active_buffer = &s_buffer_a;

/* Producer (ISR or Sensor Task) */
void sensor_publish_new_sample(uint32_t id, float volt) {
    /* 1. Identify inactive scratch buffer */
    SensorData_t *scratch = (atomic_load_explicit(&g_active_buffer, memory_order_relaxed) == &s_buffer_a) 
                            ? &s_buffer_b : &s_buffer_a;

    /* 2. Populate non-atomic buffer */
    scratch->sample_id = id;
    scratch->voltage = volt;

    /* 3. Atomically publish pointer with release ordering */
    atomic_store_explicit(&g_active_buffer, scratch, memory_order_release);
}

/* Consumer (Display / Telemetry Task) */
SensorData_t sensor_read_latest(void) {
    /* Acquire load guarantees we read fully initialized sample fields */
    SensorData_t *buf = atomic_load_explicit(&g_active_buffer, memory_order_acquire);
    return *buf; /* Value copy of snapshot */
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- Dereferencing an atomic pointer that was loaded with `memory_order_relaxed` while another thread is mutating the underlying buffer invokes Undefined Behavior (Data Race).

## Edge Cases and Failure Modes
- **The ABA Problem in Lock-Free Stacks:** If a node pointer is popped ($A$), freed, and re-allocated at the exact same memory address ($A$) while another thread is executing a CAS loop, the CAS succeeds incorrectly, corrupting the list. Mitigate using tagged pointers (embedding a version counter in pointer high bits) or epoch-based reclamation.
- **Memory Leakage:** Atomically swapping a pointer without retaining a reference to the old pointer leaks the underlying buffer.

## Embedded Implications
- **Zero-Copy DMA Buffer Flipping:** Atomic pointer swapping allows high-speed ADC or Ethernet DMA routines to flip ping-pong buffers instantaneously without stopping hardware DMA transfers.

## Firmware Review Angle
- Confirm that the atomic pointer update uses `memory_order_release` to publish the underlying struct fields.
- Verify that consuming threads read the pointer with `memory_order_acquire` before accessing buffer contents.

## Compiler, ABI, and Toolchain Implications
- On 32-bit MCUs, atomic pointers are 32-bit words; on 64-bit platforms, they are 64-bit words. Compilers map them to native pointer register operations.

## Performance, Memory, Timing, and Power
- Swapping a pointer takes single-digit nanoseconds, enabling microsecond-level telemetry processing.

## Verification / Debugging
- Sanitizers (ASan + TSan) detect memory leaks and data races on pointer dereferences.

## Safety, Security, and Reliability
- Eliminates deep buffer copying, reducing CPU utilization and instruction cache thrashing.

## Trade-offs and Alternatives
- **Atomic Pointer Swap vs Mutex Copy:** Swapping pointers is 100x faster than copying large structures under a mutex lock, but requires careful buffer lifetime management.

## Staff-Level Takeaway
Atomic pointers are the foundation of zero-copy concurrent data exchange. Always publish pointers using `memory_order_release` and consume them using `memory_order_acquire` to ensure that data written into the buffer is fully visible before the pointer address is resolved.

## Related Concepts
- `04_compare_exchange`
- `06_acquire_release`
- `../18_C_Typedef/05_Pointer_typedefs`
