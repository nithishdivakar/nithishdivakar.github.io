---
categories: array stack
date: 2024-01-01 00:00:00 +0000
layout: post
slug: 60a
status: done
tags:
- monotonic stack
title: Largest Rectangle in Histogram
---

## Largest Rectangle in Histogram [ LC# 84]
Given an array of integers heights representing the histogram's bar height where the width of each bar is 1, return the area of the largest rectangle in the histogram.

### Brute Force
- Enumerate every range. Compute the Area
- $T(n) = O(n^2)$; $S(n) = O(n^2)$

```python
area[i][j] = min_heights[i:j] * ( j-i+1 )
min_heights[i:j] = min(min_heights[i-1:j-1], heights[i], heights[j])
min_heights[i:i] = heights[i]
```

### Intuition: Monotonic Stack
- If we are at a rectangle of height $h$ and we are interested in finding the largest rectangle with minimum height $h$ in the histogram. We can extend the rectangle to both the sides till we encounter a height that is smaller.
- If we trasverse the histogram from left to right and maintain a non-decreasing monotonic stack, it will have all these states that we need.

```              
           ┌─┐         ┌─┐    
       ┌─┐ │ │       ┌─┤ │    
   ┌─┐ │ ├─┤ │     ┌─┤ │ │    
   │ ├─┤ │ │ │   ┌─┤ │ │ │    
   │ │ │ │ │ │...│h│ │ │ ├─┐   
 ┌─┤ │ │ │ │ │   │ │ │ │ │ │   
 └─┴─┴─┴─┴─┴─┘   └─┴─┴─┴─┴─┘   
   └─────────────────────┘                
┌─┴──┐          ┌─┴─┐  ┌──┴──┐
 left            mid    right
```          

### Code
```python
def largest_rectangle_in_historgam(heights: List[int]) -> int:
    stack = [-1] # monotonic stack : non decreasing order
    max_area = 0
    
    heights.append(0)
    for i in range(len(heights)):
        while stack and heights[stack[-1]] > heights[i]:
            mid = stack.pop()
            left = stack[-1] + 1
            right = i
            max_area = max(max_area,  heights[mid] * (right - left))
        stack.append(i)
    return max_area
```


### Time complexity
- $T(n) = O(n)$; $S(n) = O(n)$