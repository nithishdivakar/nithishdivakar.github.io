---
date: 2024-01-01 00:00:00 +0000
layout: post
slug: 20a
status: done
title: Longest Consecutive Sequence
---

## Longest Consecutive Sequence [LC#128]
> Given an unsorted array of integers nums, return the length of the longest consecutive elements sequence.

**Brute Force**
- Consider each element as seed. 
- Check if next element in the sequece is in the list. keep track of sequence length
- $T(n) = O(n^3)$; $S(n) = O(1)$

**Sorting**
- Sort the array.
- Check the length of longest conseqtive sequence
- $T(n) = O(n \log n)$; $S(n) = O(n)$

**Hash Table based look up**
- For each num, if num-1 is not in the list, then its possibly a sequence's begning
- For each sequence begning, check if conseqtive elements are in the list
- Each valid sequence is tested once
- $T(n) = O(n)$
- $S(n) = O(n)$
```python
def longest_consecutive_sequence(nums: List[int]) -> int:
    entries = set(nums)
    best = 0
    for num in nums:
        if num-1 not in entries:
            next_num, seq_len = num+1, 1
            while next_num in entries: 
                next_num += 1
                seq_len += 1
            best = max(best, seq_len)
    return best
```