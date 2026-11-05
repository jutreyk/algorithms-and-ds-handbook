import pytest
from src.sorting.sorts import quick_sort, merge_sort, heap_sort, radix_sort, tim_sort
from src.graphs.graph_algos import bfs, dfs, dijkstra, a_star, floyd_warshall, tarjan_scc
from src.trees_and_ds.structures import DisjointSetUnion, FenwickTree, SegmentTree, Trie
from src.strings.string_algos import kmp_search, z_algorithm, PolynomialRollingHash

def test_sorting_algorithms():
    arr = [64, 34, 25, 12, 22, 11, 90, 0, 12]
    expected = sorted(arr)
    
    assert quick_sort(arr) == expected
    assert merge_sort(arr) == expected
    assert heap_sort(arr) == expected
    assert radix_sort(arr) == expected
    assert tim_sort(arr) == expected

def test_graph_algorithms():
    g = {0: [(1, 4.0), (2, 1.0)], 1: [(3, 1.0)], 2: [(1, 2.0), (3, 5.0)], 3: []}
    dists = dijkstra(g, 0)
    assert dists[3] == 4.0  # 0 -> 2 (1.0) -> 1 (2.0) -> 3 (1.0) = 4.0

    # A*
    h = {0: 3.0, 1: 1.0, 2: 2.0, 3: 0.0}
    cost, path = a_star(g, 0, 3, h)
    assert cost == 4.0
    assert path == [0, 2, 1, 3]

def test_data_structures():
    # DSU
    dsu = DisjointSetUnion(5)
    assert dsu.union(0, 1) is True
    assert dsu.union(1, 2) is True
    assert dsu.find(0) == dsu.find(2)
    assert dsu.find(0) != dsu.find(3)

    # Fenwick Tree
    ft = FenwickTree(5)
    ft.update(1, 10)
    ft.update(2, 20)
    ft.update(3, 30)
    assert ft.range_query(1, 3) == 60
    assert ft.range_query(2, 3) == 50

    # Segment Tree (Lazy)
    st = SegmentTree([1, 2, 3, 4, 5])
    assert st.query_range(0, 4) == 15
    st.update_range(1, 3, 10)  # [1, 12, 13, 14, 5]
    assert st.query_range(1, 3) == 39

    # Trie
    trie = Trie()
    trie.insert("apple")
    assert trie.search("apple") is True
    assert trie.search("app") is False
    assert trie.starts_with("app") is True

def test_string_algorithms():
    text = "ABABDABACDABABCABAB"
    pat = "ABABCABAB"
    assert kmp_search(text, pat) == [10]

    # Z-algorithm
    z = z_algorithm("aabxaabxcaabxaabxay")
    assert z[0] == 0
    assert z[4] == 4

    # Rolling hash
    rh = PolynomialRollingHash("abcdefabc")
    assert rh.get_hash(0, 2) == rh.get_hash(6, 8)  # "abc" == "abc"
