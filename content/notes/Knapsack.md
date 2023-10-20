---
title: Knapsack
layout: post
tags : [algorithms]
date: 2023-10-20T05:52:32+05:30
draft: false
---


# Knapsack


The following is the description of knapsack problem.

We are given a set of items each with its own weight ($w_i$) and value ($v_i$). We are also given a limit or maximum capacity $T$. 
How do we select a subset of items such that the total weight is within the limit, but the total value is maximum?

$$\begin{align} 
&\max\; \sum x_i v_i 
\\
&s.t. \quad \sum x_i w_i \leq T
\end{align}$$

Recurrence relation solving the problem
$$S_{k,t} = \max \{S_{k-1,t}, v_k + S_{k-1,t-w_k}\}$$

$S_{k,t}$ represents maximum value that can be achieved which has a maximum weight of $t$ with some subset of first $k$ items. 


Can we select more that one of the same item? 

Restricted cases of knapsack are more interesting. Minimising counts of items (value of each item is 1) while constraining on overall sum amounts to a selection problem. And the question we are solving for essentially is what is the minimum number of items we can select which gives us the aspired value. 



## Bounded knapsacks
Bounded knapsacks is when we have at most $c$ copies of  each item. We need to only consider the case  when we have only a single copy of each item or **0/1 knapsack**. We can extending 0/1 knapsack to bounded knapsack by creating copies of items which occur more than one. 

### 0/1 knapsack
```python
# O(nT) time, O(T) space
def knapsack_01(nums,T) -> int:
    nums.sort()                           
    dp = [0 for _ in range(T+1)]     
    for num in nums:                      
        if num > T: break
        for slack in range(T-num,-1,-1):
            if dp[slack] > 0:
                dp[slack + num] = max(
                              dp[slack + num], 
                              dp[slack]+1)
        dp[num] = max(dp[num], 1)
    return dp[T]
```

A few things to unpack here on what the algorithm is doing. 

First we are sorting all the 

Time complexity is $O(n\log n)$ for sorting the items and $O(nT)$
for computing the optimal answer. The algorithm also uses a $O(T)$ sized array for storing solutions of sub-problems.


## Unbounded knapsack

When we have infinite copies of each items, we have **unbounded knapsack** problem. $x_i > 0$ and $x_i\in \mathbb{Z}$

A classic example of unbounded knapsack is coin change problem. 

### Coin Change
Given a set of coins denomination find the smallest collection of coins that add up to a given amount.

The problem is an instance of unbounded [knapsack](app://obsidian.md/Knapsack).

```python
def coin_change(coins, amount):
    dp = [float('inf') for _ in range(amount+1)]
    dp[0] = 0
    for coin in coins:
        for i in range(coin, amount+1):
            dp[i] = min(dp[i], dp[i-coin]+1)
    return dp[-1] if dp[-1] != float('inf') else -1
```


## Fractional Knapsack
$x_i \in [0,1]$ $$\begin{align}
&\max \sum x_iv_i
\\
& s.t. \quad \sum x_iw_i \leq T\end{align}$$
Can be solved using greedy algorithm in $O(n \log n)$. 

```python # Sort all the items by their value per unit weight.
v,w = unzip(sorted(zip(v,w),key= lambda r:r[0]/r[1]))
x = [0.0 for i in range(n)]
C = 0.0

for i range(n):
	x[i] = min((T-C)/w[i],1.0)
	C += w[i] * x[i]
```
