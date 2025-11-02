---
date: 2024-01-01 00:00:00 +0000
layout: post
slug: 50d03
status: doing
tags:
- line sweep
- intervals
title: Smallest Range Covering Elements from K Lists
---

## Smallest Range Covering Elements from K Lists [LC#632]
> You have k lists of sorted integers in non-decreasing order. Find the smallest range that includes at least one number from each of the k lists. We define the range `[a, b]` is smaller than range `[c, d] if b - a < d - c or a < c if b - a == d - c`.



### Intution



### Code
```python
def smallestRange(nums: List[List[int]]) -> List[int]:
    heap = [(arr[0], i, 0) for i, arr in enumerate(nums)]
    heapq.heapify(heap)
    right = max(arr[0] for arr in nums)
    ans = (-math.inf, math.inf)
    
    while heap:
        left, row, col = heapq.heappop(heap)
        if right - left < ans[1] - ans[0]:
            ans = left, right

        if col + 1 == len(nums[row]):
            return ans

        next_point = nums[row][col + 1]
        right = max(right, next_point)
        heapq.heappush(heap, (next_point, row, col + 1))
```

### Time complexity
$n$ max size of lists and $m$ is number of lists
- $T(n) = O(n \log m)$. $S(n) = O(m)$