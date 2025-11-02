---
date: 2024-01-01 00:00:00 +0000
layout: post
slug: 84a03b
status: done
tags: [bfs]
title: Jump Game III
---

## Jump Game III [LC#1306]
> Given an array of non-negative integers arr, you are initially positioned at start index of the array. When you are at index `i`, you can jump to `i + arr[i]` or `i - arr[i]`, check if you can reach any index with value 0. Notice that you can not jump outside of the array at any time.

### Intuition
- BFS

### Code
```python
def jump(arr: List[int], start: int) -> bool:
    seen = set([start])
    queue = deque([start])
    n = len(arr)
    while queue:
        node = queue.popleft()
        if arr[node]==0: return True

        for idx in [node+arr[node],  node-arr[node]]:
            if idx not in seen and 0 <= idx < n:
                queue.append(idx)
                seen.add(idx)
    return False
```

### Time complexity
- $T(n) = O(n)$ 
- $S(n) = O(n)$. We can use original array to maintain seen nodes by making them negative.