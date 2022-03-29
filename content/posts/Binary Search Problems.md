---
title: Binary Search
tags : [algorithms]
date: 2022-01-28T06:59:51+05:30
---


# Binary Search

Binary search is more than just a search algorithm for sorted arrays. It's an algorithm which keeps showing up as optimal solutions in unlikely places. This note is a very limited exploration of what binary search can do. 

Let's begin by talking about vanilla binary search. 

## Binary Search

We are given a sorted array of numbers and a target. Binary search is the most optimal way of finding position of target in the array if present. 

Binary search starts by having the entire array as a search space. It then progressively compares the middle element with the target, eliminating half pf search space as not needing further exploration w.r.to the relativeness of target and middle element. 

```python
def binary_search(nums, target):
    low, high = 0, len(nums)
    while low < high:
        mid = low + (high-low)//2
        if nums[mid] == target:
            return mid

        if nums[mid] < target:
            low = mid+1
        else:
            high = mid
    return -1
```


The basic structure of binary search can be used to solve many other seemingly different problems. A one line abstraction of such problems is

>Find a lowest value in a range which is feasible

Lets describe the  search in sorted array problem in this framework. 

Instead of trying to find the location of target, let us recast the problem as the smallest index in the  which contains elements which are larger than or equal to target. Note that this is no  longer solving the search problem exactly. The difference in when target is not present in the array. 

In this description, an index in the array is feasible if the element at the index is larger than or equal to target


```python
def feasible(index, nums, target):
    return (nums[index]>=target)
    
def binary_search(nums, target):
    low, high = 0, len(nums)
    while low < high:
        mid = low + (high-low)//2
        if feasible(mid, nums, target):
            high = mid
        else
            low = mid+1
    return low
```

This template can be quickly extended to solve a few other problems. 

## Split array largest sum
Given an array which consists of non-negative integers, split array into M non-empty  contiguous sub-arrays such that the largest  sum of the segments is minimum.

```python
def feasible(threshold, M) -> bool:
    count, total = 1, 0
    for num in nums:
        total += num
        if total > threshold:
            total = num
            count += 1
            if count > M:
                return False
    return True

def binary_search(nums) -> int:
    low, high = max(nums), sum(nums)
    while low < high:
        mid = low + (high - low)//2
        if feasible(mid, M):
            high = mid
        else:
            low = mid + 1
    return low
```

Now lets look at another problem with similar structure. 


## Median in a row wise sorted Matrix
```python
def binary_median(A):
    m, n  = len(A),len(A[0])        
    low  = min(A[i][ 0] for i in range(m))
    high = max(A[i][-1] for i in range(m))
    median_loc = (m * n + 1) // 2

    while low < high:
        mid = low + (high - low) // 2
        count = 0
        for i in range(m):
            count += upper_bound(A[i], mid)
        if count < median_loc:
            low = mid + 1
        else:
            high = mid
    return high # is median
```



## Square root of a number
Binary search can also used to find roots of an equations. Let us demonstrate how it is used to find square root of a number. 

```python
def square_root(x, tolerance=1e-4):
    low, high = 0,x
    while (high-low) > tolerance:
        mid = low + (high - low)/2.0
        if mid * mid <= x:
            low = mid
        else:
            high = mid
    return low
```


## Find Minimum in Rotated Sorted Array With No Duplicates

\url{https://www.topcoder.com/thrive/articles/Binary%20Search}


## Median of 2 sorted arrays
```python
class Solution:
    def findMedianSortedArrays(self, A: List[int], B: List[int]) -> float:
        m, n = len(A), len(B)
        length, mid = (m+n+1), (m+n+1)//2
        m1 = self.find_kth(A,B, mid)
        m2 = self.find_kth(A,B, length - mid)
        return (m1+m2)/2.0
        
    def find_kth(self, A, B, k):
        if not A: return B[k-1]
        if not B: return A[k-1]
        
        lo, hi = min(A[0], B[0]), max(A[-1], B[-1])
        
        while lo < hi:
            mid = lo + (hi - lo)//2
            a_md = bisect.bisect_right(A, mid)
            b_md = bisect.bisect_right(B, mid)
            
            if a_md + b_md < k:
                lo = mid + 1
            else:
                hi = mid
        return hi
```

