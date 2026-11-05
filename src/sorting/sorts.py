from typing import List, TypeVar
import heapq

T = TypeVar('T')

def quick_sort(arr: List[T]) -> List[T]:
    """Optimized 3-way partition QuickSort (Dijkstra Dutch National Flag)."""
    if len(arr) <= 1:
        return arr[:]
    
    pivot = arr[len(arr) // 2]
    less = [x for x in arr if x < pivot]
    equal = [x for x in arr if x == pivot]
    greater = [x for x in arr if x > pivot]
    
    return quick_sort(less) + equal + quick_sort(greater)

def merge_sort(arr: List[T]) -> List[T]:
    """Classic Divide & Conquer MergeSort (O(N log N) guaranteed, stable)."""
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
    """In-place style HeapSort using binary min/max heap structure."""
    h = arr[:]
    heapq.heapify(h)
    return [heapq.heappop(h) for _ in range(len(h))]

def radix_sort(arr: List[int]) -> List[int]:
    """LSD Radix Sort for non-negative integers (O(d * (N + b)))."""
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
    """Hybrid sorting algorithm combining insertion sort and merge sort."""
    n = len(arr)
    res = arr[:]
    
    # 1. Sort individual sub-arrays of size RUN with insertion sort
    for start in range(0, n, min_run):
        end = min(start + min_run, n)
        for i in range(start + 1, end):
            key = res[i]
            j = i - 1
            while j >= start and res[j] > key:
                res[j + 1] = res[j]
                j -= 1
            res[j + 1] = key
            
    # 2. Merge runs
    size = min_run
    while size < n:
        for left in range(0, n, 2 * size):
            mid = min(n, left + size)
            right = min(n, left + 2 * size)
            if mid < right:
                # Merge res[left:mid] and res[mid:right]
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
