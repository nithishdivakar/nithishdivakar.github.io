---
date: 2024-01-01 00:00:00 +0000
layout: post
slug: 84a01
status: done
tags:
- greedy
title: Gas Station
---

## Gas Station [LC#134]
> There are n gas stations along a circular route, where the amount of gas at the `station i` is `gas[i]`. You have a car with an unlimited gas tank and it costs `cost[i]` of gas to travel from the station `i` station to  `(i + 1)`. You begin the journey with an empty tank at one of the gas stations.
> 
> Given two integer arrays gas and cost, return the starting gas station's index if you can travel around the circuit once in the clockwise direction, otherwise return -1. If there exists a solution, it is guaranteed to be unique.

 
### Intuition: Greedy Approach
- Base case: If the total gas is less than the total cost, the circuit is not traversable. Otherwise, there is at least one valid starting point.
- If we had `tank` amount of gas before entering station `i` we can update the state as `tank += (gas[i] - cost[i])`. If we are starting from `i`, we set `tank = 0`.
- We started from j and `tank` becomes negative at i, the segment [j,i] is not traversable starting with an empty tank. Additionally, none of the stations in that segment can be valid starting points as that would also lead to a negative `tank`.
- Therefore, the possible starting point is `i + 1`, and reset `tank` to 0 and re-check. 
- We are guranteed to find a starting point.

### Code

```python
def gas_station_valid_starting_point(gas: List[int], cost: List[int]) -> int:
    if sum(gas) < sum(cost):
        return -1
    tank = 0
    starting_index = 0
    for i in range(len(gas)):
        tank += gas[i] - cost[i]
        if tank < 0:
            tank = 0
            starting_index = i + 1
    return starting_index
```

### Time complexity
- $T(n) = O(n)$ , $S(n) = O(1)$