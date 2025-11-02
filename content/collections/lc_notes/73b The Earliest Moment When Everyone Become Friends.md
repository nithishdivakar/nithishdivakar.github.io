---
date: 2024-01-01 00:00:00 +0000
layout: post
slug: 73b
status: done
title: The Earliest Moment When Everyone Become Friends
---

## The Earliest Moment When Everyone Become Friends [LC#1101]
> There are n people in a social group labeled from `0` to `n - 1`. You are given an array logs where `logs[i] = [timestampi, xi, yi]` indicates that `xi` and `yi` will be friends at the time timestamp i.
>
> Friendship is symmetric. That means if `a` is friends with `b`, then `b` is friends with `a`. Also, person `a` is acquainted with a person `b` if `a` is friends with `b`, or `a` is a friend of someone acquainted with `b`.
>
> Return the earliest time for which every person became acquainted with every other person. If there is no such earliest time, return `-1`.

### Intuition

Since the friendship is symetric, wheever two people become friends, we can merge their acquaintance sets togethere. When there is only 1 such sets, everyone is aquainted. For finding earliest time, we simply go through the logs in chronological order. 

### Code

```python
def earliestAcq(self, logs: List[List[int]], n: int) -> int:
    dsu = DSU()
    for i in range(n):
        dsu.find(i)
    for timestamp, x, y in sorted(logs):
        if dsu.union(x, y):
            if dsu.components == 1:
                return timestamp
    return -1
```

### Time Complexity

- $T(n) = O(n)$ since union is $O(\alpha(n))$. $S(n) = O(n)$