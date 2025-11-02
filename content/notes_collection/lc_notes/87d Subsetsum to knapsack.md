---
date: 2024-01-01 00:00:00 +0000
layout: post
slug: 87d
status: done
title: Subsetsum to knapsack
---

## Reducing subset sum to 0/1 knapsack
### Intuition

The Subset Sum problem can be reduced to the 0/1 Knapsack problem by treating the elements of the set as both the weights and values of the items. Given a target sum, we can construct a 0/1 Knapsack with target sum as the capacity and if the the maximum value of the knapsack is equal to the target sum, the selected items form the required subset.

```python
def subset_sum(nums: List[int], target: int) -> bool:
    max_value = knapsack_01(nums, nums, target)
    return max_value == target

def knapsack_01(weights: List[int], values: List[int], capacity: int) -> int:
    max_value = [0] * (capacity + 1)

    for weight, value in zip(weights, values):
        for slack in range(capacity, weight - 1, -1):
            max_value[slack] = max(max_value[slack], max_value[slack - weight] + value)

    return max_value[capacity]
```