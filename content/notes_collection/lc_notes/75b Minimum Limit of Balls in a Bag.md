---
date: 2024-01-01 00:00:00 +0000
layout: post
slug: 75b
status: done
tags:
- binary search
title: Minimum Limit of Balls in a Bag
---

## Minimum Limit of Balls in a Bag [LC#1760]
> You are given an integer array nums where the ith bag contains `nums[i]` balls. You are also given an integer `max_operations`. You can perform the following operation at most `max_operations` times:
> - Take any bag of balls and divide it into two new bags with a positive number of balls. For example, a bag of 5 balls can become two new bags of 1 and 4 balls, or two new bags of 2 and 3 balls.
>
> Your penalty is the maximum number of balls in a bag. You want to minimize your penalty after the operations. Return the minimum possible penalty after performing the operations.


### Intuition
Binary search on penalty.


### Code
```python
def minimum_size(nums: List[int], max_operations: int) -> int:
    def valid(th):
        count = 0
        for num in nums:
            operations = math.ceil(num / th) - 1
            count += operations
            if count > max_operations: return False
        return True
    
    left, right = 1, max(nums)

    while left < right:
        mid = left + (right - left) // 2
        if valid(mid):
            right = mid
        else:
            left = mid + 1
    return left
```

## Time Complexity
The search take `log(range)` steps. The range is of size $2^b$ if $b$ is max number of bits representing the numbers in the list `nums`. Hence number of search steps is upperbounded by $\log (2^b) = b$. Each step take $O(n)$ to evaluate the validity condition. So time complexity $T(n) = O(b \ast n)$. If we consider $b$ as a constant then time complexity is $O(n)$