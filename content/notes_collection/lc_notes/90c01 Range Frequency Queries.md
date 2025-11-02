---
date: 2024-01-01 00:00:00 +0000
layout: post
slug: 90c01
status: done
tags: []
title: Range Frequency Queries
---

## Range Frequency Queries [LC#2080]
> Design a data structure to find the frequency of a given value in a given subarray. The frequency of a value in a subarray is the number of occurrences of that value in the subarray.
>
> Implement the RangeFreqQuery class: RangeFreqQuery(int[] arr) Constructs an instance of the class with the given 0-indexed integer array arr. int query(int left, int right, int value) Returns the frequency of value in the subarray arr[left...right]. A subarray is a contiguous sequence of elements within an array. arr[left...right] denotes the subarray that contains the elements of nums between indices left and right (inclusive).

### Intuition

### Code
```python
class RangeFreqQuery:
    def __init__(self, arr: List[int]):
        self.index = defaultdict(list)
        for idx, num in enumerate(arr):
            self.index[num].append(idx)

    def query(self, left: int, right: int, value: int) -> int:
        low = bisect.bisect_left(self.index[value], left)
        high = bisect.bisect_right(self.index[value], right)
        return high - low
```

### Time complexity
- $T(n) = O(\log n)$ for each queries and $T(n) = O(n)$ for preprocessing
- $S(n) = O(n)$ for holding the indexes