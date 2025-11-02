---
date: 2024-01-01 00:00:00 +0000
layout: post
slug: 42b
status: done
title: Prims Algorithm
tags: [mst]
---

## Prim's Algorithm for Minimum spanning tree

- Start with adding a randomly choosen vertex to mst
- Find an edge such that one vertex is in the constructed mst, the other is not and the weight is smallest. Add this edge and vertex to mst
- repeat untill mst has all vertices.

```python
@dataclass
class Edge:
    u: int
    v: int
    w: float

def prims_mst(num_vertices: int, edges: List[Edge]) -> Tuple[List[Edge], float]:
    graph = {u: [] for u in range(num_vertices)}
    for edge in edges:
        graph[edge.u].append((edge.v, edge.w))
        graph[edge.v].append((edge.u, edge.w))

    visited = [False] * num_vertices
    min_heap = [(0.0, 0)]  # (weight, vertex)
    total_cost = 0
    mst_edges = []

    while min_heap:
        weight, u = heapq.heappop(min_heap)
        if visited[u]:
            continue
        visited[u] = True
        total_cost += weight

        if weight > 0:  # Skip the initial vertex
            mst_edges.append(Edge(prev_vertex, u, weight))

        for v, edge_weight in graph[u]:
            if not visited[v]:
                heapq.heappush(min_heap, (edge_weight, v))
                prev_vertex = u  # Track the previous vertex for the edge

    return mst_edges, total_cost, all(visited)
```

Time Complexity
- While loop is executed n times as the MST only has n-1 edges. This give no of times heappop is called. 
- The heap push is called max m times.
- $T(n) = O(n \log n + m \log n) = O((m+n) \log n)$
- $S(n) = O(n)$ for the heap