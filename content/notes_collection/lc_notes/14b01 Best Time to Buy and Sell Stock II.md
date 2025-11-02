---
date: 2024-01-01 00:00:00 +0000
layout: post
slug: 14b01
status: done
tags:
- greedy
title: Best Time to Buy and Sell Stock II
---

## Best Time to Buy and Sell Stock II [LC#122]
> You are given an integer array prices where prices[i] is the price of a given stock on the ith day. On each day, you may decide to buy and/or sell the stock. You can only hold at most one share of the stock at any time. However, you can buy it then immediately sell it on the same day. Find and return the maximum profit you can achieve.

### Intuition
- Every climb is the sub profit. Add all sub profits.
- `[1,7,5,8]`.  `(7-1) + (8-5) > (8 - 1)`.


### Code
```python
def max_profit(self, prices: List[int]) -> int:
    profit = 0
    for i in range(1, len(prices)):
        if prices[i - 1] < prices[i]:
            profit += (prices[i] - prices[i - 1])
    return profit
```

### Time complexity
- $T(n) = O(n)$ 
- $S(n) = O(1)$