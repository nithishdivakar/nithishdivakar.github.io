---
date: 2024-01-01 00:00:00 +0000
layout: post
slug: 14b02
status: done
tags: []
title: Best Time to Buy and Sell Stock IV
---

## Best Time to Buy and Sell Stock IV [LC#188]
> You are given an integer array prices where prices[i] is the price of a given stock on the ith day, and an integer k. Find the maximum profit you can achieve. You may complete at most k transactions: i.e. you may buy at most k times and sell at most k times. Note: You may not engage in multiple transactions simultaneously (i.e., you must sell the stock before you buy again).

### Intuition
- `f[k][i]` denotes maximum profit obtainable by doing k transactions with first i prices.
- The dp equation is 
    ```
    f[k][i] = max(
        f[k][i-1], 
        max( prices[i] - prices[j] + f[k-1, j] for i in [0, i-1] )
    )
    = max(
        f[k][i-1], 
        prices[i] + max( f[k-1, j] - prices[j] +  for i in [0, i-1] )
    )
    ```
- Also, `f[k][0] = 0` and `f[0][i] = 0`
- The inner max can be maintained as a running maximum.

### Code
```python
def max_profit_with_k_transactions(K: int, prices: List[int]) -> int:
    n = len(prices)
    f = [[0] * (n) for _ in range(K + 1)]
    max_profit = 0
    for k in range(1, K + 1):
        t = f[k - 1][0] - prices[0]
        for i in range(1, n):
            t = max(t, f[k - 1][i] - prices[i])
            f[k][i] = max(f[k][i - 1], prices[i] + t)
            max_profit = max(max_profit, f[k][i])
    return max_profit
```

### Time complexity
- $T(n) = O(nk)$ 
- $S(n) = O(n)$ Currently $O(nk)$ but can be optimised to use only two array of storage. The algorithm can also be modified to use only $O(k)$ storage.