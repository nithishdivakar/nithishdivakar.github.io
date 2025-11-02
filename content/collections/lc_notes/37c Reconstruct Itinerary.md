---
date: 2024-01-01 00:00:00 +0000
layout: post
slug: 37c
status: done
tags:
- eulerian path
- dfs
title: Reconstruct Itinerary
---

## Reconstruct Itinerary [LC#332]
> You are given a list of airline tickets where tickets[i] = [fromi, toi] represent the departure and the arrival airports of one flight. Reconstruct the itinerary in order and return it. All of the tickets belong to a man who departs from "JFK", thus, the itinerary must begin with "JFK". If there are multiple valid itineraries, you should return the itinerary that has the smallest lexical order when read as a single string. For example, the itinerary ["JFK", "LGA"] has a smaller lexical order than ["JFK", "LGB"]. You may assume all tickets form at least one valid itinerary. You must use all the tickets once and only once.

### Intuition
- Eulerian Path , greedy DFS

### Code
```python
def reconstruct_iternary(tickets: List[List[str]]) -> List[str]:
    # Eulerian Path , greedy DFS
    graph = defaultdict(list)
    for frm, to in sorted(tickets)[::-1]:
        graph[frm].append(to)

    stack = ["JFK"]
    ans = []
    while stack:
        while graph[stack[-1]]:
            neigh = graph[stack[-1]].pop()
            stack.append(neigh)
        node = stack.pop()
        ans.append(node)        
    return ans[::-1]
```

### Time complexity
- $T(n) = O(E)$ 
- $S(n) = O(E)$