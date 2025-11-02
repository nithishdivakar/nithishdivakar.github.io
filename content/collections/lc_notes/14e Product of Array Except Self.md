---
date: 2024-01-01 00:00:00 +0000
layout: post
slug: 14e
status: done
title: Product of Array Except Self
---

## Product of Array Except Self [LC#238]
> Given an integer array nums, return an array answer such that `answer[i]` is equal to the product of all the elements of nums except `nums[i]`. The product of any prefix or suffix of nums is guaranteed to fit in a 32-bit integer. You must write an algorithm that runs in O(n) time and without using the division operation.

### Code 
```python
def product_except(nums: List[int]) -> List[int]:
    n = len(nums)
    ans = [1,]
    for i in range(n - 1):
        ans.append(ans[-1] * nums[i])
    post = 1
    for i in range(n - 2, -1, -1):
        post = post * nums[i + 1]
        ans[i] = ans[i] * post
    return ans
```

### Time Complexity
- $T(n)= O(n)$ and $S(n)= O(n)$