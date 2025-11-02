---
date: 2024-01-01 00:00:00 +0000
layout: post
slug: 80c
status: done
tags:
- string
- dp
title: Interleaving String
---

## Interleaving String [LC#97]
> Given strings `u`, `v`, and `t`, find whether `t` can formed by an interleaving of `u` and `v`.

### Intuition
- Dynamic Prgraming

### Code
```python
from functools import cache

def isInterleave(u: str, v: str, t: str) -> bool:
    m, n, k = len(u), len(v), len(t)
    if m + n != t: return False
    
    @cache
    def memo(i, j, k):
        if k == 0:
            return i == 0 and j == 0

        if i > 0 and u[i - 1] == t[k - 1] and memo(i - 1, j, k - 1):
            return True
        if j > 0 and v[j - 1] == t[k - 1] and memo(i, j - 1, k - 1):
            return True

        return False

    return memo(m, n, k)
```

### Time complexity
- $T(n) = O(mn)$ 
- $S(n) = O(mn)$ but optimised to $O(\min\\{m,n\\})$