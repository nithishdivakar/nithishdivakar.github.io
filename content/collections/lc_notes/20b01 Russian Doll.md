---
date: 2024-01-01 00:00:00 +0000
layout: post
slug: 20b01
status: done
title: Russian Doll
---

## Russian Doll Envelopes [LC#354]
> You are given a 2D array of integers envelopes where envelopes[i] = [wi, hi] represents the width and the height of an envelope. One envelope can fit into another if and only if both the width and height of one envelope are greater than the other envelope's width and height. Return the maximum number of envelopes you can Russian doll (i.e., put one inside the other).
> _Note: You cannot rotate an envelope._


### Intuition
- The problem is a 2D version of Longest Increasing Subsequence, but since the item order is not static in the original problem, we can convert it to a 1D version as follows. 
- If a set of envelopes share same width, then 2 in such should not be selected. To ensure this, we sort the sequence in increasing order of width and then decreasing order of height. This also ensures that when a taller one is selected, the shorter ones are not selected after that. 

### Code
```python

def russian_dolls(envelopes: List[List[int]]) -> int:
    envelopes.sort(key=lambda r: (r[0], -r[1]))
    return self.length_of_lis(h for w, h in envelopes)

def length_of_lis(nums: List[int]) -> int:
    if not nums:
        return 0
    tails = []
    for num in nums:
        pos = bisect.bisect_left(tails, num)
        if pos == len(tails):
            tails.append(num)
        else:
            tails[pos] = num
    return len(tails)
```

### Run time
Time complexity for sorting is $O(n \log n)$ and for LIS it is $O(n \log n)$. Depending on the implementation, we need $O(n)$ extra space. 

- $T(n) = O(n \log n)$ and $S(n) = O(n)$