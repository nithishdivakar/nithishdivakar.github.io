---
date: 2024-01-01 00:00:00 +0000
layout: post
slug: 75d
status: done
tags:
- binary search
title: Split Array Largest Sum
---

## Split Array Largest Sum [LC#412]
> Given an integer array nums and an integer k, split nums into k non-empty subarrays such that the largest sum of any subarray is minimized. Return the minimized largest sum of the split. A subarray is a contiguous part of the array.


### Intuition
Binary search on the range of possible values.


### Code
```python
def splita_array_largest_sum(nums: List[int], k: int) -> int:
    left, right = max(nums), sum(nums)

    def valid(th):
        num_partitions = 0
        sum_partition = 0
        for num in nums:
            if sum_partition + num <= th:
                sum_partition += num
            else:
                sum_partition = num
                num_partitions += 1
            if num_partitions >= k:
                return False
        return True

    while left < right:
        mid = left + (right - left) // 2
        if valid(mid):
            right = mid
        else:
            left = mid + 1
    return right
```

## Time Complexity
The search take `log(range)` steps. The range is of size $2^b$ if $b$ is max number of bits representing the numbers in the list `nums`. Hence number of search steps is upperbounded by $\log (2^b) = b$. Each step take $O(n)$ to evaluate the validity condition. So time complexity $T(n) = O(b \ast n)$. If we consider $b$ as a constant then time complexity is $O(n)$