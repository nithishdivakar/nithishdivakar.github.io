---
date: 2024-01-01 00:00:00 +0000
layout: post
slug: 23a
status: done
tags:
- stack
title: Longest Valid Parentheses
---

## Longest Valid Parentheses [LC32]

Given a string containing just the characters '(' and ')', return the length of the longest valid (well-formed) parentheses 
substring

### Using stack
```python
def longest_valid_parentheses(self, s: str) -> int:
    ans = 0
    stack = [-1]
    for i in range(len(s)):
        if s[i] == "(":
            stack.append(i)
        else:
            stack.pop()
            if stack:
                ans = max(ans, i - stack[-1])
            else:
                stack.append(i)
    return ans
```

### Time Complexity
- $T(n) = O(n)$ and $S(n) = O(n)$

### Using 2 pointers
One of the passes will catch all the longest substring. Check the counter comparison condition and order of the comparisons. 

```python
def longest_valid_parentheses(self, s: str) -> int:
    left, right = 0, 0
    ans = 0
    for c in s:
        if c == '(':
            left += 1
        else:
            right += 1
            
        if right == left:
            ans = max(ans, 2*right)
        elif right > left:
            left = right = 0
    
    left = right = 0
    for c in reversed(s):
        if c == '(':
            left += 1
        else:
            right += 1

        if right == left:
            ans = max(ans, 2*right)
        elif left > right:
            left = right = 0
    return ans
```
### Time Complexity
- $T(n) = O(n)$ and $S(n) = O(1)$