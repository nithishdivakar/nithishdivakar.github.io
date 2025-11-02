---
date: 2024-01-01 00:00:00 +0000
layout: post
level: h1
slug: '75'
status: done
title: Binary Search
---

# Binary Search
> Minimize k , s.t. condition(k) is True

```
  [ f ][ f ][ f ][ t ][ t ][ t ][ t ][ t ]     
                   └── ans 
```
- Set up the boundary to include all possible elements

```python
def binary_search(search_space) -> int:
    left, right = min(search_space), max(search_space)
    while left < right:
        mid = left + (right - left) // 2
        if condition(mid):
            right = mid
        else:
            left = mid + 1
    return left
```