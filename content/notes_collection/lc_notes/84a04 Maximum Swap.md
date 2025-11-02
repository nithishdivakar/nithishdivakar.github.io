---
date: 2024-01-01 00:00:00 +0000
layout: post
slug: 84a04
status: done
tags: []
title: Maximum Swap
---

## Maximum Swap [LC#670]
> You are given an integer num. You can swap two digits at most once to get the maximum valued number. Return the maximum valued number you can get.

### Intuition
The possible pairs which can be swapped to increase the value of the numbers are such that larger number follows smaller number. The optimum pair among those are the ones where the larger number is most to the left.

### Code
```python
def maximum_swap(num: int) -> int:
    digits = list(str(num))
    n = len(digits)
    max_pos = n - 1
    left, right = n, n
    for i in range(n - 1, -1, -1):
        if digits[i] > digits[max_pos]:
            max_pos = i

        if digits[i] < digits[max_pos]:
            left = i
            right = max_pos

    if left == n or right == n:
        return num
    digits[left], digits[right] = digits[right], digits[left]
    return int("".join(digits))
```

### Time complexity
- $T(n) = O(n)$ 
- $S(n) = O(1)$