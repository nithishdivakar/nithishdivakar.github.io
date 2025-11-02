---
categories: array stack
date: 2024-01-01 00:00:00 +0000
layout: post
slug: 60c
status: done
tags:
- monotonic stack
title: Daily Temperatures
---

## Daily Temperatures [LC#739]

> Given an array of integers temperatures represents the daily temperatures, return an array answer such that `answer[i]` is the number of days you have to wait after the ith day to get a warmer temperature. If there is no future day for which this is possible, keep `answer[i] == 0` instead.

### Intuition
We have to fine the next largest in the array for every element.


### Code

```python
def next_warmer_day(temperatures: List[int]) -> List[int]:
    n = len(temperatures)
    stack = []
    answers = [0] * n
    for i in range(n - 1, -1, -1):
        while stack and temperatures[stack[-1]] <= temperatures[i]:
            stack.pop()
        if stack:
            answers[i] = stack[-1] - i
        stack.append(i)
    return answers

OR

def next_warmer_day(temperatures: List[int]) -> List[int]:
    n = len(temperatures)
    stack = []
    answers = [0] * n
    for curr_day in range(n):
        while stack and temperatures[stack[-1]] < temperatures[curr_day]:
            prev_day = stack.pop()
            answers[prev_day] = curr_day - prev_day
        stack.append(curr_day)
    return answers
```
_Note the different comparison signs between 2 implementation_

### Time Complexity
- $T(n) = O(n)$ ; $S(n) = O(n)$