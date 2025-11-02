---
date: 2024-01-01 00:00:00 +0000
slug: '73c'
layout: post
status: done
title: Making A Large Island
tags: [dsu]
---

## Making A Large Island [LC#827]
> You are given an `n x n` binary matrix grid. You are allowed to change at most one 0 to be 1. Return the size of the largest island in grid after applying this operation. An island is a 4-directionally connected group of 1s.

### Intuition
- First make all islands using same technique in connected components
- Then for each 0, compute largest island you can make by flipping it.

### Code
```python
def largest_island(grid: List[List[int]]) -> int:
    parent = {}
    size = {}

    def find(x):
        if x not in parent:
            parent[x], size[x] = x, 1

        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(x, y):
        x = find(x)
        y = find(y)
        if x != y:
            if size[x] < size[y]:
                x, y = y, x
            parent[y], size[x] = x, size[x] + size[y]
        return

    m, n = len(grid), len(grid[0])
    for x in range(m):
        for y in range(n):
            if grid[x][y] == 1:
                find((x, y))
                if x > 0 and grid[x - 1][y] == 1:
                    union((x, y), (x - 1, y))

                if y > 0 and grid[x][y - 1] == 1:
                    union((x, y), (x, y - 1))

    max_size = max(size.values(), default=0)

    for x in range(m):
        for y in range(n):
            if grid[x][y] == 0:
                unique_parents = set()
                if x > 0 and grid[x - 1][y] == 1:
                    unique_parents.add(find((x - 1, y)))
                if y > 0 and grid[x][y - 1] == 1:
                    unique_parents.add(find((x, y - 1)))
                if x < m - 1 and grid[x + 1][y] == 1:
                    unique_parents.add(find((x + 1, y)))
                if y < n - 1 and grid[x][y + 1] == 1:
                    unique_parents.add(find((x, y + 1)))

                new_island_size = 1 + sum(size[p] for p in unique_parents)
                max_size = max(max_size, new_island_size)

    return max_size
```

### Time complexity
- $T(n) = O(mn)$ 
- $S(n) = O(mn)$
