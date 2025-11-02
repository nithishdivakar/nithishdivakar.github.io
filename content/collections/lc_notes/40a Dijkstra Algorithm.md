---
date: 2024-01-01 00:00:00 +0000
layout: post
slug: 40a
status: done
title: Dijkstra Algorithm
tags:
- dijkstra sssp
---

## Dijkstra algorithm

- `graph = {u : [(v, w(u,v)), ..], ... }`
```python
def dijkstra(graph: List[List[Tuple[int, float]]], source: int) -> List[float]:
    n = len(graph)
    distances: List[float] = [math.inf] * n
    distances[source] = 0.0
    heap: List[Tuple[float, int]] = [(0.0, source)]

    while heap:
        curr_dist, node = heapq.heappop(heap)
        # if curr_dist > distances[node]:
        #     continue
        
        for neighbour, weight in graph[node]:
            dist = curr_dist + weight
            if dist < distances[neighbour]:
                distances[neighbour] = dist
                heapq.heappush(heap, (dist, neighbour))
    
    return distances
```
- $T(n) = O( (V+E) \log V)$
    - $O(V \log\{V\})$: Extract the minimum node from the heap for each vertex.
    - $O(E \log\{V\})$: Time taken to insert or update distances for each edge.    
- $S(n) = O(V)$