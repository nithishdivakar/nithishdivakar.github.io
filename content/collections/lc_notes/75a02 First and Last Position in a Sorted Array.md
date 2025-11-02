---
date: 2024-01-01 00:00:00 +0000
layout: post
slug: 75a02
status: done
tags:
- binary search
title: First and Last Position in a Sorted Array
---

## Find First and Last Position of Element in Sorted Array [LC#34]
> Given an array of integers nums sorted in non-decreasing order, find the starting and ending position of a given target value. If target is not found in the array, return [-1, -1]. You must write an algorithm with O(log n) runtime complexity.


### Code
```python
def searchRange(nums: List[int], target: int) -> Tuple[int, int]:
    def binary_search(value):
        left, right = 0, len(nums) - 1
        while left < right:
            mid = left + (right - left) // 2
            if nums[mid] >= value:
                right = mid
            else:
                left = mid + 1
        return left

    nums.append(math.inf) # to handle edge cases

    pos_beg = binary_search(target)
    if nums[pos_beg] != target:
        return (-1, -1)
    pos_end = binary_search(target + 1)
    return (pos_beg, pos_end - 1)
```

### Time Complexity
$T(n) = O(\log n)$