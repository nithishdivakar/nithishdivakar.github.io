---
date: 2024-01-01 00:00:00 +0000
layout: post
slug: 16a
status: done
tags: [stack]
title: Asteroid Collision
---

## Asteroid Collision [LC#735]
> We are given an array asteroids of integers representing asteroids in a row. The indices of the asteriod in the array represent their relative position in space. For each asteroid, the absolute value represents its size, and the sign represents its direction (positive meaning right, negative meaning left). Each asteroid moves at the same speed.
> 
> Find out the state of the asteroids after all collisions. If two asteroids meet, the smaller one will explode. If both are the same size, both will explode. Two asteroids moving in the same direction will never meet.

### Intuition

### Code
```python
def asteroid_collision(asteroids: List[int]) -> List[int]:
    stack = []

    for asteroid in asteroids:
        store = True
        while stack and stack[-1] > 0 and asteroid < 0:
            # there is collision
            if abs(stack[-1]) < abs(asteroid):
                stack.pop()
                continue                
            elif abs(stack[-1]) == abs(asteroid):
                stack.pop()
                store = False
                break
            else:
                store = False
                break
        if store:
            stack.append(asteroid)
    return stack
```
### Time complexity
- $T(n) = O(n)$
- $S(n) = O(n)$