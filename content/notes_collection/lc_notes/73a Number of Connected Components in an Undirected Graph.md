---
date: 2024-01-01 00:00:00 +0000
slug: '73a'
layout: post
status: done
title: Number of Connected Components in an Undirected Graph
tags: [dsu]
---

## Number of Connected Components in an Undirected Graph [LC#323]
> You have a graph of n nodes. You are given an integer n and an array edges where edges[i] = [ai, bi] indicates that there is an edge between ai and bi in the graph. Return the number of connected components in the graph.

### Intuition

### Code
```python
def count_components(self, n: int, edges: List[List[int]]) -> int:
    parent = {i: i for i in range(n)}

    def find(a):
        if parent[a] != a:
            parent[a] = find(parent[a])
        return parent[a]

    def union(a, b):
        a = find(a)
        b = find(b)
        parent[b] = a

    for a, b in edges:
        union(a, b)

    for a, b in edges:
        find(a)
        find(b)

    return len(set(v for k, v in union_find.items()))

```

### Time complexity
- $T(n) = O(V + E\alpha(n))$ 
- $S(n) = O(V)$
