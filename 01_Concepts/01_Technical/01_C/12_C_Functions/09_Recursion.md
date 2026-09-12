# 09: Recursion

## Definition
Recursion is the programming technique where a function calls itself directly or indirectly through a chain of intermediate function invocations. In ISO C (C99 §6.5.2.2), every recursive invocation allocates a new, distinct set of automatic variables within a new call stack frame, maintaining isolated state across execution depths.

## Scope and Boundaries
*   **Covers:** Direct recursion, indirect (mutual) recursion, base cases, call stack consumption, tail recursion, and tail-call optimization (TCO).
*   **Does not cover:** Iterative control flow statements (`for`, `while`), or long jumps (`setjmp`/`longjmp`).

## Why Does It Exist
Certain mathematical algorithms and data structures are inherently recursive:
*   **Tree/Graph Traversal:** Navigating hierarchical structures (e.g., ASTs, file systems, JSON parsers).
*   **Divide-and-Conquer Algorithms:** Quicksort, mergesort, binary search, and mathematical induction computations.
*   **Grammar Parsing:** Recursive descent parsers for state machines and communication protocols.

## Mechanism and Language Rules
1.  **Stack Allocation:** Each invocation allocates its own stack frame containing local variables, parameters, and return addresses.
2.  **Base Case Requirement:** A recursive algorithm must contain at least one terminating condition (base case) that returns without making further recursive calls.
3.  **Tail Recursion:** A recursive call is a *tail call* if it is the absolute final operation executed before returning.
4.  **No Native Stack Safeguards:** ISO C provides no language-level mechanisms to detect or catch stack overflow. Exhausting stack memory results in undefined behavior.

## Examples

```c
/* Keep examples minimal: prove the rule before embedding it in a larger API. */
#include <stdint.h>

/* Correct: Tail-recursive implementation */
static uint32_t factorial_tail(uint32_t n, uint32_t acc)
{
    if (n <= 1U) {
        return acc; /* Base case */
    }
    return factorial_tail(n - 1U, acc * n); /* Tail call: optimizer can convert to loop */
}

/* Correct: Non-tail recursion with clear termination bound */
static uint32_t count_leading_zeros_rec(uint32_t val, uint32_t bit_pos)
{
    if ((val & (1UL << bit_pos)) != 0U || bit_pos == 0U) {
        return 31U - bit_pos;
    }
    return count_leading_zeros_rec(val, bit_pos - 1U);
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
*   **Undefined Behavior:** Unbounded recursion causing call stack overflow. Modifying memory beyond the allocated stack boundary corrupts adjacent RAM regions (e.g., `.data`, `.bss`, or heap).
*   **Implementation-Defined:** Maximum stack size and whether the compiler implements Tail Call Optimization (TCO) across optimization levels.

## Edge Cases and Failure Modes
*   **Missing Base Case:** A missing or faulty base case causes infinite recursion, instantly exhausting the stack and triggering a hard system crash.
*   **Debug vs. Release Inconsistencies:** In `-O2`, a tail-recursive function may be optimized into an iterative loop with $O(1)$ stack usage. In `-O0` (debug), TCO is disabled, creating an $O(N)$ stack frame chain that overflows the stack during debug testing.

## Embedded Implications
*   **Strict Prohibition in Safety-Critical Firmware:** In safety-critical embedded systems (automotive, aerospace, medical), recursion is strictly forbidden by standards like MISRA C and DO-178C. Embedded systems have fixed stack boundaries (often a few kilobytes) with no virtual memory to expand into.
*   **Silent Memory Corruption:** Microcontrollers without an MPU will silently overwrite global variables or heap structures when the stack expands past its limit, resulting in delayed, undebuggable hardware faults.

## Firmware Review Angle
1.  **Zero-Tolerance Policy:** Flag and reject any recursive function unless explicitly permitted by system architecture with proven, statically bounded depth.
2.  **Tail Call Reliance:** Never rely on the compiler performing Tail Call Optimization (TCO) for safety; rewrite recursive logic into explicit iterative loops (`while`, `for`).
3.  **Stack Margin Proofs:** If recursion is permitted, require static proof of maximum recursion depth and a physical stack budget analysis.

## Compiler, ABI, and Toolchain Implications
*   **Tail Call Elimination:** At `-O2/-O3`, modern compilers detect tail calls and emit unconditional branch instructions (`B` / `JMP`) instead of branch-with-link (`BL` / `CALL`), effectively transforming the recursive function into an iterative loop.
*   **Stack Canaries:** Compilers insert stack protector canaries (`-fstack-protector-all`) to detect stack boundary violations before function return.

## Performance, Memory, Timing, and Power
*   **Stack Consumption:** $O(N)$ stack memory allocation for non-tail recursion.
*   **Instruction Overhead:** Recursive call chains incur continuous prologue/epilogue instruction executions, consuming CPU cycles and degrading execution determinism.

## Verification / Debugging
*   **Static Stack Analysis:** Use `-fstack-usage` paired with call-graph tools (e.g., `avstack.pl`) to compute worst-case stack depth. (Recursive cycles break static stack analysis).
*   **MPU Stack Guard:** Configure the microcontroller's Memory Protection Unit (MPU) to place a No-Access guard page at the bottom of the stack to trap overflows immediately.

## Safety, Security, and Reliability
*   **MISRA C:2012 Compliance:**
    *   *Rule 17.2:* Functions shall not call themselves, either directly or indirectly.
*   **Security Vulnerabilities:**
    *   CWE-674: Uncontrolled Recursion. Attackers supply deep payloads (e.g., deeply nested JSON) to force stack exhaustion, causing Denial of Service (DoS) or remote code execution.

## Trade-offs and Alternatives
*   **Recursion vs. Iteration:**
    *   *Recursion:* Elegant, concise mathematical expression. Dangerous for embedded systems.
    *   *Iteration (Loops + Explicit Stack):* 100% deterministic, bounded memory usage, MISRA compliant, and robust against stack exhaustion.

## Staff-Level Takeaway
Recursion is an architectural hazard in embedded systems. Due to the lack of hardware stack expansion and strict determinism requirements, Staff engineers must ban recursion across production firmware, enforcing MISRA Rule 17.2. Any recursive algorithm must be refactored into an explicit iterative loop with a statically bounded memory footprint.

## Related Concepts
*   [[01_Function_definition]]
*   [[03_Parameter_passing]]
*   [[11_Calling_conventions]]
*   [[Stack Frame Architecture and ABI]]

---
*Related: [[00_Chapter_Index]], [[../00_Complete_Topic_Map]]*
