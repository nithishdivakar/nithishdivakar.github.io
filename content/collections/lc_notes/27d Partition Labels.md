---
date: 2024-01-01 00:00:00 +0000
layout: post
slug: 27d
status: done
tags:
- sliding window
title: Partition Labels
---

## Partition Labels [LC#763]
> You are given a string s. We want to partition the string into as many parts as possible so that each letter appears in at most one part. Note that the partition is done so that after concatenating all the parts in order, the resultant string should be s. Return a list of integers representing the size of these parts.

### Intuition
- While iterating through the string, if we know the last position of each character, we can keep extending the span of sting to include to safely include c. 
- If the span and the current index coincide, then the string can be partitioned at the current index.

### Code
```python
def partition_string(string: str) -> List[int]:
    last_pos = defaultdict(int)
    for i, char in enumerate(string):
        last_pos[char] = i

    left = 0
    right = 0
    lengths = []
    for i, char in enumerate(string):
        right = max(right, last_pos[char])
        if right == i:
            lengths.append(right - left + 1)
            left = i + 1
    return lengths
```

### Time complexity
- $T(n) = O(n)$ 
- $S(n) = O(|c|)$