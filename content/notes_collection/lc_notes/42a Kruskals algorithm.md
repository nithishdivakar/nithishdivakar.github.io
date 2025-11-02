---
date: 2024-01-01 00:00:00 +0000
layout: post
slug: 42a
status: done
title: Kruskals algorithm
tags: [mst]
---

## Kruskal's algorithm for Minimum spanning tree

Kruskal's algorithm is as follows. 
- Go in order of lowest to highest weighted edges.
- Add edge to the graph if it doesn't create a cycle. 

```python
@dataclass
class Edge:
    u: int
    v: int
    w: float

def kruskal_mst(num_edges: int, edges: List[Edge]) -> Tuple[List[Edge], float]:
    edges.sort(key=lambda x: x.w)
    dsu = DisjointSetUnion(num_edges)
    mst = []
    total_weight = 0

    for edge in edges:
        if dsu.find(edge.u) != dsu.find(edge.v):
            dsu.union(edge.u, edge.v) 
            mst.append(edge)
            total_weight += edge.w
            
    return mst, total_weight
```

- Time Complexity: $O(m \log m + n + m) = O(m \log n)$ 
    - $O(m \log m)$ for sorting all edges
    - $O(n)$ for make set  on each edges
    - $O(m)$ for find and union on all nodes in edges
- Space Complexity: Extra space to maintaint the DSU datastructure ~ $O(n)$