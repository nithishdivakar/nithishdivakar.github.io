---
date: 2024-01-01 00:00:00 +0000
layout: post
slug: 50c
status: done
tags:
- intervals
- greedy
title: Min Meeting Rooms
---

## Min meeting rooms [LC#253]
>  Meeting Rooms II :
> Given an array of meeting time intervals intervals where intervals[i] = [starti, endi], return the minimum number of conference rooms required.


### Intuition

- Sort all meetings by their start time
- Keep the ending times of currently occupied meeting rooms in the min heap
- If current start time is earlier than the min heap end time, we need a new room else we can pop the top and add a new room

### Code

```python
def min_meeting_rooms(intervals: List[List[int]]) -> int:
    intervals = sorted(intervals)
    heap = [intervals[0][1]]  # first end time
    meeting_rooms = 1
    for start_time, end_time in intervals[1:]:
        if start_time >= heap[0]:
            heapq.heappop(heap)
        heapq.heappush(heap, end_time)
        meeting_rooms = max(meeting_rooms, len(heap))
    return meeting_rooms
```
### Time Complexity
- $T(n)  = O(n \log n + n \log n)$ sorting + n pops
- $S(n) = O(n)$