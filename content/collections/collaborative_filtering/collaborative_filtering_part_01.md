---
date: 2026-01-04 00:00:00 +0000
layout: post
level: h1
slug: '01'
status: done
title: Collaborative Filtering Part 01 - The Foundations & Classic Flaws
type: "series_collection"
---

# Collaborative Filtering - The Foundations & Classic Flaws

In the world of recommendation-system, the main objective simple to state but hard to do:

> Figure out which content to recommend to which user.

The easiest strategy is to show the most popular items and hope for the best. But can we do better?

This  means figuring out **which content a particular user is likely to enjoy**. Not just what the crowd likes. That sounds straightforward until we hit two hard realities:

- R1: We have *lots* of users
- R2: We have *lots* of content

If we only had a handful of each, we could solve this manually by asking every user to rank every piece of content. But scale of our problem makes this impossible, we must predict preferences instead of asking for them.

There’s one more complication: what does it actually mean to "like" content? To stay grounded and practical, let's adopt a simple behavioral assumption:

> Users click on content because they like it.

Of course, real life behaviour is messier.  People click out of curiosity, boredom, mistakes, click-bait, doom-scrolling or butter fingers. But as a first step, let's forge ahead with this assumption.

So the core problem is calculating:

## P(click)

Given specific user and a content, can we predict the probability that the user will click? or .. 

$$P(click | \\\{content, user\\\})$$

A quick segue: This $P(click)$ problem underpins a variety of systems like ranking, feed, search and more. Simply the definition of content and user might change to suit the problem.

## The "Naive" Approach: Neighborhood-Based CF

The initial solution to the $P(click)$ problem is simple. 
- Step 1: Find a set of simlar users. 
- Step 2: Estimate P(click) as the fraction of those similar users who clicked the item.
- Step 3: Done.

Simple ... except we don’t know who the "similar users" are. So lets define it as the most obvious thing. **Two users are similar if they clicked on same content**.

This leads to the simplest possible collaborative filtering setup. We construct a user–item interaction matrix with each row for a user and each column for a content. Each cell = 1 if the user clicked the item, 0 otherwise.

To measure similarity between two users, we compare their rows. A straightforward method is to count how many items they both clicked (1s in common) versus how many items either of them clicked; compute Jaccard similarity of the user's clicks.

$$\text{Jaccard similarity} = \frac{\text{item both clicked}}{\text{ items either clicked}} $$

```
 
      m1  m2  m3  m4  m5  m6 
    ┌───┬───┬───┬───┬───┬───┐ 
 u1 │   │ ✓ │   │ ✓ │   │ ✓ │ 
    ├───┼───┼───┼───┼───┼───┤ 
 u2 │ ✓ │ ✓ │   │   │   │   │ 
    ├───┼───┼───┼───┼───┼───┤ 
 u3 │ ✓ │ ✓ │   │ ✓ │   │   │ 
    └───┴───┴───┴───┴───┴───┘ 
     
         J(u1,u2) = 1/4
         J(u1,u3) = 2/4
         J(u2,u3) = 2/3
 
```


Jaccard similarity gives us a number between 0 and 1 indicating the degree of similarity between any two users. With a reasonable threshold on this score, we can decide who counts as a “similar user.” Once we have that set, Step 2 and Step 3 follow immediately: compute $P(click)$ as the fraction of those similar users who clicked on the item.

Finally, we recommend the items the user hasn’t seen yet, ranked by this estimated $P(click)$.
This is **Neighborhood-based Collaborative Filtering**.

## Neighborhood-Based Collaborative Filtering
- **Step 1**: Construct the user–item interaction matrix. Each row represents a user, each column an item, and each cell is 1 if the user clicked the item, 0 otherwise.
- **Step 2**: For each user, compute their Jaccard similarity with every other user using this matrix. This gives a measure of how similar each pair of users is, based on their past clicks.
- **Step 3**: For each user, identify their neighbor set as users whose similarity score is above a chosen threshold. Then, estimate
    $$P(click∣\\{user,item\\})= \frac{\|\text{similar users who clicked the item}\|}{\|\text{similar users}\|}$$
- **Step 4**: Recommend the items the user hasn’t seen yet, ranked by this estimated $P(click)$.


We used Jaccard similarity because it’s simple and intuitive. But there are many ways to measure similarity between two users.

In our setup, each user is represented as a vector with each dimension for an item, with 1 for clicked and 0 for not clicked. This implies we can use any distance or similarity metric for binary vectors: cosine similarity, L1 norm, L2 norm, or others. Each metric has its own perks and problems.

But irrespective of metrics, Neighborhood-Based CF has some fundamental flaws.

