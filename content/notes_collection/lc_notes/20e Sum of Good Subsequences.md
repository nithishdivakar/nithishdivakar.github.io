---
date: 2024-01-01 00:00:00 +0000
layout: post
slug: 20e
status: done
tags:
- sub sequence
- dp
title: Sum of Good Subsequences
---

## Sum of Good Subsequences [LC#3351]
> You are given an integer array nums. A good subsequence is defined as a subsequence of nums where the absolute difference between any two consecutive elements in the subsequence is exactly 1. Return the sum of all possible good subsequences of nums (modulo  $10^9 + 7$). Note that a subsequence of size 1 is considered good by definition.

### Intuition
- We can append `num` to a sequence ending in `num-1` or `num+1` or start a new good subsequence, i.e,  `count[num] = count[num-1] + count[num+1] + 1`
- Contribution of `num` to the final sum is `(num * count[num])`. But to avoid duplicates, we iterate over the array and keep the total in another counter

### Solution
```python
def sum_of_good_subsequences(nums: List[int]) -> int:
    mod = 10 ** 9 + 7
    total = Counter()
    count = Counter()
    for num in nums:
        ending_at = count[num - 1] + count[num + 1] + 1
        total[num] += total[num - 1] + total[num + 1] + num * ending_at
        count[num] += ending_at
    return sum(total.values()) % mod
```

### Time Complexity
- $T(n) = O(n)$; $S(n) = O(n)$