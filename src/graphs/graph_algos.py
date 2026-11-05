from collections import deque
import heapq
from typing import Dict, List, Tuple, Optional, Set

Graph = Dict[int, List[Tuple[int, float]]]  # node -> [(neighbor, weight)]

def bfs(graph: Dict[int, List[int]], start: int) -> List[int]:
    """Breadth-First Search traversal."""
    visited: Set[int] = set([start])
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
    """Depth-First Search iterative traversal."""
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
    """Dijkstra's Single-Source Shortest Path using Min-Heap (O((V + E) log V))."""
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
    """A* Pathfinding Algorithm with admissible heuristic."""
    open_set: List[Tuple[float, int]] = [(heuristic.get(start, 0.0), start)]
    came_from: Dict[int, int] = {}
    g_score: Dict[int, float] = {start: 0.0}
    
    while open_set:
        _, current = heapq.heappop(open_set)
        
        if current == goal:
            # Reconstruct path
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
    """All-Pairs Shortest Paths in O(V^3)."""
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
    """Tarjan's algorithm for finding Strongly Connected Components in linear time O(V + E)."""
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
