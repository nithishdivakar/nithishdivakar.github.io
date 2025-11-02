---
date: 2024-01-01 00:00:00 +0000
layout: post
slug: 14b
status: done
tags:
- greedy
title: Best Time to Buy and Sell Stock
---

## Best Time to Buy and Sell Stock [LC#121] 
> You are given an array prices where `prices[i]` is the price of a given stock on the ith day. You want to maximize your profit by choosing a single day to buy one stock and choosing a different day in the future to sell that stock. Return the maximum profit you can achieve from this transaction. If you cannot achieve any profit, return 0.

### Inutition
- The solution is a variation of Kadane's algorithm. 
- Keep track of minimum seen so far. 
- Max profit if we sell now can be computed with this minimum.
- Keep track of max profit.

### Code
```python
def max_profit(prices: List[int]) -> int:
    max_profit = 0
    min_price = prices[0]
    for price in prices:
        min_price = min(min_price, price)
        max_profit = max(max_profit, price - min_price)
    return max_profit
```

### Time Complexity
- $T(n) = O(n)$ and $S(n) = O(1)$