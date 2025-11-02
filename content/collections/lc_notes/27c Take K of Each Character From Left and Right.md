---
date: 2024-01-01 00:00:00 +0000
layout: post
slug: 27c
status: done
title: Take K of Each Character From Left and Right
tags:
- sliding window
---

## Take K of Each Character From Left and Right [LC#2516]
> You are given a string s consisting of the characters 'a', 'b', and 'c' and a non-negative integer k. Each minute, you may take either the leftmost character of s, or the rightmost character of s. Return the minimum number of minutes needed for you to take at least k of each character, or return -1 if it is not possible to take k of each character.


### Intuition
We are looking for a largest window that can be removed without making count of all characters going below `k`

### Code
```python
def take_characters(s: str, k: int) -> int:
    if k == 0 : return 0 
    count = Counter({"a": 0, "b": 0, "c": 0})
    for char in s:
        count[char] += 1

    if min(count.values()) < k:
        return -1

    max_window = 0
    left = 0
    for right in range(len(s)):
        count[s[right]] -= 1
        while left <= right and min(count.values()) < k:
            count[s[left]] += 1
            left += 1
        max_window = max(max_window, right - left + 1)
    return len(s) - max_window
```

### Time complexity
- $T(n) = O(n)$
- $S(n) = O(|characters|)$