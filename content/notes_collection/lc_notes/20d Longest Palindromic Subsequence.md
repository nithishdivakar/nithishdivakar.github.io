---
date: 2024-01-01 00:00:00 +0000
layout: post
slug: 20d
status: done
title: Longest Palindromic Subsequence
---

## Longest Palindromic Subsequence [LC#516]
> Given a string `s`, find the longest palindromic subsequence's length in `s`. A subsequence is a sequence that can be derived from another sequence by deleting some or no elements without changing the order of the remaining elements.

 

### Intuition

If the characters at the both ends of the string sre the same, they must be part of the longest palindrome. We can add 2 to the length and remove those characters. If they are not equal, then the longest palindrome would be in either of the arrays with one of the end characters removed. 

**Dynamic Programming**
```python
def longest_palindrommic_subsequence(s: str) -> int:
    @cache
    def longest(i, j):
        if i == j:
            return 1
        if i > j:
            return 0
        if s[i] == s[j]:
            return 2 + longest(i + 1, j - 1)
        else:
            return max(longest(i + 1, j), longest(i, j - 1))
    return longest(0, len(s) - 1)
```

### Time Complexity

- $T(n) = O(n^2)$ and $S(n) = O(n^2)$



**Dynamic Programming with space optimisation**
```python
def longest_palindromic_subsequence(s: str) -> int:
    n = len(s)
    curr_dp, prev_dp = [0] * n, [0] * n

    for i in range(n - 1, -1, -1):
        curr_dp[i] = 1
        for j in range(i + 1, n):
            if s[i] == s[j]:
                curr_dp[j] = prev_dp[j - 1] + 2
            else:
                curr_dp[j] = max(prev_dp[j], curr_dp[j - 1])
        prev_dp = curr_dp[:]

    return curr_dp[n - 1]
```

### Time Complexity

- $T(n) = O(n^2)$ and $S(n) = O(n)$