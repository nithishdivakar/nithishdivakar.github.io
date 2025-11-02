---
date: 2024-01-01 00:00:00 +0000
layout: post
slug: 84a03a
status: done
tags:
- greedy
title: Jump Game II
---

## Jump Game II [LC#45]
> You are given a 0-indexed array of integers `nums` of length n. You are initially positioned at `nums[0]`. Each element `nums[i]` represents the maximum length of a forward jump from index `i`. Return the minimum number of jumps to reach the last position.

### Intuition
- There is a DP approach which takes $O(n^2)$ `steps[i] = 1+min(steps[j], 0<=j<i)`

- Say we are at a position left and max reachable range is till right.
- By using a node in this range, we can extend this reachable range by adding another jump. 
- The extended range is `max(nums[i]+i for i in [left, right])`

### Code
```python
def min_jump(nums: List[int]) -> int:
    n = len(nums)
    if n == 1: return 0
    left, right, jumps = 0, 0, 0
    while right < n - 1:
        max_reach = max(nums[i] + i for i in range(left, right + 1))
        left = right 
        right = max_reach
        jumps += 1
    return jumps
```

### Time complexity
- $T(n) = O(n)$ 
- $S(n) = O(1)$