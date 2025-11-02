---
date: 2024-01-01 00:00:00 +0000
layout: post
slug: 42a01
status: done
tags: [mst]
title: Min Cost to Connect All Points
---

## Min Cost to Connect All Points [LC#1584]
> You are given an array points representing integer coordinates of some points on a 2D-plane, where `points[i] = [xi, yi]`. The cost of connecting two points `[xi, yi]` and `[xj, yj]` is the manhattan distance between them: `|xi - xj| + |yi - yj|`. Return the minimum cost to make all points connected. All points are connected if there is exactly one simple path between any two points.

### Intuition
- Generate the graph of all pairs with distance. 
- The answer is MST of this graph

### Code
```python
def min_cost_connect_points(points: List[List[int]]) -> int:
    class DSU:
        def __init__(self):
            self.parent = {}
            self.rank = {}

        def find(self, node):
            if node not in self.parent:
                self.parent[node] = node
                self.rank[node] = 1

            if self.parent[node] != node:
                self.parent[node] = self.find(self.parent[node])
            return self.parent[node]

        def union(self, x, y):
            x = self.find(x)
            y = self.find(y)
            if x == y:
                return False

            if self.rank[x] < self.rank[y]:
                x, y = y, x

            self.parent[y] = x
            if self.rank[x] == self.rank[y]:
                self.rank[x] += 1

            return True

    def manhattan_distance(p, q):
        return abs(p[0] - q[0]) + abs(p[1] - q[1])

    dsu = DSU()
    edge_list = []
    for i in range(len(points)):
        dsu.find(i)
        for j in range(0, i):
            edge_list.append((i, j, manhattan_distance(points[i], points[j])))

    edge_list.sort(key=lambda r: r[2])
    min_cost = 0
    for i, j, d in edge_list:
        if dsu.find(i) != dsu.find(j):
            min_cost += d
            dsu.union(i, j)

    return min_cost
```

### Time complexity
If n is number of points 
- $T(n) = O(n^2) + O(n^2 \log n^2) + O(n^2)$ Constructing graph, sorting edges, mst construction. 
- $S(n) = O(n^2)$