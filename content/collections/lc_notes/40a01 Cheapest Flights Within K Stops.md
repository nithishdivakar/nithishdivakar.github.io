---
date: 2024-01-01 00:00:00 +0000
layout: post
slug: 40a01
status: done
tags:
- dijkstra sssp
- bfs
title: Cheapest Flights Within K Stops
---

## Cheapest Flights Within K Stops [LC#787]
> There are `n` cities connected by some number of flights. You are given an array flights where `flights[i] = [from_i, to_i, price_i]` indicates that there is a flight from city from_i to city to_i with cost price_i. You are also given three integers `src`, `dst`, and `k`, return the cheapest price from `src` to `dst` with at most `k` stops. If there is no such route, return -1.

### Intuition
- Dijkstra's single source shortest path algorithm with added constraint to update distance only if the stops are less than limit
- Can also solve with level wise BFS. 

### Code : Dijkstra's
```python
def min_distance_within_k_hops(n: int, flights: List[List[int]], src: int, dst: int, k: int) -> int:
    graph = defaultdict(list)
    for frm, to, price in flights:
        graph[frm].append((to, price))
    dist = {src: math.inf for src in range(n)}

    dist[src] = 0
    heap = [(0, 0, src)]

    while heap:
        stops, distance, node = heapq.heappop(heap)

        for neigh, weight in graph[node]:
            if stops <= k and dist[neigh] > distance + weight:
                dist[neigh] = distance + weight
                heapq.heappush(heap, (stops + 1, dist[neigh], neigh))

    return -1 if dist[dst] == math.inf else dist[dst]
```

### Time complexity : Dijkstra's
- $T(n) = O(N + EK \log(EK) )$ 
- $S(n) = O(N + EK)$


### Code : Level wise BFS
```python
def min_distance_within_k_hops(n: int, flights: List[List[int]], src: int, dst: int, k: int) -> int:
    graph = defaultdict(list)
    for frm, to, price in flights:
        graph[frm].append((to, price))
    dist = {src: math.inf for src in range(n)}
    dist[src] = 0
    queue = deque([(src, 0)])

    steps = 0
    while steps <= k and queue:
        level_size = len(queue)
        for _ in range(level_size):
            node, distance = queue.popleft()
            for neigh, weight in graph[node]:
                if dist[neigh] > distance + weight:
                    dist[neigh] = distance + weight
                    queue.append((neigh, dist[neigh]))
        steps += 1
    return -1 if dist[dst] == math.inf else dist[dst]
```


### Time complexity : Level wise BFS
- $T(n) = O(N + EK)$ 
- $S(n) = O(N + EK)$