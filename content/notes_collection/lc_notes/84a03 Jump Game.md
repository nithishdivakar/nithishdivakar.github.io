---
date: 2024-01-01 00:00:00 +0000
layout: post
slug: 84a03
status: done
tags:
- greedy
title: Jump Game
---

## Jump Game [LC#55]
> You are given an integer array nums. You are initially positioned at the array's first index, and each element in the array represents your maximum jump length at that position. Return true if you can reach the last index, or false otherwise.

### Intuition
There is a dp approach. But time complexity is $O(n^2)$ with linear storage. The greedy approach. 

- We keep track of the positions from which last index is reachable. In the begning its the last index itself.
- traverse the array in the reverse order. If we can reach on of the exisiting reachable position from current index, then the curent index is also in reachable. 

### Code
```python
def jump_game(nums: List[int]) -> bool:
    n = len(nums)
    left_limit = n - 1
    for pos in range(n - 1, -1, -1):
        if pos + nums[pos] >= left_limit:
            left_limit = pos
    return left_limit == 0
```

### Time complexity
- $T(n) = O(n)$
- $S(n) = O(1)$