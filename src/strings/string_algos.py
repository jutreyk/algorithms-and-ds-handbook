from typing import List

def kmp_search(text: str, pattern: str) -> List[int]:
    """Knuth-Morris-Pratt string matching algorithm in O(N + M)."""
    if not pattern or not text:
        return []

    # 1. Compute Prefix Function (pi)
    m = len(pattern)
    pi = [0] * m
    j = 0
    for i in range(1, m):
        while j > 0 and pattern[i] != pattern[j]:
            j = pi[j - 1]
        if pattern[i] == pattern[j]:
            j += 1
        pi[i] = j

    # 2. Search pattern in text
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
    """Computes Z-array for string s in linear time O(N)."""
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
    """Rabin-Karp polynomial rolling hash for O(1) substring equality queries."""
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
        """Returns hash of s[left:right+1] (0-indexed)."""
        val = (self.pref_hash[right + 1] - self.pref_hash[left] * self.powers[right - left + 1]) % self.mod
        return (val + self.mod) % self.mod
