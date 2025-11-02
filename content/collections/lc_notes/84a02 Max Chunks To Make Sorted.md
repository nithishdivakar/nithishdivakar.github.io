---
date: 2024-01-01 00:00:00 +0000
layout: post
slug: 84a02
status: done
tags:
- greedy
title: Max Chunks To Make Sorted
---

## Max Chunks To Make Sorted [LC#769]
> You are given an integer array arr of length n that represents a permutation of the integers in the range [0, n - 1]. We split arr into some number of chunks (i.e., partitions), and individually sort each chunk. After concatenating them, the result should equal the sorted array. Return the largest number of chunks we can make to sort the array.

### Intuition
- If we encounter a number k at position i, then $[i, k]$ should be in same chunk for the array to get sorted. 
- So we traverse the array left to right and keep expanding the chunk's right limit as we encounter new number. 
- When we are a number and chunk's limit cannot be expanded beyond the same position, we can start a new chunk. 

### Code
```python
def maximum_chunks(arr: List[int]) -> int:
    right_limit = 0
    count = 0
    for i, num in enumerate(arr):
        right_limit = max(right_limit, num)
        if i >= right_limit:
            count +=1           
    return count
```
### Time complexity
- $T(n) = O(n)$
- $S(n) = O(1)$