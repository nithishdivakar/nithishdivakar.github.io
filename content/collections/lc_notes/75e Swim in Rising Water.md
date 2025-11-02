---
date: 2024-01-01 00:00:00 +0000
layout: post
slug: 75e
status: done
tags:
- binary search
- bfs
title: Swim in Rising Water
---

## Swim in Rising Water [LC#778]
> You are given an `n x n` integer matrix grid where each value `grid[i][j]` represents the elevation at that point `(i, j)`. The rain starts to fall. At time `t`, the depth of the water everywhere is `t`. You can swim from a square to another 4-directionally adjacent square if and only if the elevation of both squares individually are at most t. You can swim infinite distances in zero time. Of course, you must stay within the boundaries of the grid during your swim.
>
> Return the least time until you can reach the bottom right square `(n - 1, n - 1)` if you start at the top left square `(0, 0)`.

### Intuition
- Solution is a path from source to target with least maximum elevation.
- Binary search on all possible paths 
- BFS or DFS can be used interchangeably

### Code
```python
def swim_in_water(grid: List[List[int]]) -> int:
    m, n = len(grid), len(grid[0])

    def neighbours(x, y):
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if (0 <= nx < m) and (0 <= ny < n):
                yield (nx, ny)

    def bfs_with_limit(limit):
        queue = deque([(0, 0)])
        seen = {(0, 0)}
        while queue:
            row, col = queue.popleft()
            if (row, col) == (m - 1, n - 1):
                return True
            for nx, ny in neighbours(row, col):
                if (nx, ny) not in seen and grid[nx][ny] <= limit:
                    queue.append((nx, ny))
                    seen.add((nx, ny))
        return False

    lo, hi = grid[0][0], max(max(grid[i]) for i in range(m))

    while lo < hi:
        mid = lo + (hi - lo) // 2
        if bfs_with_limit(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo
```

### Time complexity
- $T(n) = O(\log(2^b) mn) = O(mn)$
- $S(n) = O(mn)$