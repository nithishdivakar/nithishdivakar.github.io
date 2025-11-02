---
date: 2024-01-01 00:00:00 +0000
layout: post
slug: 01c01
status: done
title: Quick Sort
---

## Quick Select
### Partition Scheme intuition.
- Select the last element in the array as pivot.
- Maintain 2 pointer, `left` and `right`. 
- Traverse the array updating both pointers such that the values in  `[left, right]` is always `>` the pivot.

```python
#  [ ≤ ][ ≤ ][ > ][ > ][ > ][ > ][ ? ][ hi ]     
#              └─ left        └─ right 

def lomuto_partition(A, lo, hi):
    pivot = A[hi]
    left = lo
    for right in range(lo,  hi): 
        if A[right] <= pivot:
            A[left], A[right] = A[right], A[left]
            left = left + 1
    A[left], A[hi] = A[hi], A[left]
    return left
```

### Quick sort using the partition scheme
```python
def quicksort(A, lo, hi):
    if lo >=hi or lo <0:
        return 
    p = lomuto_partition(A, lo, hi)
    quicksort(A, lo, p - 1)
    quicksort(A, p + 1, hi)
```