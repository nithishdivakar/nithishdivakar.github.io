---
date: 2024-01-01 00:00:00 +0000
layout: post
slug: 87a
status: done
title: Bounded Knapsack
---

## Bounded Knapsack
Bounded knapsack is when we have $n$ items $[(w_i, v_i, n_i)]$ representing weight,  value and copies available of each item. This is tribvially reducible to 0/1 knapsack if we simply assume that there are $n_i$ number of distinct items with same weight and value for each of the original item. The time complexity would then be $O(sum(n_i)\times sum(w_i n_i))$. 

```python
def knapsack_01(weights: List[int], values: List[int], capacity: int) -> int:
    max_value = [0] * (capacity + 1)

    for weight, value in zip(weights, values):
        for slack in range(capacity, weight - 1, -1):
            max_value[slack] = max(
                max_value[slack], 
                max_value[slack - weight] + value
            )

    return max_value[capacity]
```

There is a slightly better way to do the reduction. create logaritmic number of copies of items with 1,2,4,.. times weight, value of each item and solve as a 0/1 knapsack problem. Any number of selection of copies of original problem can be represented by a specific selection of new items. Time complexity is $O(sum(w_i) \times n \times \log (\max n_i))$. [Ref](https://blog.mitrichev.ch/2011/07/integral-bounded-knapsack-problem.html)