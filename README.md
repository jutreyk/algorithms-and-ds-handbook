# algorithms-and-ds-handbook

A comprehensive, production-tested reference library of foundational and competitive algorithms, data structures, and computational geometry written in Python 3.10+. Designed to showcase deep algorithmic rigor, asymptotic optimality, and clean mathematical implementations.

## Algorithmic Coverage

### 1. Sorting Algorithms
- **QuickSort**: 3-Way Dutch National Flag partitioning handling duplicate elements in $O(N)$ expected time.
- **MergeSort**: Stable divide-and-conquer implementation with $O(N \log N)$ worst-case guarantee.
- **HeapSort**: Priority queue-backed sorting utilizing binary min-heaps.
- **RadixSort (LSD)**: Non-comparative integer sorting executing in $O(d \cdot (N + b))$.
- **TimSort**: Adaptive hybrid combining insertion sort on mini-runs ($k=32$) and merge sweeps.

### 2. Graph Theory & Shortest Paths
- **BFS & DFS**: Linear traversal, connectivity analysis, and cycle detection.
- **Dijkstra's Algorithm**: Single-Source Shortest Path using min-heaps in $O((V + E) \log V)$.
- **A\* Pathfinding**: Heuristic-guided search algorithm for optimal grid and graph routing.
- **Floyd-Warshall**: All-Pairs Shortest Path dynamic programming matrix in $O(V^3)$.
- **Tarjan's SCC**: Linear-time $O(V + E)$ identification of Strongly Connected Components using DFS low-link traversal.

### 3. Advanced Trees & Data Structures
- **Segment Tree with Lazy Propagation**: Range sum queries and range delta updates in $O(\log N)$.
- **Fenwick Tree (Binary Indexed Tree)**: Prefix sums and point modifications with minimal memory footprint.
- **Disjoint Set Union (DSU)**: Path compression and union-by-rank heuristics executing in near-linear inverse Ackermann time $\alpha(N)$.
- **Prefix Tree (Trie)**: String dictionary storage, prefix lookup, and predictive text structures.

### 4. String Matching
- **Knuth-Morris-Pratt (KMP)**: Linear $O(N + M)$ pattern search with prefix-function preprocessing.
- **Z-Algorithm**: Longest prefix match array computation in $O(N)$.
- **Polynomial Rolling Hash**: Rabin-Karp substring hashing allowing $O(1)$ equality verification under modulo $10^9 + 7$.

---

## Benchmarks

Run automated performance benchmarks across datasets:

```bash
python -m src.benchmarks.bench_sorts
```

```
+-----------------------------------------------------------------------------+
| Algorithm               | N = 1,000 (ms) | N = 5,000 (ms) | N = 10,000 (ms) |
|-------------------------+----------------+----------------+-----------------|
| QuickSort (3-Way)       |           1.61 |           7.92 |           20.46 |
| MergeSort               |           1.55 |           9.83 |           19.36 |
| HeapSort                |           0.25 |           1.05 |            2.71 |
| RadixSort (LSD)         |           0.51 |           2.53 |            4.73 |
| TimSort (Hybrid)        |           1.20 |           7.70 |           17.34 |
+-----------------------------------------------------------------------------+
```

---

## Verification & Testing

```bash
python -m pytest -v
```

## License

MIT © [Arkadiy Gazizov](https://arkadiygazizov.ru)
