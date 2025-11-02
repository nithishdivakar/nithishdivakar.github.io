---
date: 2024-01-01 00:00:00 +0000
layout: post
slug: 80d
status: done
tags:
- string
- sub sequence
- dp
title: Distinct Subsequences
---

## Distinct Subsequences [LC#115]
> Given two strings `s` and `t`, return the number of distinct subsequences of `s` which equals `t`.

### Intuition

### Code
```python
def count_distinct_subsequences(s: str, t: str) -> int:
    m = len(s) 
    n = len(t)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    dp[0][0] = 1

    for i in range(1, m + 1):
        dp[i][0] = 1
        for j in range(1, n + 1):
            dp[i][j] = dp[i - 1][j]
            if s[i - 1] == t[j - 1]:
                dp[i][j] += dp[i - 1][j - 1]
    return dp[m][n]

def count_distinct_subsequences_space_optimised(s: str, t: str) -> int:
    m = len(s)  
    n = len(t)  
    dp = {0: [0] * (n + 1), 1:[0] * (n + 1)}

    dp[0][0] = 1

    for i in range(1, m + 1):
        dp[i%2][0] = 1
        for j in range(1, n + 1):
            dp[i%2][j] = dp[(i - 1)%2][j]
            if s[i - 1] == t[j - 1]:
                dp[i%2][j] += dp[(i - 1)%2][j - 1]
    return dp[m%2][n]
```

### Time complexity
- $T(n) = O(mn)$ 
- $S(n) = O(mn)$ but optimised to $O(\min\\{m,n\\})$