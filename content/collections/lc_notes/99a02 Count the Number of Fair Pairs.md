---
date: 2024-01-01 00:00:00 +0000
slug: '99a02'
layout: post
status: done
title: Count the Number of Fair Pairs
tags: []
---
Counting problems
## Count the Number of Fair Pairs [LC#2563]
> Given an array two limits `[lower, upper]`, return the number of pairs in the array whose sum is withihg the limits (includive)

### Intuition
- `Count[L <= s <= U] = Count[s <= U] - Count[s <= L - 1]`

### Code
```python
def pairs_within_bounds(self, nums: List[int], lower: int, upper: int) -> int:
    nums = sorted(nums)
    U = self.count_lower_sorted(nums, upper)
    L = self.count_lower_sorted(nums, lower - 1)
    return U - L

def pairs_below_bounds(self, nums: List[int], th: int ):
    left, right = 0, len(nums) - 1
    counts = 0
    while left < right:
        s = nums[left] + nums[right]
        if s <= th:
            counts += right - left
            left += 1
        else:
            right -= 1
    return counts
```

### Time complexity
- $T(n) = O(n \log n) + O(n)$ dominated by sorting 
- $S(n) = O(1)$ if we sort in place.
