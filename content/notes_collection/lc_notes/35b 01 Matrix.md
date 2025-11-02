---
date: 2024-01-01 00:00:00 +0000
layout: post
slug: 35b
status: done
tags:
- bfs
title: 01 Matrix
---

## 01 Matrix [LC#542]
> Given an m x n binary matrix mat, return the distance of the nearest 0 for each cell. The distance between two cells sharing a common edge is 1.

### Intuition
BFS starting at all 0. BFS for binary graph give shortest path. 


### Code
```python
def neares_zero(matrix: List[List[int]]) -> List[List[int]]:
    m = len(matrix)
    n = len(matrix[0])

    def neighbors(x, y):
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < m and 0 <= ny < n:
                yield nx, ny

    queue = deque()
    seen = set()

    for x in range(m):
        for y in range(n):
            if matrix[x][y] == 0:
                queue.append((x, y, 0))
                seen.add((x, y))

    while queue:
        row, col, steps = queue.popleft()
        for nx, ny in neighbors(row, col):
            if (nx, ny) not in seen:
                matrix[nx][ny] = steps + 1
                queue.append((nx, ny, steps + 1))
                seen.add((nx, ny))
    return matrix

```

### Time complexity
- $T(n) = O(mn)$ 
- $S(n) = O(mn)$