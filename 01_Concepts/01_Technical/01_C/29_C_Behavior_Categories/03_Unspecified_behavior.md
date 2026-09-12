# 03: Unspecified Behavior

## Definition
Unspecified Behavior refers to aspects of program execution where the ISO C standard provides two or more valid choices and imposes no requirements on which choice is actually made, nor is the compiler required to document which choice it selected.

## Scope and Boundaries
- **Covers:** Function argument evaluation order, subexpression evaluation order, and struct padding content selection.
- **Does not cover:** Undefined behavior ([[04_Undefined_behavior]]) or implementation-defined behavior ([[02_Implementation_defined_behavior]]).

## Why Does It Exist
To give compiler writers absolute freedom to optimize code generation without being forced into arbitrary ordering constraints:
- **Evaluation Order Freedom:** Allowing the compiler to evaluate function arguments in whatever register allocation order is most efficient for the CPU architecture.

## Mechanism and Language Rules
- **Non-Determinism:** The outcome is valid either way, but the specific choice can vary between compiler versions, optimization levels, or even adjacent statement lines.
- **Side Effect Hazards:** If multiple arguments or subexpressions within the same statement modify the same variable without sequence points, unspecified behavior interacts with sequence rules, frequently crossing into undefined behavior.

## Examples
```c
#include <stdio.h>

int compute_a(void) {
    printf("A evaluated
");
    return 1;
}

int compute_b(void) {
    printf("B evaluated
");
    return 2;
}

void print_sum(int x, int y) {
    printf("Sum: %d
", x + y);
}

int main(void) 
{
    /* Argument evaluation order is UNSPECIFIED: 
       compute_a() might run before compute_b(), or vice versa! */
    print_sum(compute_a(), compute_b());
    return 0;
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- **Distinction:** Implementation-defined behavior *must* be documented by the vendor; unspecified behavior requires *no* documentation and can vary unpredictably.

## Edge Cases and Failure Modes
- **Function Argument Side Effects:** Writing `foo(x++, x++)` combines unspecified argument evaluation order with undefined behavior (modifying a scalar object more than once between sequence points).

## Embedded Implications
- **Driver Initialization Bugs:** Writing `init_uart(read_reg(A), read_reg(B))` where order of register reads matters leads to silent hardware initialization failures due to unspecified evaluation order.

## Firmware Review Angle
- **Enforce Single-Effect Statements:** Ban function calls with side-effect arguments. Evaluate expressions on separate lines to enforce deterministic execution ordering.

## Compiler, ABI, and Toolchain Implications
- **Register Allocation Freedom:** Optimizers exploit unspecified evaluation order to schedule instructions around pipeline stalls and register pressure.

## Performance, Memory, Timing, and Power
- **Optimizer Latitude:** Permitting unspecified evaluation order enables compilers to generate faster, more compact instruction sequences.

## Verification / Debugging
- **Compiler Warnings:** Enable `-Wsequence-point` to catch overlapping side effects that trigger undefined behavior within unspecified evaluation contexts.

## Safety, Security, and Reliability
- **Defensive Design:** Eliminating reliance on evaluation order guarantees deterministic, repeatable execution across compiler builds.

## Trade-offs and Alternatives
- **Conciseness vs. Determinism:** Splitting complex expressions across multiple lines sacrifices conciseness but guarantees 100% deterministic execution ordering.

## Staff-Level Takeaway
Unspecified behavior means "the standard doesn't care, and neither should your code." Never write code whose correctness depends on the evaluation order of function arguments or subexpressions.

## Related Concepts
- [[00_Chapter_Index]]
- [[01_Defined_behavior]]
- [[02_Implementation_defined_behavior]]
- [[04_Undefined_behavior]]
