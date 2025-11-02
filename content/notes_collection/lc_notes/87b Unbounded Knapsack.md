---
date: 2024-01-01 00:00:00 +0000
layout: post
slug: 87b
status: done
title: Unbounded Knapsack
---

## Unbounded Knapsack
Unbounded knpasack is when we have infinite number of each items. 

```python
def unbounded_knapsack(weights: List[int], values: List[int], capacity: int) -> int:
    max_value = [0] * (capacity + 1)
    for i in range(1, capacity + 1):
        for j in range(len(weights)):
            if weights[j] <= i:
                max_value[i] = max(
                    max_value[i], 
                    max_value[i - weights[j]] + values[j]
                )
    return max_value[capacity]
```