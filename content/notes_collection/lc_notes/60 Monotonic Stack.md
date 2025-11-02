---
categories: array stack
date: 2024-01-01 00:00:00 +0000
layout: post
level: h1
slug: '60'
status: done
tags:
- monotonic stack
title: Monotonic Stack
---

## Monotonic Stack

A monotonic decreasing stack is a data structure based on a stack. While traversing an array, it maintains a sorted list of elements encountered so far that are strictly greater than or equal to the current element being processed. It upholds this property by continuously removing elements from the top of the stack that violate the requirement (i.e., elements that are less than the current element).

```python
stack = []
for num in nums:
    while stack and stack[-1] <= num:
        stack.pop()
    stack.append(num)
    # stack[-1] > stack[-2] > ... > stack[0]
```

Although a monotonic stack can be used to solve problems that require finding previous smaller (or larger) elements from the stack, a more interesting use is to exploit the interim states of the monotonic stack while it updates itself to maintain the property of monotonicity. Ex.

```python
stack = []
arr.append(-math.inf) # to ensure all elements are processed
for idx range(len(arr)):
    while stack and arr[stack[-1]] <= arr[idx]:
        mid = stack.pop()
        left = -1 if not stack else stack[-1]
        right = idx
        # do something with arr[left] > a[mid] < a[right]
    stack.append(idx)
```

References 
- https://labuladong.gitbook.io/algo-en/ii.-data-structure/monotonicstack
- https://leetcode.com/discuss/study-guide/2347639/A-comprehensive-guide-and-template-for-monotonic-stack-based-problems