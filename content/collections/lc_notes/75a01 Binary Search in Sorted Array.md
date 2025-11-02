---
date: 2024-01-01 00:00:00 +0000
layout: post
slug: 75a01
status: done
tags:
- binary search
title: Binary Search in Sorted Array
---

## Binary search in a sorted array     
```                                   
  [      <      ][ = ][      >      ]                            
```
```python
def binary_search_array(arr: List[int], target: int) -> int:
    left, right = 0, len(arr) - 1
    while left < right:
        mid = left + (right - left) // 2
        if arr[mid] >= target:
            right = mid
        else:
            left = mid + 1
    return left if arr[left] == target else -1
```