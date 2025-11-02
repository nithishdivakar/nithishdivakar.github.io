---
date: 2024-01-01 00:00:00 +0000
layout: post
slug: 50d01
status: done
tags:
- line sweep
title: Zero Array Transformation I
---

## Zero Array Transformation I [LC#3355]
> You are given an integer array nums of length n and a 2D array queries, where `queries[i] = [li, ri]`. For each `queries[i]`:
> - Select a subset of indices within the range [li, ri] in nums.
> - Decrement the values at the selected indices by 1.
>
> A Zero Array is an array where all elements are equal to 0. Return true if it is possible to transform nums into a Zero Array after processing all the queries sequentially, otherwise return false.

### Intuition
The key idea is to find the maximum possible decrements that can be applied to each element in the array. If the maximum possible decrements for any element is less than the initial value of that element, then it is not possible to transform the array into a Zero Array. We can use a line sweep approach to efficiently compute the maximum possible decrements for each element.

### Code
```python
def is_zero_array(nums: List[int], queries: List[List[int]]) -> bool:
    n = len(nums)
    arr = [0] * n
    for left, right in queries:
        arr[left] += 1
        if right + 1 < n:
            arr[right + 1] -= 1

    prev = 0
    for i in range(n):
        prev += arr[i]
        if prev < nums[i]:
            return False
    return True
```

### TimeComplexity
- $T(n) = O(n)$ and $S(n) = O(n)$