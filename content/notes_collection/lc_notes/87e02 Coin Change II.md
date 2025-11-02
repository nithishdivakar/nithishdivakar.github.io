---
date: 2024-01-01 00:00:00 +0000
layout: post
slug: 87e02
status: done
tags:
- knapsack
title: Coin Change II
---

## Coin Change II [LC#518]
> You are given an integer array `coins` representing coins of different denominations and an integer `amount` representing a total amount of money. Return the number of combinations that make up that amount. If that amount of money cannot be made up by any combination of the coins, return 0. You may assume that you have an infinite number of each kind of coin.

### Intuition

### Code
```python
def coin_change(amount: int, coins: List[int]) -> int:
    dp = [0]*(amount +1)
    dp[0] = 1
    for coin in coins:
        for amt in range(coin, amount + 1):
            dp[amt] += dp[amt - coin]
    return dp[amount]
```

### Time complexity
- $T(n) = O(nW)$ 
- $S(n) = O(n)$