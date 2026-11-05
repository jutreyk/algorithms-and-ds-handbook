from typing import List, Dict, Optional, Any

class DisjointSetUnion:
    """Disjoint Set Union (DSU / Union-Find) with path compression and rank heuristic."""
    def __init__(self, size: int):
        self.parent = list(range(size))
        self.rank = [0] * size

    def find(self, i: int) -> int:
        if self.parent[i] != i:
            self.parent[i] = self.find(self.parent[i])  # Path compression
        return self.parent[i]

    def union(self, i: int, j: int) -> bool:
        root_i = self.find(i)
        root_j = self.find(j)
        if root_i == root_j:
            return False  # Already in same set
            
        # Union by rank
        if self.rank[root_i] < self.rank[root_j]:
            self.parent[root_i] = root_j
        elif self.rank[root_i] > self.rank[root_j]:
            self.parent[root_j] = root_i
        else:
            self.parent[root_j] = root_i
            self.rank[root_i] += 1
        return True

class FenwickTree:
    """Binary Indexed Tree (Fenwick) for prefix sums and point updates in O(log N)."""
    def __init__(self, size: int):
        self.size = size
        self.tree = [0] * (size + 1)

    def update(self, idx: int, delta: int):
        """Adds delta to element at 1-based index idx."""
        while idx <= self.size:
            self.tree[idx] += delta
            idx += idx & (-idx)

    def query(self, idx: int) -> int:
        """Returns prefix sum from index 1 to idx."""
        s = 0
        while idx > 0:
            s += self.tree[idx]
            idx -= idx & (-idx)
        return s

    def range_query(self, left: int, right: int) -> int:
        return self.query(right) - self.query(left - 1)

class SegmentTree:
    """Segment Tree with Lazy Propagation supporting range add and range sum queries."""
    def __init__(self, arr: List[int]):
        self.n = len(arr)
        self.tree = [0] * (4 * self.n)
        self.lazy = [0] * (4 * self.n)
        if self.n > 0:
            self._build(arr, 1, 0, self.n - 1)

    def _build(self, arr: List[int], node: int, start: int, end: int):
        if start == end:
            self.tree[node] = arr[start]
            return
        mid = (start + end) // 2
        self._build(arr, 2 * node, start, mid)
        self._build(arr, 2 * node + 1, mid + 1, end)
        self.tree[node] = self.tree[2 * node] + self.tree[2 * node + 1]

    def _push(self, node: int, start: int, end: int):
        if self.lazy[node] != 0:
            val = self.lazy[node]
            mid = (start + end) // 2
            
            self.tree[2 * node] += val * (mid - start + 1)
            self.lazy[2 * node] += val
            
            self.tree[2 * node + 1] += val * (end - mid)
            self.lazy[2 * node + 1] += val
            
            self.lazy[node] = 0

    def update_range(self, l: int, r: int, delta: int, node: int = 1, start: int = 0, end: Optional[int] = None):
        if end is None:
            end = self.n - 1
            
        if l > end or r < start:
            return
            
        if l <= start and end <= r:
            self.tree[node] += delta * (end - start + 1)
            self.lazy[node] += delta
            return
            
        self._push(node, start, end)
        mid = (start + end) // 2
        self.update_range(l, r, delta, 2 * node, start, mid)
        self.update_range(l, r, delta, 2 * node + 1, mid + 1, end)
        self.tree[node] = self.tree[2 * node] + self.tree[2 * node + 1]

    def query_range(self, l: int, r: int, node: int = 1, start: int = 0, end: Optional[int] = None) -> int:
        if end is None:
            end = self.n - 1
            
        if l > end or r < start:
            return 0
            
        if l <= start and end <= r:
            return self.tree[node]
            
        self._push(node, start, end)
        mid = (start + end) // 2
        left_sum = self.query_range(l, r, 2 * node, start, mid)
        right_sum = self.query_range(l, r, 2 * node + 1, mid + 1, end)
        return left_sum + right_sum

class TrieNode:
    def __init__(self):
        self.children: Dict[str, TrieNode] = {}
        self.is_terminal: bool = False

class Trie:
    """Prefix Tree (Trie) for dictionary string search and autocompletion."""
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str):
        curr = self.root
        for ch in word:
            if ch not in curr.children:
                curr.children[ch] = TrieNode()
            curr = curr.children[ch]
        curr.is_terminal = True

    def search(self, word: str) -> bool:
        curr = self.root
        for ch in word:
            if ch not in curr.children:
                return False
            curr = curr.children[ch]
        return curr.is_terminal

    def starts_with(self, prefix: str) -> bool:
        curr = self.root
        for ch in prefix:
            if ch not in curr.children:
                return False
            curr = curr.children[ch]
        return True
