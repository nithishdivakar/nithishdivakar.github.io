---
title: Knapsack
layout: post
tags : [algorithms]
date: 2023-10-20T05:52:32+05:30
draft: false
---


# Knapsack

Knapsack problems are probably the first introduction to many on problems where you are trying to optimize a dimension while constrained by another. Let's look at it in depth.


You are given a metaphorical knapsack which atmost can carry $W$ weight items. You are also given $n$ items, each with its own weight $w_i$ and value $v_i$. We are asked to select a few items from this set so that the total weight is atmost $W$ while maximising the total value. 


If we say $x_i \in \\{0,1\\}$ represents wether item $i$ is selected or not in a possible solution, then the problem is 


$$\begin{align} 
&\max \sum_i x_i v_i 
\\\\
&s.t. \quad \sum_i x_i w_i \leq T
\end{align}$$


There are 3 broad classifications of knapsack problems:

1. Bounded knapsack: We can select an item only once.
2. Unbounded knapsack: We have an infinite copies of each item.
3. Fractional knapsack: We can select a fraction of any item.


What if we have at most $c$ copies of each item. This is trivially reducible to Bounded knapsack  if we assume they are $c$ distinct items which happen to have same weight and value. This reduction applies to any case where the number of copies of each item is finite. For this reason, Bounded knapsack is also called 0/1 knapsack.


## 0/1 knapsack
So we can either select an item or not while maximizing the values.

The solution is quite easy to describe. Try all possible combinations of items; all $2^n$ of them, and see which one is the best. However, we can do better than enumerating all possible combinations by exploiting the [optimal substructure](https://en.wikipedia.org/wiki/Optimal_substructure) of the problem.

Concretely, the impact of choosing or not choosing item $i$ on the solution can be depicted as 

$S(i,w) = \max \{v_i + S(i-1, w-w_i), S(i-1,w)\}$

where $S(i,w)$ represents the maximum value that can be achieved with a maximum weight of $w$ using some subset of the first $i$ items.


```python
def knapsack_01(
    weights: List[int], 
    values: List[int], 
    capacity: int
) -> int:

    max_value = [0 for _ in range(capacity + 1)]
    
    for weight, value in zip(weights, values):
        if weight > capacity:
            continue
        for slack in range(capacity - weight, -1, -1):
            max_value[slack + weight] = max(
                max_value[slack + weight], 
                max_value[slack] + value
            )
    
    return max_value[capacity]

```

This algorithm takes $O(nW)$ time and  $O(W)$ space to run. The time complexity is called sublinear as $W$ can be a bit unbounded. _W = capacity_


## Unbounded knapsack

When we have infinite copies of each items, we have **unbounded knapsack** problem. $x_i > 0$ and $x_i\in \mathbb{Z}$. Let talk about this using an example; the coin change problem. 

### Coin Change
Given a set of coins denomination find the smallest collection of coins that add up to a given amount.


```python
def coin_change(coins: List[int], amount: int) -> int:
    min_coins = [float('inf')] * (amount + 1)
    min_coins[0] = 0
    
    for coin in coins:
        for i in range(coin, amount + 1):
            min_coins[i] = min(min_coins[i], min_coins[i - coin] + 1)
    
    return min_coins[amount] if min_coins[amount] != float('inf') else -1

```


## Fractional Knapsack

The fractional knapsack problem allows us to pick and add a fraction of an item. It is easier to solve than the 0/1 knapsack problem. The solution employs a greedy approach, where we continuously add items based on their value-to-weight ratio until the knapsack's capacity is reached.

```python
def fractional_knapsack(
    values: List[float], 
    weights: List[float], 
    capacity: float
) -> List[float]:

    ratio_sorted = sorted(
        zip(values, weights), 
        key=lambda item: item[0] / item[1], 
        reverse=True
    )

    fractions = [0.0] * len(values)
    current_weight = 0.0

    for i, (value, weight) in enumerate(ratio_sorted):
        if current_weight >= capacity:
            break
        fractions[i] = min(
            (capacity - current_weight) / weight, 
            1.0
        )
        current_weight += weight * fractions[i]

    return fractions
```

Although the algorithm makes only a single pass, it takes $O(n \log n)$ time due to the sorting at the beginning.