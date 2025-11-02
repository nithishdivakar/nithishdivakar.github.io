---
date: 2024-01-01 00:00:00 +0000
layout: post
slug: 22b
status: done
tags:
- palindromes
title: Count Palindromic Substrings
---

## Count Palindromic Substrings [LC#647]
> Given a string s, return the number of palindromic substrings in it. A string is a palindrome when it reads the same backward as forward. A substring is a contiguous sequence of characters within the string.

### Intuition

Expand around Center

### Code
```python
def count_palindromic_substrings(s: str) -> int:
    def expand_around_center(left: int, right: int) -> int:
        count = 0
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left = left - 1
            right = right + 1
            count = count + 1
        return count

    count = 0
    for i in range(len(s)):
        # odd length palindromes
        count += expand_around_center(i, i)

        # even length palindromes
        count += expand_around_center(i, i + 1)
    return count

def count_palindromic_substrings_faster(s: str) -> int:
    p = manacher(s)
    count = 0
    for length in p:
        if length % 2 == 0:
            count += length // 2
        else:
            count += length // 2 + 1
    return count

def manacher(self, s):
    t = "#".join("^{}$".format(s))
    n = len(t)
    p = [0] * n
    center = right = 0

    for i in range(1, n - 1):
        if i < right:
            p[i] = min(right - i, p[2 * center - i])
        while t[i + p[i] + 1] == t[i - p[i] - 1]:
            p[i] += 1

        if i + p[i] > right:
            center, right = i, i + p[i]

    return p[1:-1]
```
### Time Complexity
- $T(n) = O(n^2)$ $O(n)$ if you use manacher.
- $S(n) = O(1)$