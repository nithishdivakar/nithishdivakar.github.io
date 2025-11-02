---
date: 2024-01-01 00:00:00 +0000
layout: post
slug: 75a04
status: done
tags: []
title: Find Peak Element
---

## Find Peak Element [LC#162]
> A peak element is an element that is strictly greater than its neighbors. Given a 0-indexed integer array nums, find a peak element, and return its index. If the array contains multiple peaks, return the index to any of the peaks. You may imagine that `nums[-1] = nums[n] = $-\infty$`. In other words, an element is always considered to be strictly greater than a neighbor that is outside the array. You must write an algorithm that runs in O(log n) time.

### Intuition

### Code
```python
def find_peak_element(nums: List[int]) -> int:
    lo, hi = 0, len(nums)-1
    nums.append(-math.inf)
    while lo < hi:
        mid = lo + (hi - lo)//2
        if nums[mid] > nums[mid+1]:
            hi = mid
        else:
            lo = mid+1
    return lo
```

### Time complexity
- $T(n) = O(\log n)$ 
- $S(n) = O(1)$