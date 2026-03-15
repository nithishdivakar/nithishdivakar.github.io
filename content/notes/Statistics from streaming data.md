---
title: Statistics from Streaming Data
tags : [algorithms, statistics]
date: 2022-02-16T07:30:00+05:30
draft: false
layout: post
---

# Statistics from Streaming Data

Many real-world data pipelines deal with streams; data that arrives continuously and cannot be stored in full. The challenge is to compute useful statistics using $O(1)$ or $O(k)$ memory, in a single pass.

## Running Average

The naive approach is to accumulate the sum and divide but total number. But this approach leads to overflows for large streams. Instead, maintain a running average updated incrementally:

$$s_n = \frac{n-1}{n} s_{n-1} + \frac{1}{n} x_n$$
```python
s = 0
n = 0
while True:
    x = get_next()
    s = (s*n)/(n+1) + x/(n+1)
    n += 1
```

This is numerically more stable than accumulating a sum because $s$ stays in the same range as the data throughout.

## Exponential Moving Average

The running average weights all samples equally. But for non-stationary streams where the distribution shifts over time, recent samples should matter more. EMA does this with a single parameter $\alpha \in (0, 1)$:

$$s_t = \alpha s_{t-1} + (1-\alpha) x_t$$
```python
s = 0
alpha = 0.5
while True:
    x = get_next()
    s = alpha * s + (1-alpha) * x
```

Unrolling the recurrence, sample $x_{t-k}$ contributes an exponentially decaying influence $\alpha^k (1-\alpha)$. Larger $\alpha$ means a longer memory; smaller $\alpha$ reacts faster to recent changes. Unlike the running average, EMA never "forgets" old samples completely, but their influence becomes negligible.

## Reservoir Sampling

**Problem:** sample $k$ elements uniformly at random from a stream of unknown length $n$, using $O(k)$ memory.

The key idea: when the $i$-th element arrives, include it with probability $\frac{k}{i}$, displacing a random existing element if selected.
```python
import random

reservoir = []
for i, x in enumerate(stream()):
    if i < k:
        reservoir.append(x)
    else:
        j = random.randint(0, i)  # uniform in [0, i]
        if j < k:
            reservoir[j] = x
```

**Why it's uniform:** by induction. After seeing $k$ elements the reservoir holds all $k$, each with probability $1$. When the $i$-th element arrives ($i \geq k$), it is included with probability $\frac{k}{i+1}$. Each element already in the reservoir survives with probability $\frac{i}{i+1}$ (probability of not being evicted). If by induction each was present with probability $\frac{k}{i}$, after step $i$ it remains with probability:

$$\frac{k}{i} \cdot \frac{i}{i+1} = \frac{k}{i+1}$$

which matches the new element's inclusion probability. So at all times, every element seen so far is in the reservoir with equal probability $\frac{k}{n}$.

## Count-Min Sketch

**Problem:** estimate the frequency $f_x$ of any element $x$ in a stream over a large universe $\mathcal{U}$, using sublinear memory. Storing exact counts is infeasible when $|\mathcal{U}|$ is huge (e.g. IP addresses, n-grams).

A Count-Min Sketch maintains a $d \times w$ table of counters and $d$ independent hash functions $h_1, \ldots, h_d : \mathcal{U} \to [w]$. On seeing element $x$, increment all $d$ corresponding cells. To query, return the minimum across all $d$ cells.
```python
d, w = 5, 2000  # depth, width
table = [[0] * w for _ in range(d)]

def update(x):
    for i in range(d):
        table[i][hash(x, i) % w] += 1

def query(x):
    return min(table[i][hash(x, i) % w] for i in range(d))
```

The estimate $\hat{f}_x$ is always an overestimate ($\hat{f}_x \geq f_x$) — cells can only be inflated by hash collisions, never deflated. Taking the minimum across $d$ rows reduces this overestimation. With $w = \lceil e/\varepsilon \rceil$ columns and $d = \lceil \ln(1/\delta) \rceil$ rows:

$$P\left(\hat{f}_x \leq f_x + \varepsilon \cdot \|f\|_1\right) \geq 1 - \delta$$

where $\|f\|_1$ is the total stream length. So with $w = 2718, d = 5$ we get error within $0.1\%$ of total stream size with probability $\geq 99.3\%$, using only $\sim 100\text{K}$ counters regardless of $|\mathcal{U}|$.