---
date: 2024-01-01 00:00:00 +0000
layout: post
slug: 01a01
status: done
title: Two Sum
---

## Two sum [LC#1]
> Given an array of integers `nums` and an `integer` target, return indices of the two numbers such that they add up to target. You may assume that each input would have exactly one solution, and you may not use the same element twice. You can return the answer in any order.


### Sorting and two pointers
- $T(n) = O(n \log n)$; $S(n) = O(n)$ for maintaining the index.

```python
def two_sum(nums: List[int], target:Int) -> Tuple[int, int]:
    indexed_nums  = sorted((n, i) for i, n in enumerate(nums))
    left, right = 0, len(indexed_nums) - 1
    
    while left < right:
        current_sum = indexed_nums[left][0] + indexed_nums[right][0]
        
        if current_sum == target:
            return (indexed_nums[left][1], indexed_nums[right][1])
        elif current_sum < target:
            left += 1
        else:
            right -= 1

    return (-1, -1)
```

### Hashset
- $T(n) = O(n)$; $S(n) = O(n)$

```python
def two_sum(nums: List[int], target: int) -> Tuple[int, int]:
    num_to_idx = {}
    for i, num in enumerate(nums):
        residue = target - num
        if residue in lut:
            return (i, num_to_idx[residue])
        num_to_idx[num] = i
    return (-1, -1)
```