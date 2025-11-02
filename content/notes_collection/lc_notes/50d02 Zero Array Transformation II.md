---
date: 2024-01-01 00:00:00 +0000
layout: post
slug: 50d02
status: done
tags:
- line sweep
- binary search
title: Zero Array Transformation II
---

## Zero Array Transformation II [LC#3356]
> You are given an integer array nums of length `n` and a 2D array queries where `queries[i] = [l_i, r_i, val_i]`. Each `queries[i]` represents the following action on nums:
> - Decrement the value at each index in the range `[l_i, r_i]` in nums by at most `val_i`. 
> - The amount by which each value is decremented can be chosen independently for each index.
> A Zero Array is an array with all its elements equal to 0. Return the minimum possible non-negative value of `k`, such that after processing the first `k` queries in sequence, nums becomes a Zero Array. If no such `k` exists, return `-1`.


### Intuition
Line sweep and binary search on min queries required.

### Code
```python
def minZeroArray(nums: List[int], queries: List[List[int]]) -> int:
    n, m = len(nums), len(queries)

    def apply_query(T) -> bool:
        arr = [0] * n
        for left, right, val in queries[:T]:
            arr[left] += val
            if right + 1 < n:
                arr[right + 1] -= val
        prev = 0
        for i in range(n):
            prev += arr[i]
            if prev < nums[i]:
                return False
        return True

    L, R = 0, m
    if not apply_query(m):
        return -1

    while L < R:
        mid = L + (R - L) // 2
        if apply_query(mid):
            R = mid
        else:
            L = mid + 1
    return R
```

### TimeComplexity
If $n$ is the size of array and $m$ is number of queries, then
- $T(n) = O(n \log m)$ and $S(n) = O(n)$