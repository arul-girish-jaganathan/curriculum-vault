# 60.08 Constraint propagation

## Core idea

**Constraint propagation** is a concrete subtopic of **Backtracking**. This note is its canonical home. Other notes should link here rather than repeating its explanation.

DSA reasoning starts with the operation contract, invariant, complexity target and implementation constraints.

## Canonical pattern

```text
choose -> recurse -> undo
prune as soon as the partial state cannot lead to a valid answer
```

## Mechanism

The reliable way to learn this topic is to define the state first, then the operation that changes the state, then the invariant that must remain true after each operation.

For **Constraint propagation**, identify:
- the input representation;
- the maintained state;
- the legal operation sequence;
- the invariant after each operation;
- the answer or output definition;
- the stopping condition.

## Complexity

Always record:
- time complexity;
- auxiliary space;
- recursion/stack depth if applicable;
- preprocessing cost;
- cost per query/update when operations repeat.

Do not stop at Big-O when input constraints are small enough that constant factors, cache locality or allocation cost decide the real implementation.

## Boundary cases

Check:
- empty input;
- one element;
- duplicate values;
- already sorted/adversarial order;
- minimum and maximum values;
- disconnected or unreachable states where the topic allows them;
- overflow-sensitive arithmetic;
- repeated updates or queries;
- degenerate structure height.

## Failure modes

The most common DSA implementation failures are:
- wrong invariant;
- off-by-one boundary;
- state updated before it is consumed;
- stale heap/queue entry;
- duplicate suppression performed at the wrong layer;
- recursion stack exhaustion;
- integer overflow;
- incorrect complexity caused by hidden copying or repeated scans.

A correct algorithm implemented with the wrong invariant is still incorrect.

## Worked reasoning

Use this sequence:

```text
1. Define the state.
2. Define the invariant.
3. Perform one operation manually.
4. Check the invariant.
5. Repeat until the termination condition.
6. Prove the returned state represents the required answer.
```

For optimization problems, also identify what makes a local decision safe, or why a DP state contains enough information to represent all future choices.

## Implementation notes

Prefer explicit names for:
- indices and ranges;
- graph vertices and edges;
- subtree/state identifiers;
- capacities and counts;
- distance/answer arrays.

Separate algorithmic logic from I/O and test harness code so the invariant is visible.

## Testing

Use at least:
1. a tiny hand-solvable example;
2. an edge case;
3. a random case checked against a slower reference;
4. a stress case near the stated constraints.

For graph and tree algorithms, generate structural edge cases such as isolated vertices, chains, stars, repeated edges and disconnected components when relevant.

## Debugging

When the result is wrong, inspect the **first state that violates the invariant**.

Useful checks:
- print or assert state after each iteration for tiny inputs;
- compare against a brute-force reference;
- log parent/visited/distance arrays;
- validate heap ordering assumptions;
- verify that every update decreases the remaining search space or progresses an index.

## Optimization

Optimize only after identifying the bottleneck.

Possible transformations include:
- replace repeated scans with hashing;
- replace nested range work with prefix structures;
- sort once and use binary search/two pointers;
- replace recursion with iterative state when stack depth matters;
- compress coordinates when values are sparse;
- use cache-friendly contiguous storage when access is sequential.

## Proof sketch

A complete explanation should contain three parts:

**Initialization:** the invariant is true before the first operation.

**Maintenance:** one iteration/transition preserves the invariant.

**Termination:** when the algorithm stops, the invariant plus the stopping condition implies the required answer.

For greedy algorithms, add the exchange or cut argument that proves the choice is safe. For DP, explain optimal substructure. For graph algorithms, state why the traversal order or relaxation rule establishes the claimed distance/component property.

## Embedded and systems perspective

For firmware and systems code, also ask:
- Is the memory footprint bounded?
- Does the algorithm allocate?
- Is worst-case execution acceptable?
- Does data layout fit the cache?
- Can the algorithm run with limited stack?
- Are integer widths large enough?
- Can input corruption violate an assumed invariant?

A theoretically optimal algorithm can still be a poor embedded choice if it has unpredictable memory behavior.

## Staff-level review

1. What constraint drove the algorithm choice?
2. What is the simplest correct baseline?
3. Which invariant makes the optimized solution correct?
4. What is the exact worst-case complexity?
5. What memory is required at peak?
6. Which input distribution makes the algorithm perform poorly?
7. What alternatives were rejected and why?
8. How is correctness verified independently of the implementation?
9. How does the choice change when scale or hardware changes?

## Related

- [[../02_Complexity_Analysis/00_Chapter_Index|Complexity Analysis]]
- [[../06_Arrays_Fundamentals/00_Chapter_Index|Arrays]]
- [[../23_Hashing_Fundamentals/00_Chapter_Index|Hashing]]
- [[../43_Graph_Representations/00_Chapter_Index|Graphs]]
- [[../64_Dynamic_Programming_Fundamentals/00_Chapter_Index|Dynamic Programming]]
- [[../90_Staff_DSA/00_Chapter_Index|Staff-Level DSA]]

## Source backbone

This note is organized from the GeeksforGeeks DSA Tutorial, which currently covers fundamentals, complexity analysis, arrays, hashing, strings, linked lists, stacks, queues, trees, heaps, graphs, searching, sorting, two pointers, sliding window, prefix sum, recursion, greedy algorithms, dynamic programming, trie, segment tree, red-black tree, binary indexed tree, bitwise algorithms, backtracking, divide and conquer, branch and bound, geometry and randomized algorithms. citeturn391309search1turn391309search5turn391309search2

Primary: https://www.geeksforgeeks.org/dsa/introduction-to-dsa/
Roadmap: https://www.geeksforgeeks.org/dsa/complete-roadmap-to-learn-dsa-from-scratch/
