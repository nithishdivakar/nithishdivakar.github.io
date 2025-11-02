---
date: 2024-01-01 00:00:00 +0000
layout: post
slug: 50e
status: done
tags:
- intervals
- greedy
title: Minimum Number of Arrows to Burst Balloons
---

## Minimum Number of Arrows to Burst Balloons [LC#452]
> There are some spherical balloons taped onto a flat wall that represents the XY-plane. The balloons are represented as a 2D integer array points where points[i] = [xstart, xend] denotes a balloon whose horizontal diameter stretches between xstart and xend. You do not know the exact y-coordinates of the balloons.
> 
> Arrows can be shot up directly vertically (in the positive y-direction) from different points along the x-axis. A balloon with xstart and xend is burst by an arrow shot at x if xstart <= x <= xend. There is no limit to the number of arrows that can be shot. A shot arrow keeps traveling up infinitely, bursting any balloons in its path.
>  
> Given the array points, return the minimum number of arrows that must be shot to burst all balloons.
 
### Intuition: Greedy Approach
- This problem is about find min vertical lines intersecting a given set of intervals. 
- We pick an interval as a root interval. Any interval intersecting with this one can all be taken out by a single arrow. 
- To find minimum such sets, we sort the interval by ending time, pick first interval as root, and find the intesecting intervals to it by checking the ones whose start time is earlier.
- Iteratively we can find all such combinations. 

### Code

```python
def min_arrows(balloons: List[List[int]]) -> int:
    if not balloons:
        return 0
    balloons.sort(key = lambda r: r[1])
    end_location = balloons[0][1]
    num_arrows = 1
    for balloon in balloons:
        if balloon[0] > end_location:
            end_location = balloon[1]
            num_arrows +=1
    return num_arrows
```

### Time complexity
Time complexity is domniated by sorting. $T(n) = O(n \log n) + O(n)$ , $S(n) = O(1)$