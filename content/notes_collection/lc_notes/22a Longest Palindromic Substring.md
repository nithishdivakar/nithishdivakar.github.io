---
date: 2024-01-01 00:00:00 +0000
layout: post
slug: 22a
status: done
tags:
- palindromes
title: Longest Palindromic Substring
---

## Longest Palindromic Substring [LC#5]
> Given a string s, return the longest  palindromic substring in s.

### Intuition

Expand around Center

### Code
```python
def longestPalindrome(string: str) -> str:
    def expand_around_center(left: int, right: int, string: str) -> str:
        while left >= 0 and right < len(string) and string[left] == string[right]:
            left = left - 1
            right = right + 1
        return string[left + 1 : right]

    longest = ""
    for i in range(len(s)):
        longest = max(
            longest,
            expand_around_center(i, i, string),
            expand_around_center(i, i + 1, string),
            key=len,
        )
    return longest
```
### Time Complexity
- $T(n) = O(n^2)$
- $S(n) = O(1)$