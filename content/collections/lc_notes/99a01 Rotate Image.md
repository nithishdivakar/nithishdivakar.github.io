---
date: 2024-01-01 00:00:00 +0000
layout: post
slug: 99a01
status: done
tags: []
title: Rotate Image
---

## Rotate Image [LC#48]
> You are given an n x n 2D matrix representing an image, rotate the image by 90 degrees (clockwise). You have to rotate the image in-place, which means you have to modify the input 2D matrix directly. DO NOT allocate another 2D matrix and do the rotation.

### Intuition
90 degree Rotation clockwise = tranpose + reflect

### Code
```python
def rotate(matrix: List[List[int]]) -> None:
    n = len(matrix)

    # tranpose
    for i in range(n):
        for j in range(i+1, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]

    # reflect
    for i in range(n):
        for j in range(n//2):
            matrix[i][j], matrix[i][n-j-1] = matrix[i][n-j-1], matrix[i][j]
```

### Time complexity
- $T(n) = O(n)$
- $S(n) = O(1)$