---
date: 2024-01-01 00:00:00 +0000
layout: post
slug: 25a
status: done
title: Containers with Most Water
tags:
    - two pointers
---

## Containers with most water [LC#11]
> Given $n$ non-negative integers $a_1$, $a_2$, ... , $a_n$ , where each represents a point at coordinate $(i, a_i)$. $n$ vertical lines are drawn such that the two endpoints of the line $i$ is at $(i, a_i)$ and $(i, 0)$. Find two lines, which, together with the x-axis forms a container, such that the container contains the most water.

**Two pointer approach**
- Given 2 walls, the volume of water between them is limited by the smaller one. So we can move inwards from the smaller wall.
- This can be implemented using a 2 pointer approach closing in from both ends.
- $T(n) = O(n)$
```python
def max_water(height: List[int]) -> int:
    left, right = 0, len(height)-1
    max_area = 0
    while left < right:
        max_area = max(
            max_area, 
            (right - left)*(min(height[left], height[right])) 
        )
        # we have to move away from the smaller wall
        # as it is limiting factor of the area
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1
    return max_area
```