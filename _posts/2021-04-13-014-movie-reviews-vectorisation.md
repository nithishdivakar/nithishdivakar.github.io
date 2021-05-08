---
title : Representation Learning through Matrix Factorisation 
tags : [ml-applied]

---

Movie rating is a starter problem for learning machine learning. The problem is easy to define and model, but it has a few hidden gems to learn form. Lets explore that here. 

The problem is simple, $m$ movies, $n$ users and we have the data of rating of movies by users. Now in reality, each user might have rated a few movies while total number of users and movies are huge. We can consider the whole ratings data as a matrix $n\times m $ matrix $R$ where $R_{ij}$  is the rating of $i^{th}$ movie by $j^{th}$ user.


The problem is to have a system which can predict the rating a user would have given a movie. Now the modelling part is easy as a matrix facotrisation problem. We can assume every user is represented by a embedding $u_i$  and similarly, every movie has a embedding $m_j$. We simply want 

$$M_{ij}  \sim \langle u_i,m_j\rangle$$

## Bad Modelling
If we simply model the learning problem as $ error = \lVert U^TM - R \rVert_2$, then we are making a few implicit assumptions. We have implicitly converted the sparse rating data $D = \{(u,m,r)\}$ into a dense matrix and while doing so, we have filled the unknown entires with zeros. This is equivalent to assuming that each unknown rating is 0. 

## Good Modelling

What we have to do instead is to simply model what the data is telling us and nothing else.  Essentially, 

$$error = \sum_{(u_i,m_j,r_{ij})\in D} \left(\langle u_i^T,m_j\rangle - r_{ij}\right)^2$$


## Gradient Descent and Learning

The updates for U and M according to gradient descent are

$$U \gets U = 2\alpha (U^TM - R)M$$

$$M \gets M = 2\alpha (U^TM - R)U$$


Now to convert this to a batched gradient descent, we simply have to take a batch of ratings and work on updating only the concerned indices of $U$ and $M$. But we do have to take care if in our batch, user id or movie id is repeated. The gradient have to be averaged in such case. The following code does it, but slowly. 

![Slow Code](/images/014_slow_batch_update.png)

Vectorising the same code requires calculation of all gradients and then scaling it using frequency of each indices. The scaled gradients of each indices can them simply be added together to effectively get average gradient from each repeated indices.  The vectorised version is significantly faster.

![Fast Code](/images/014_fast_batch_update.png)

MovieLens is a good movie ratings data to play with. It is [here](https://grouplens.org/datasets/movielens/25m). 
