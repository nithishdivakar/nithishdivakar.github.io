---
date: 2024-01-01 00:00:00 +0000
layout: post
slug: 23b
status: done
tags:
- stack
title: Valid Parenthesis String
---

## Valid Parenthesis String [LC#678]
> Given a string s containing only three types of characters: `'('`, `')'` and `'*'`, return true if s is valid. The string is valid if it is a valid paranthesised string where any `'*'` could be treated as `'('` or `')'` or empty string. 


### Intuition
- there is a 2 stacks approach where one stack is used to store indices of `'('` and match with the corresponding `')'` while the other maintains indices of `'*'`. 

- The key observation here is to note that either the aesterics can all be left or empty OR right or empty in valid configurations. We count from both sides for either.

### Code
```python
def valid_parenthesis(string: str) -> bool:
    n = len(string)
    open_cnt = 0
    close_cnt = 0
    for left, right in zip(range(n), range(n-1, -1, -1)):

        if string[left] in ["(", "*"]:
            open_cnt += 1
        else:
            open_cnt -= 1

        if string[right] in [")", "*"]:
            close_cnt += 1
        else:
            close_cnt -= 1

        if open_cnt < 0 or close_cnt < 0:
            return False
    return True
```

### Time complexity
- $T(n) = O(n)$ 
- $S(n) = O(1)$