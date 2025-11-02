---
date: 2024-01-01 00:00:00 +0000
layout: post
slug: 01a06
status: done
tags: []
title: Rotate Array
---

## Rotate Array [LC#189]
> Given an integer array nums, rotate the array to the right by k steps, where k is non-negative.

### Intuition
- If we look at the indices formed by k hops, they form a cycle ending at the start indices. If `n%k = 0` , then there are `k` such cycles. 
- We use 1 extra storage and simply swap the elemnts to their right position.

### Code
```python
def rotate_array(nums: List[int], k: int) -> None:
    n = len(nums)
    k = k % n # for k > n
    start = 0
    count = 0
    while count < n:
        curr = start
        storage = nums[curr]
        while True:
            curr = (curr + k) % n
            nums[curr], storage = storage, nums[curr]
            count += 1
            if start == curr:
                break
        start += 1
```

### Time complexity
- $T(n) = O(n)$
- $S(n) = O(1)$