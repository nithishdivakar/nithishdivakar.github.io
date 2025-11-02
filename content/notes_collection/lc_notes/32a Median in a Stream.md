---
date: 2024-01-01 00:00:00 +0000
layout: post
slug: 32a
status: done
title: Median in a Stream
tags:
- heap
---

## Find Median from Data Stream [LC#295]
> The median is the middle value in an ordered integer list. If the size of the list is even, there is no middle value, and the median is the mean of the two middle values.
> - For example, for arr = [2,3,4], the median is 3.
> - For example, for arr = [2,3], the median is (2 + 3) / 2 = 2.5.

### Intuition
- We can easily find median if we have access to the 2 middle elements. 
- The middle elements are largest of the first half and smallest of the second half if the array was sorted
- We can maintain first half of elements in a max heap and second half in min heap
- Always maintain insertion so that max heap has at most 1 value more than the min heap

### Code
```python
class MedianFinder:
    def __init__(self):
        self.low = [] # stores n or n+1 elements
        self.high = [] # stores n elements

    def add(self, num: int) -> None:
        val = heapq.heappushpop(self.low, -num)
        heapq.heappush(self.high, -val)
        if len(self.low) <  len(self.high):
            val = heapq.heappop(self.high)
            heapq.heappush(self.low, -val)

    def find_median(self) -> float:
        if len(self.low) > len(self.high):
            return -self.low[0]
        return (-self.low[0] + self.high[0])/2
```

### Time complexity
- $T(n) = O(\log n) $ for each insertion and median can be computed in $O(1)$ always
- $S(n) = O(n)$ for the heaps