## Flaws of Neighborhood-Based CF
1. Neighborhood-based CF only sees the surface level behavior.

    Imagine a user who likes horror, comedy, and drama. But if no other user shares the interest in these exact three genres at once, the user will have low similarity scores with everyone. They'll probably have a few clicks with horror fans, a few with comedy fans, and a few with drama fans, but never enough with any single group to be a neighbour. **Your similarity score with everyone would be low even though your taste overlaps with many users in parts.**

    In summary this approach can't capture composite behaviour. It completely misses deeper and latent behaviour.

2. Computationally expensive. 

    To find similar users, we need to compare every user with everyone else. So there are $O(N^2)$ comparisons; clearly impractical when when we have millions of users. Even if we use Approximate Nearest Neighbour (ANN) techniques to speed things up, we still face another problem. Each user is represented by a vector which is as long as our item catalogue.

3. Sparse interactions.

    The user-item matrix is extremly sparse. Almost every cell is a zero. When we compare 2 users, there is very little overlap to base similarity on. Since Neighbourhood CF doesn't infer latent behaviour, it only recommend items with explict co-click evidence. This creates a negative feedback loop. Sparse Data -> No shared clicks -> no recommendation -> Sparser data. 
    
    Even for users who are genuinely similar, we never make the connection because the model cannot infer them without explicit evidence.

*Note for practitioners. I intentionally skipping cold start problem for now because the next approach we discuss solves flaws above, but not cold start. We will bring it up later :)*

## Moving From Inference to Prediction
In the Neighborhood approach, we are essentially performing a lookup. We look at the past to find "people like you" and infer that you will do what they did. This is purely reactive which is also the fundamental reasons for the flaws we uncovered. 

To do better, we move to a more predictive setup based on a core assertion:

> A click is the result of compatibility between a user and an item.

In concrete terms, we assume there are "latent features" (hidden traits) of both the user and the item that make them compatible. The stronger this compatibility, the higher the chance of a click. We are looking for a function that can measure this strength:

$$P(click) = f(user, item)$$


To turn this into a working algorithm, we have to answer two implementation details.
1. How do we represent the latent features of the user and the item?
2. What should the function $f$ be?

If we represent both the user and item as $k$-dimensional vectors and define $f$ as the dot product, we arrive at the classic recommendation algorithm: Matrix Factorization (MF).

## Matrix Factorization (MF)
If $p_u$ is a $k$-dimensional vector representing the latent features of a user $u$, and $q_i$ is a $k$-dimensional vector representing the latent features of an item $i$, we have,

$$P(click \mid \\\{user, item\\\}) = p_u^T q_i$$

But how do we compute the actual values within these vectors?

We use the existing user–item interaction matrix, $A$, as our ground truth. For $p_u$ and $q_i$ to be faithful representations of latent traits, their alignment must agree with the clicks we have already observed. 

$$A_{u,i} = p_u^T q_i$$

If we stack all user vectors into a matrix $P$ and all item vectors into a matrix $Q$, what we have is 

$$A \approx P Q^T$$

This is essentialy factorising a large matrix A into two slim matrices. ergo the name, Matrix Factorization. With this, we gain the ability to predict score for any combination of user and item. simply take their corresponding vector and compute dot product to compute $P(click)$

Singular Value Decoposition (SVD) is an excellent algorithm to compute $P$ and $Q$ from $A$ here. However,  we will refrain from diving into the specific implementation details just yet. Because there is a fatal flaw in this algorithm. The zeros.

## The "Zero" Problem

Let’s re-examine how we constructed our user-item interaction matrix:

> Each cell = 1 if the user clicked the item, 0 otherwise.

And in Matrix factorisation, we equate $A_{u,i}$ with $P(click \mid \\\{user, item\\\})$. But if we closely examine what 0 means, we can quickly realise a disconnect. 

A 0 in our matrix doesn't imply a very low chance of click, it often imply  no data. The item was never shown to the user. They never had the chance to decide.

To fix the problem, we have to change how the interaction matrix is constructed. Ideally we would fill A with 1 if there was a click and 0 if and only if the item was viewed by the user and they choose not to click. 

There are many nuances here. If a system presents 20 items to a user and they click item #7, should we record the other 19 items as zeros? Or perhaps just #6 and #8? This is a system-dependent decision that must cater to the specific goals of your recommendation engine.

This change however leads to a different problem. Vast majority of matrix A would be empty. Singular Value Desomposition cannot process a matrix where  cells are empty. None of the linear algebra factorisation algorithms can. 

We deal with this missing values with a clever change in the formulation. Read more in [part 2](../02).