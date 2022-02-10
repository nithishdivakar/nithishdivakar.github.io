---
title : Reservoir Sampling
tags : [probability,distributed-computing]
date: 2021-10-12T05:04:51+05:30
draft: true
---

<!--<embed src="{{site.dev-images}}/2021-10-12-reservoir-sampling.pdf" width="500" height="500"  type="application/pdf" frameborder="0" allowfullscreen>-->
<embed src="https://daxpy-website.s3.ap-southeast-1.amazonaws.com/2021-10-12-reservoir-sampling.pdf" width="500" height="500"  type="application/pdf" frameborder="0" allowfullscreen>

---
title: Reservoir Sampling
---

` Machine Learning notes by Nithish Divakar. More at daxpy.xyz `

Reservoir Sampling is a technique for obtaining a uniform sample of
elements from a stream. The length of the stream is not known apriori
and the stream is large enough that we cannot look back.

-   Reservoir Sampling

-   reservoir\[1:k\] = stream\[1:k\]

-   i=k+1 to n

    -   j = random(1,i)

    -   $j<k$,

        -   reservoir\[j\]=stream\[i\]

Let the stream be $(s_1,s_2,\ldots)$ and the reservoir be of size $k$.

At step $i$, the probability of $s_i$ getting selected to be added into
the reservoir is $\frac{k}{i}$. Also, probability of randomly selecting
an element from the reservoir to make room is $\frac{1}{k}$.

Lets assume $s_j$ is in the reservoir before step $i$. Probability that
$s_i$ replaces $s_j$ from the reservoir is probability that $s_i$ is
selected to be added and $s_j$ gets selected to be removed; which is
$\frac{k}{i}\frac{1}{k}=\frac{1}{i}$. Probability that $s_j$ survives
the round is then $1-\frac{1}{i}$

So at beginning of an arbitrary step $i$, probability that an element
$s_j$ is in the reservoir is $\frac{k}{i-1}$ and it survives this round
is $s_j$ being in reservoir multiplied by that it was never selected =
$\frac{k}{i-1}\left(1- \frac{1}{i}\right)=\frac{k}{i}$.

So by the end of the stream, each element which is in the reservoir
would have been selected by a probability of $\frac{k}{n}$.


    