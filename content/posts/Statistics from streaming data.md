---
title: Statistics from Streaming Data
tags : [algorithms, statistics]
date: 2022-02-16
draft: true
---

Compute average of 500B numbers

Q1: Assume you have 500B samples (of type double) data that you need to compute the average for. Write code that computes this average. 

[1, 1, 1, 1000, 1, 1, 8000, 1, 1, 3000] 

## Running Average
```python
s = 0
n = 0
while True:
    x = get_next()
    s = (s*n)/(n+1) + (x)/(n+1)
    n +=1
```

## Exponential Moving Average
```python
s = 0
alpha = 0.5
while True:
    x = get_next()
    s = alpha * s + (1-alpha) * x
```


## Reservoid Sampling

## Count min sketch

