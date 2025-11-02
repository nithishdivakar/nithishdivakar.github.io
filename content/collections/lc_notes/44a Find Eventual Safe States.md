---
date: 2024-01-01 00:00:00 +0000
layout: post
slug: 44a
status: done
tags:
- topological sort
title: Find Eventual Safe States
---

## Find Eventual Safe States [LC#802]
> There is a directed graph of `n` nodes with each node labeled from `0` to `n - 1`. The graph is represented by a 0-indexed 2D integer array graph where `graph[i]` is an integer array of nodes adjacent to node i, meaning there is an edge from node i to each node in `graph[i]`.
>
> A node is a terminal node if there are no outgoing edges. A node is a safe node if every possible path starting from that node leads to a terminal node (or another safe node). Return an array containing all the safe nodes of the graph. The answer should be sorted in ascending order.

### Intuition
Terminal nodes are safe nodes. Any node whose all ougoing edge are to safe nodes are also safe. We can iteratively grow the list of safe nodes this way. Essentially, topological sort on the reverse graph.

### Code
```python
def eventual_safe_nodes(graph: List[List[int]]) -> List[int]:
    n = len(graph)
    in_degree = [0] * n
    reverse_graph = [[] for _ in range(n)]
    for i in range(n):
        for node in graph[i]:
            reverse_graph[node].append(i)
            in_degree[i] += 1
    safe_nodes = []
    queue = deque([i for i in range(n) if in_degree[i]==0])
    while queue:
        node = queue.popleft()
        safe_nodes.append(node)
        for neigh in reverse_graph[node]:
            in_degree[neigh] -= 1
            if in_degree[neigh] == 0:
                queue.append(neigh)
    return sorted(safe_nodes)
```

### Time complexity
$T(n) = $ $S(n) = $