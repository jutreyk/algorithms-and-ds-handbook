import heapq
from collections import deque
from typing import List, Dict, Tuple, Optional, Set, TypeVar

T = TypeVar('T')

def quick_sort(arr: List[T]) -> List[T]:
    if len(arr) <= 1:
        return arr[:]
    pivot = arr[len(arr) // 2]
    less = [x for x in arr if x < pivot]
    equal = [x for x in arr if x == pivot]
    greater = [x for x in arr if x > pivot]
    return quick_sort(less) + equal + quick_sort(greater)

def merge_sort(arr: List[T]) -> List[T]:
    if len(arr) <= 1:
        return arr[:]
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    merged = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged

def heap_sort(arr: List[T]) -> List[T]:
    h = arr[:]
    heapq.heapify(h)
    return [heapq.heappop(h) for _ in range(len(h))]

def radix_sort(arr: List[int]) -> List[int]:
    if not arr:
        return []
    max_val = max(arr)
    exp = 1
    res = arr[:]
    while max_val // exp > 0:
        buckets = [[] for _ in range(10)]
        for num in res:
            digit = (num // exp) % 10
            buckets[digit].append(num)
        res = [num for bucket in buckets for num in bucket]
        exp *= 10
    return res

def tim_sort(arr: List[T], min_run: int = 32) -> List[T]:
    n = len(arr)
    res = arr[:]
    for start in range(0, n, min_run):
        end = min(start + min_run, n)
        for i in range(start + 1, end):
            key = res[i]
            j = i - 1
            while j >= start and res[j] > key:
                res[j + 1] = res[j]
                j -= 1
            res[j + 1] = key
    size = min_run
    while size < n:
        for left in range(0, n, 2 * size):
            mid = min(n, left + size)
            right = min(n, left + 2 * size)
            if mid < right:
                merged = []
                i, j = left, mid
                while i < mid and j < right:
                    if res[i] <= res[j]:
                        merged.append(res[i])
                        i += 1
                    else:
                        merged.append(res[j])
                        j += 1
                merged.extend(res[i:mid])
                merged.extend(res[j:right])
                res[left:right] = merged
        size *= 2
    return res

Graph = Dict[int, List[Tuple[int, float]]]

def bfs(graph: Dict[int, List[int]], start: int) -> List[int]:
    visited: Set[int] = {start}
    queue = deque([start])
    order = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    return order

def dfs(graph: Dict[int, List[int]], start: int) -> List[int]:
    visited: Set[int] = set()
    stack = [start]
    order = []
    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            order.append(node)
            for neighbor in reversed(graph.get(node, [])):
                if neighbor not in visited:
                    stack.append(neighbor)
    return order

def dijkstra(graph: Graph, start: int) -> Dict[int, float]:
    distances: Dict[int, float] = {start: 0.0}
    pq: List[Tuple[float, int]] = [(0.0, start)]
    while pq:
        curr_dist, u = heapq.heappop(pq)
        if curr_dist > distances.get(u, float('inf')):
            continue
        for v, weight in graph.get(u, []):
            dist = curr_dist + weight
            if dist < distances.get(v, float('inf')):
                distances[v] = dist
                heapq.heappush(pq, (dist, v))
    return distances

def a_star(graph: Graph, start: int, goal: int, heuristic: Dict[int, float]) -> Optional[Tuple[float, List[int]]]:
    open_set: List[Tuple[float, int]] = [(heuristic.get(start, 0.0), start)]
    came_from: Dict[int, int] = {}
    g_score: Dict[int, float] = {start: 0.0}
    while open_set:
        _, current = heapq.heappop(open_set)
        if current == goal:
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            path.reverse()
            return g_score[goal], path
        for neighbor, weight in graph.get(current, []):
            tentative_g = g_score[current] + weight
            if tentative_g < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score = tentative_g + heuristic.get(neighbor, 0.0)
                heapq.heappush(open_set, (f_score, neighbor))
    return None

def floyd_warshall(nodes: List[int], edges: List[Tuple[int, int, float]]) -> Dict[Tuple[int, int], float]:
    dist: Dict[Tuple[int, int], float] = {}
    for u in nodes:
        for v in nodes:
            dist[(u, v)] = 0.0 if u == v else float('inf')
    for u, v, w in edges:
        dist[(u, v)] = min(dist[(u, v)], w)
    for k in nodes:
        for i in nodes:
            for j in nodes:
                if dist[(i, k)] + dist[(k, j)] < dist[(i, j)]:
                    dist[(i, j)] = dist[(i, k)] + dist[(k, j)]
    return dist

def tarjan_scc(graph: Dict[int, List[int]], nodes: List[int]) -> List[List[int]]:
    index = 0
    indices: Dict[int, int] = {}
    lowlink: Dict[int, int] = {}
    on_stack: Set[int] = set()
    stack: List[int] = []
    sccs: List[List[int]] = []

    def strongconnect(v: int):
        nonlocal index
        indices[v] = index
        lowlink[v] = index
        index += 1
        stack.append(v)
        on_stack.add(v)
        for w in graph.get(v, []):
            if w not in indices:
                strongconnect(w)
                lowlink[v] = min(lowlink[v], lowlink[w])
            elif w in on_stack:
                lowlink[v] = min(lowlink[v], indices[w])
        if lowlink[v] == indices[v]:
            scc = []
            while True:
                w = stack.pop()
                on_stack.remove(w)
                scc.append(w)
                if w == v:
                    break
            sccs.append(scc)

    for node in nodes:
        if node not in indices:
            strongconnect(node)
    return sccs

class DisjointSetUnion:
    def __init__(self, size: int):
        self.parent = list(range(size))
        self.rank = [0] * size

    def find(self, i: int) -> int:
        if self.parent[i] != i:
            self.parent[i] = self.find(self.parent[i])
        return self.parent[i]

    def union(self, i: int, j: int) -> bool:
        root_i = self.find(i)
        root_j = self.find(j)
        if root_i == root_j:
            return False
        if self.rank[root_i] < self.rank[root_j]:
            self.parent[root_i] = root_j
        elif self.rank[root_i] > self.rank[root_j]:
            self.parent[root_j] = root_i
        else:
            self.parent[root_j] = root_i
            self.rank[root_i] += 1
        return True

class FenwickTree:
    def __init__(self, size: int):
        self.size = size
        self.tree = [0] * (size + 1)

    def update(self, idx: int, delta: int):
        while idx <= self.size:
            self.tree[idx] += delta
            idx += idx & (-idx)

    def query(self, idx: int) -> int:
        s = 0
        while idx > 0:
            s += self.tree[idx]
            idx -= idx & (-idx)
        return s

    def range_query(self, left: int, right: int) -> int:
        return self.query(right) - self.query(left - 1)

class SegmentTree:
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
        return self.query_range(l, r, 2 * node, start, mid) + self.query_range(l, r, 2 * node + 1, mid + 1, end)

class TrieNode:
    def __init__(self):
        self.children: Dict[str, TrieNode] = {}
        self.is_terminal: bool = False

class Trie:
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

def kmp_search(text: str, pattern: str) -> List[int]:
    if not pattern or not text:
        return []
    m = len(pattern)
    pi = [0] * m
    j = 0
    for i in range(1, m):
        while j > 0 and pattern[i] != pattern[j]:
            j = pi[j - 1]
        if pattern[i] == pattern[j]:
            j += 1
        pi[i] = j
    occurrences = []
    j = 0
    for i in range(len(text)):
        while j > 0 and text[i] != pattern[j]:
            j = pi[j - 1]
        if text[i] == pattern[j]:
            j += 1
        if j == m:
            occurrences.append(i - m + 1)
            j = pi[j - 1]
    return occurrences

def z_algorithm(s: str) -> List[int]:
    n = len(s)
    z = [0] * n
    l = r = 0
    for i in range(1, n):
        if i <= r:
            z[i] = min(r - i + 1, z[i - l])
        while i + z[i] < n and s[z[i]] == s[i + z[i]]:
            z[i] += 1
        if i + z[i] - 1 > r:
            l = i
            r = i + z[i] - 1
    return z

class PolynomialRollingHash:
    def __init__(self, s: str, base: int = 31, mod: int = 1_000_000_007):
        self.mod = mod
        self.base = base
        n = len(s)
        self.pref_hash = [0] * (n + 1)
        self.powers = [1] * (n + 1)
        for i in range(n):
            self.powers[i + 1] = (self.powers[i] * base) % mod
            self.pref_hash[i + 1] = (self.pref_hash[i] * base + ord(s[i])) % mod

    def get_hash(self, left: int, right: int) -> int:
        val = (self.pref_hash[right + 1] - self.pref_hash[left] * self.powers[right - left + 1]) % self.mod
        return (val + self.mod) % self.mod
