---
date: 2024-01-01 00:00:00 +0000
layout: post
slug: 35a
status: done
tags:
- bfs
title: Shortest Path in Binary Matrix
---

## Shortest Path in Binary Matrix [LC#1091]
> Given an `n x n` binary matrix grid, return the length of the shortest clear path in the matrix from top left to bottom right. If there is no clear path, return -1. The matrix is 8 connected and you can only move in cells marked 0.

### Intuition
BFS gives the shortest path in binary matrix

### Code
```python
def shortest_path_in_binary_matrix(grid: List[List[int]]) -> int:
    n = len(grid[0])

    def neighbours(x, y):
        for dx, dy in [
            (-1, -1), (-1, +0), (-1, +1),
            (+0, -1),           (+0, +1),
            (+1, -1), (+1, +0), (+1, +1),
        ]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < n:
                yield nx, ny

    if grid[0][0] == 1 or grid[n - 1][n - 1] == 1:
        return -1

    queue = deque()
    seen = set()
    queue.append((0, 0, 1))
    seen.add((0, 0))
    while queue:
        x, y, d = queue.popleft()
        if x == n - 1 and y == n - 1:
            return d
        for nx, ny in neighbours(x, y):
            if grid[nx][ny] == 0 and (nx, ny) not in seen:
                queue.append((nx, ny, d + 1))
                seen.add((nx, ny))
    return -1
```

### Time complexity
- $T(n) = O(mn)$ 
- $S(n) = O(mn)$