---
title : Reservoir Sampling
tags : [probability,distributed-computing]
date: 2021-10-12T05:04:51+05:30
draft: true
---

# Reservoir Sampling

How can you uniformly sample $k$ items from a stream?  

Reservoir Sampling is used when you want a uniform sample from a stream. The length of the stream is not known before and the stream is large enough that we cannot look back or store everything.

The algorithm is simple. 

```python
# Reservoir Sampling
reservoir[1:k] = stream[1:k]
for i=k+1 to n
    j = random(1,i)
    if j < k:
        reservoir[j] = stream[i]
```

Let prove the above process does infact gives us a uniform sample.

Let the stream be $(s_1,s_2,\ldots)$ and the reservoir be of size $k$.

At step $i$, the probability of selecting $s_i$ to add to reservoir is $\frac{k}{i}$. Also, probability of selecting
an element at random from the reservoir to make room is $\frac{1}{k}$.

Lets assume $s_j$ is in the reservoir before step $i$. Probability that $s_i$ replaces $s_j$ from the reservoir is  that $s_i$ is selected to be added and $s_j$ gets selected to be removed; which is
$\frac{k}{i}\frac{1}{k}=\frac{1}{i}$. Probability that $s_j$ survives the round is then $1-\frac{1}{i}$

So at beginning of an arbitrary step $i$, probability that an element $s_j$ is in the reservoir is $\frac{k}{i-1}$ and it survives this round is $s_j$ being in reservoir multiplied by that it was never selected = $\frac{k}{i-1}\left(1- \frac{1}{i}\right)=\frac{k}{i}$.

So by the end of the stream, each element which is in the reservoir would have been selected by a probability of $\frac{k}{n}$. This results in uniform sampling of $k$ elements from the steam. 


    