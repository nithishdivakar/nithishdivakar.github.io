---
date: 2024-01-01 00:00:00 +0000
layout: post
level: h1
slug: '01'
status: done
title: Collaborative Filtering Part 01 - The Foundations & Classic Flaws
type: "series_collection"
---

# Collaborative Filtering - The Foundations & Classic Flaws

When we step into recommendation-system land, our job is simple to state but hard to do:

> Figure out which content to recommend to a user.

The easiest strategy is to show the most popular content and hope for the best. But can we do better?

Trying to do better means we want to figure out **which content a particular user is likely to enjoy**, not just what the crowd enjoys. That sounds straightforward until we hit two hard realities:

- R1: We have *lots* of users
- R2: We have *lots* of content

If we only had a handful of each, we could solve everything manually: just ask every user to sort every content by preference and call it a day. But nobody can rank a million movies (and we have millions of users too), so we need to predict instead of asking.

There’s one more complication: what does it even mean to "like" content? To stay grounded and practical, let's adopt a simple behavioral assumption:

> Users click content because they like it.

Of course, real life is messier.  People click for curiosity, boredom, mistakes, click-bait, doom-scrolling or butter fingers. But as a first step, let forge ahead with this assumption.

So the core problem becomes:


## P(click)

Given a user and a content, can we predict the probability that the user will click it? or .. **P(click | {content, user})**

A very quick Segue here. This P(click) problem underpins lot of other systems like ranking, feed, search and more. Simply what is meant by content and user might change to suit the problem.

## The "Naive" Approach: Neighborhood-Based CF

The initial solution to the P(click) problem is simple. Step 1: Find a set of simlar users. Step 2: Estimate P(click) as the fraction of those similar users who clicked the. Step 3: Done.

Simple ... except we don’t actually know who the "similar users" are. So lets define it as the most obvious thing. **Two users are similar if they clicked on same content**.

This leads to the simplest possible collaborative filtering setup. We construct a user–item interaction matrix with each row for a user and each column for a content. Each cell = 1 if the user clicked the item, 0 otherwise.

Now to measure similarity between two users, we compare their rows. A straightforward method is to count how many items they both clicked (1s in common) versus how many items either of them clicked; compute Jaccard similarity of the user's clicks.

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


Jaccard similarity gives us a number between 0 and 1 for any pair of users, indicating their degree of similarity. With a reasonable threshold on this score, we can decide who counts as a “similar user.” Once we have that set, Step 2 and Step 3 follow immediately: compute P(click) as the fraction of those similar users who clicked on the item.


Finally, we recommend the items the user hasn’t clicked yet, sorted by this estimated P(click).
This approach is known as **neighborhood-based collaborative filtering**.

## Neighborhood-Based Collaborative Filtering
- [Step 1]: Construct the user–item interaction matrix

    Each row represents a user, each column an item, and each cell is 1 if the user clicked the item, 0 otherwise.
- [Step 2]: For each user, compute their Jaccard similarity with every other user using this matrix.

    This gives a measure of how similar each pair of users is, based on their past clicks.
- [Step 3]: For each user, identify their neighbor set as users whose similarity score is above a chosen threshold.
 Then, estimate
    $$P(click∣\\{user,item\\})= \frac{\|\text{similar users who clicked the item}\|}{\|\text{similar users}\|}$$
	
- [Step 4:] Recommend the items the user hasn’t clicked yet, ranked by this estimated P(click).


We used Jaccard similarity because it’s simple and intuitive. But there are many ways to measure similarity between two users.

In our setup, each user is represented as a vector with each dimension for an item, with 1 for clicked and 0 for not clicked.
That means we can use any distance or similarity metric that makes sense for binary vectors: cosine similarity, L1 norm, L2 norm, or others. Each metric has its own perks and problems.


But let us specifcally talk about problems with Jaccard Similarity. What are the flaws of Neighborhood-Based CF?

## Flaws of Neighborhood-Based CF
1. Neighborhood-based CF only sees the surface level behavior.

    Imagine you’re a user who likes horror, comedy, and drama. But suppose there’s no one else on the platform who likes all three genres at once. You'll probably have a few clicks with horror fans, a few with comedy fans, and a few with drama fans, but never enough with any single group to be considered similar. **Your similarity score with everyone would be low even though your taste overlaps with many users in parts.**

    In summary this approach can't capture composite behaviour. It completely misses deeper and latent behaviour.

2. Computationally expensive. 

    To find similar users, we need to compare every user with everyone else. So there are $O(N^2)$ comparisons; clearly impractical when when we have millions of users. Even if we use Approximate Nearest Neighbour (ANN) techniques to speed things up, we still face another problem. Each user is represented by a vector whose length equals the total number of items. And we have a lots of items.

3. Sparse interactions. 

    The user-item matrix is extremly sparse. Almost every cell is a zero. When we compare 2 users, there is very little overlap to base similarity on. Since Neighbourhood CF doesn't infer latent behaviour, it only recommend items with explict co-click evidence. This creates a negative feedback loop. Sparese Data -> No shared clicks -> no recommendation -> Sparse data. 
    
    Even for users whoe are genuinely simlar, we never make the connection because the model cannot infer the connection without explicit evidence.

*Note for practitioners. I have not brought up cold start problem because the next approach we discuss  which solves most of the above issues, but not this one. We will bring it up later :)*



## The Classic Foundation: Matrix Factorization (MF)



## The "Zero" Problem: Why Standard MF is Wrong for Clicks