---
date: 2024-01-01 00:00:00 +0000
layout: post
slug: 80a
status: done
tags:
- dp
title: Target Sum
---

## Target Sum [LC#494]
> You are given an integer array `nums` and an integer `target`. You want to build an expression out of nums by adding one of the symbols `+` and `-` before each integer in nums and then concatenate all the integers. For example, if `nums = [2, 1]`, you can add a `+` before 2 and a `-` before 1 and concatenate them to build the expression `"+2-1"`.
Return the number of different expressions that you can build, which evaluates to target.

### Intuition
- Dynamic Programming

### Code
```python
def count_expressions(nums: List[int], target: int) -> int:
    n = len(nums)

    @cache
    def memo(target, i):
        if i == 0:
            if target == 0:
                return 1
            else:
                return 0

        for_plus = +nums[i - 1] + target
        for_minus = -nums[i - 1] + target

        return memo(for_plus, i - 1) + memo(for_minus, i - 1)

    return memo(target, n)
```

### Time complexity
- $T(n) = O(nW)$,  $W = target$ 
- $S(n) = O(nW)$, but can be optimised to $O(W)$