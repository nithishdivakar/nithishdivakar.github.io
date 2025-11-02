---
date: 2024-01-01 00:00:00 +0000
slug: '23c'
layout: post
status: done
title: Minimum Add to Make Parentheses Valid
tags: []
---

## Minimum Add to Make Parentheses Valid [LC#921]
> You are given a parentheses string `s`. In one move, you can insert a parenthesis at any position of the string. For example, if `s = "()))"`, you can insert an opening parenthesis to be `"(()))"` or a closing parenthesis to be `"())))"`.
Return the minimum number of moves required to make `s` valid.

### Intuition

### Code
```python
def make_valid(s: str) -> int:
    stack = []
    insert_count = 0
    for char in s:
        if char =='(':
            stack.append(char)
        if char == ')':
            if stack:
                stack.pop()
            else:
                insert_count +=1
    insert_count += len(stack)
    return insert_count

def make_valid(self, s: str) -> int:
    insert_count = 0
    open_count = 0
    for char in s:
        if char =='(':
            open_count+=1
        if char == ')':
            if open_count>0:
                open_count-=1
            else:
                insert_count +=1
    insert_count += open_count
    return insert_count
```

### Time complexity
- $T(n) = O(n)$ 
- $S(n) = O(1)$. If using stack then $O(n)$.
