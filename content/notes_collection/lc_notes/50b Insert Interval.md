---
date: 2024-01-01 00:00:00 +0000
layout: post
slug: 50b
status: done
tags:
- intervals
title: Insert Interval
---

## Insert Interval [LC#57]
> You are given an array of non-overlapping intervals intervals where intervals[i] = [starti, endi] represent the start and the end of the ith interval and intervals is sorted in ascending order by starti. You are also given an interval newInterval = [start, end] that represents the start and end of another interval.
>
> Insert newInterval into intervals such that intervals is still sorted in ascending order by starti and intervals still does not have any overlapping intervals (merge overlapping intervals if necessary).
>
> Return intervals after the insertion.
>
> Note that you don't need to modify intervals in-place. You can make a new array and return it.


### Intuition
Since the intervals are sorted by start time, when we loop through them in order, we will encounter 3 cases
1. The interval ends before the new interval
2. The interval overlaps with the new interval
3. The interval starts after the new interval

We handle each of the 3 cases separately

### Code
```python
@dataclass
class Interval:
    start: float
    end: float
    
def insert_interval(intervals: List[Interval], new: Interval) -> List[Interval]:
    ans = []
    for curr in intervals:
        if curr.end < new.start: # ends before
            ans.append(curr)
        elif curr.start > new.end: # begins after
            if new:
                ans.append(new)
                new = None
            ans.append(curr)
        else: # overlap
            new = Interval(
                min(curr.start, new.start), max(curr.end, new.end)
            )
    if new: # handle when intervals are empty
        ans.append(new)
    return ans
```

### Time Complexity
- $T(n) = O(n)$