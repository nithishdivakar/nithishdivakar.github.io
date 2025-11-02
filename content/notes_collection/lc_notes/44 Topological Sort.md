---
date: 2024-01-01 00:00:00 +0000
layout: post
level: h1
slug: '44'
status: done
title: Topological Sort
tags:
- topological sort
---

## Topological Sort

### Kahn's Algorithm (BFS-like)

```python
def topological_sort_kahn(graph: Dict[str, List[str]]) -> List[str]:
    in_degree = {u: 0 for u in graph}  # Initialize in-degrees to 0
    for u in graph:
        for v in graph[u]:
            in_degree[v] += 1  # Increment in-degree for each edge

    queue = deque([u for u in in_degree if in_degree[u] == 0])
    topological_order = []

    while queue:
        u = queue.popleft()  # Get a vertex with in-degree 0
        topological_order.append(u)  # Add it to the topological order
        
        for v in graph[u]:
            in_degree[v] -= 1  # Remove the edge u -> v
            if in_degree[v] == 0:  # If in-degree becomes 0, add to queue
                queue.append(v)

    if len(topological_order) != len(graph):
        return []
    return topological_order
```

**Example Graph**
```
graph = {
    'A': ['C'],
    'B': ['C', 'D'],
    'C': ['E'],
    'D': ['E'],
    'E': []
}
```

### DFS like topological sort
```python
def topological_sort_dfs(graph: Dict[str, List[str]]) -> List[str]:
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {node: WHITE for node in graph}
    stack: List[str] = []

    def dfs(node: str) -> bool:
        if color[node] == GRAY:
            return False # Cycle detected
        if color[node] == WHITE:
            color[node] = GRAY
            for neighbor in graph[node]:
                if not dfs(neighbor):
                    # cycle in recursion
                    return False
            color[node] = BLACK
            stack.append(node)
        return True

    for vertex in graph:
        if color[vertex] == WHITE:
            if not dfs(vertex):  # If a cycle is detected
                return []

    return stack[::-1]
```