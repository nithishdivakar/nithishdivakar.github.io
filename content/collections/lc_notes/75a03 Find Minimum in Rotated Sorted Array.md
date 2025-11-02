---
date: 2024-01-01 00:00:00 +0000
layout: post
slug: 75a03
status: done
tags:
- binary search
title: Find Minimum in Rotated Sorted Array
---

## Find Minimum in Rotated Sorted Array [LC#153]
> Suppose an array of length n sorted in ascending order is rotated between 1 and n times. For example, the array nums = [0,1,2,4,5,6,7] might become:
> - [4,5,6,7,0,1,2] if it was rotated 4 times.
> - [0,1,2,4,5,6,7] if it was rotated 7 times.
> 
> Notice that rotating an array `[a[0], a[1], a[2], ..., a[n-1]]` 1 time results in the array `[a[n-1], a[0], a[1], a[2], ..., a[n-2]]`. Given the sorted rotated array nums of unique elements, return the minimum element of this array.

### Intuition
minimum number is present in the smallest index `k` such that `nums[k] < nums[-1]`

### Code
```python
def findMin(nums: List[int]) -> int:
    left, right = 0, len(nums) - 1
    while left < right:
        mid = left + (right - left) // 2
        if nums[mid] <= nums[-1]:
            right = mid
        else:
            left = mid + 1
    return nums[left] 
```