---
date: 2024-01-01 00:00:00 +0000
layout: post
slug: 14d
status: done
title: Subarray Sum Equals K
---

## Subarray Sum Equals K [LC#560]
> Given an array of integers nums and an integer k, return the total number of subarrays whose sum equals to k. A subarray is a contiguous non-empty sequence of elements within an array.


### Intuition
- For quickly finiding sum of a subarray, we can use prefix sums. 
    - `sum(i:j) = prefix(i) - prefix(j)`
- While we are computing prefix(i) if `residue = prefix(i) - k` is already among prefixes, then there is a subarray with sum k. We simply have to keep a count.

### Solution

```python
def count_subarray_sum_to_targets(nums: List[int], k: int) -> int:
    prefixes = defaultdict(int)
    prefixes[0] = 1 # empty array is a subarray of sum 0

    current = 0
    counts = 0
    for num in nums:
        current += num
        counts += prefixes[current - k]
        prefixes[current] += 1
    return counts
```
## Time Complexity
- $T(n) = O(n)$ and $S(n) = O(n)$