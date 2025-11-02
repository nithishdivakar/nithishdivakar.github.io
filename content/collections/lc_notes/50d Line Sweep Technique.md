---
date: 2024-01-01 00:00:00 +0000
layout: post
level: h2
slug: 50d
status: done
tags:
- line sweep
title: Line Sweep Technique
---

## Line Sweep
This is a technique where we sweep an imaginary line across the whole domain, and the line's intersections with intervals are used to solve problems. They are particularly useful for problems where we have range updates and we need to find the final state of the array.

Say we are given `queries = [(left, right, value),]` implying all values in `[left, right]` are to be incremented by `value`. To quickly find the final value, we can do the following.

```python
def apply_range_updates(queries, n):
    arr = [0]*n
    for left, right, value in queries:
        arr[left] += value
        arr[right] -= value
    prev = 0
    for i in range(n):
        prev+=arr[i]
        arr[i] = prev
    return arr
```

The function `apply_range_updates` takes the list of queries and the size of the array `n`, and returns the final state of the array after applying all the range updates.