---
date: 2024-01-01 00:00:00 +0000
layout: post
slug: 22c
status: doing
tags:
- palindromes
title: Manacher Algorithm
---

## Manacher Algorithm

All palindromes in $O(1)$

```python
def manacher(s: str):
    t = '#'.join('^{}$'.format(s))
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