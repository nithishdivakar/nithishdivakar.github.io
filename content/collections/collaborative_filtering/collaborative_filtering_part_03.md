---
date: 2026-03-13 00:00:00 +0000
layout: post
level: h1
slug: '03'
tags : [recommendation system]
status: done
draft: false
type: "series_collection"
title: Scaling with Features & Neural Networks
---

# Scaling with Features & Neural Networks
*Part 3/5 of [Collaborative Filtering](/collections/collaborative_filtering) Collection* 

So far, we have discussed Neighborhood-Based Collaborative Filtering, Matrix Factorisation,  Weighted Matrix Factorization and Logistic Matrix Factorization ([part 1](../01) and [part 2](../02)). They all have the inherent flaw of "cold start" as they are built on top of interaction history. No interactions means no recommendations. New users and items are practically invisible to these algorithms.

But if we really peel out the layers of what we have built so far, it seems kinda funny. All the techniques so far has resulted in a vector per user and item. We have built a giant look up table !!

User ID $\to$ $p_u$, Item ID $\to$ $q_i$ $\ldots$ and then dot product.

So besides **Cold Start** we have these other problems.

**Feature blindness.** The model knows nothing about *what* a user or item actually is. Two movies could be nearly identical; same genre, same director, same same actor (hello Fast and Furious) but if their click histories look different, the model treats them as unrelated.

**Catalog churn.** In real systems, new content arrives constantly. A news recommender might ingest thousands of articles per day. A music platform adds hundreds of tracks per hour. Every new item needs interactions before it can be recommended. But it can't get interactions until it's recommended. Pure CF has no way out of this loop.

## From Lookup Tables to Parameterised Functions
 
In Logistic Matrix Factorisation, we trained using negative sampling; explicitly contrasting clicked items against randomly sampled ones the user ignored.

This gave us a clean training signal: push $P(\text{click} \mid u, i)$ up for observed pairs, push it down for sampled negatives. What to optimise for is clear.
 
However, the user representation $p_u$ is a row in a lookup table. It's just a vector that gets updated whenever the user appears in the click data.
 
> What if we made this vector something that is computed from the user's inherent features, through a learned function?
 
$$ p_u = g_{\theta}(x_u) $$
 
and something similar for items too.
 
$$ q_i = h_\phi(x_i) $$
 
where $x_u$ and $x_i$ are the user's and item's features, and $\theta$ and $\phi$ are learned parameters shared across *all* users and items respectively.

You must be wondering what $g$ and $h$ could possibly be. We have many options, but neural networks are the most versatile for the task at hand. Take features, compute a representation, and remain learnable end-to-end.
 
The scoring function stays the same as [LMF](../02). Instead of $\sigma(p_u^Tq_i)$ we have

$$P(\text{click} \mid \\{u, i\\}) = \sigma\left( g_{\theta}(x_u)^\top h_\phi(x_i)\right)$$

And training stays the same: negative sampling, binary cross-entropy, gradient descent. The only thing that changed is *what we're differentiating through*.

Instead of updating a single row $p_u$ or $q_i$, we update the parameters $\theta$ and $\phi$. And that update improves representations for every user and item simultaneously.
 
## The Features
- **User features:** Age, country, device, time of day, recently watched genres, historical click rate.
- **Item features:** Genre tags, release date, duration, language.
 
A neural network takes a vector as input, so we can take the user and item features and concatenate them into a single vector. But this works directly only for continuous features; the ones that are inherently numbers: age, duration, click rate, and so on.
 
We can apply simple transforms to convert some non-continuous features into continuous ones. Release date becomes days from epoch. Time of day becomes seconds from midnight. But there are features where this just isn't possible: categorical features.
 
Language is a good example. One approach to converting these into a vector is [one-hot encoding](https://en.wikipedia.org/wiki/One-hot).

- Construct a vector of size equal to the total number of distinct values for the feature.
- Assign an index to each distinct value of the categorical feature.
- Set the index to  and everything else to 0.

The representation of "english" is simply a vector of zeros with a 1 at the index assigned to english.
 
$$\text{"english"} \to \left[0,\ 0,\ \underbrace{1}_{\text{index of english}},\ \ldots,\ 0 \right]$$
 
This works fine when the number of distinct values is small. Movie languages, of which there are perhaps a few dozen. But it breaks down when the possible values are huge.

Consider director name as a categorical feature: across a large catalog there are tens of thousands of directors, and that number only grows. That's a very wide, very sparse vector for a single feature.
 
In such cases, we use learnable embeddings.
 
### Embeddings: Learnable Lookup Tables
 
In MF, WMF, and LMF we have pretty much solved this exact problem already. We had an index of an attribute and needed a vector to represent it, retrievable by index. There it was user ID and item ID. Here it is language, genre, director, and so on.
 
An embedding layer is exactly this, made explicit and generalised to any categorical variable:
 
$$E \in \mathbb{R}^{V \times d}, \qquad \text{embed}(c) = E[c] \in \mathbb{R}^d$$
 
The entries of $E$ are learned parameters updated during training. And because the embeddings are trained to minimise the task loss, the geometry of the space becomes meaningful. The model discovers that users who click Horror also tend to click Thriller, so those genre embeddings get pushed together. Different kinds of properties emerge for such learnt embeddings simply from training data. See [this blog post](https://www.offconvex.org/2016/02/14/word-embeddings-2/) for more details.

 
## Putting It All Together
 
**Neural network-based recommendation:**
1. Generate a dataset using clicks as positives and negative sampling for negatives.
2. Convert user features into a vector by applying simple transforms for continuous features, use embedding layers for discrete ones, and concatenate everything into a single feature vector. Same for items.
3. Train the model to minimise the cross-entropy loss.
4. At run time, score click probability for a user-item pair by feeding their features into the model.
 
Users or items with no interaction history still get meaningful predictions. The model sees them through their features and makes the best predictions it can with what it has. Cold start is now a sliding scale, not a binary failure.
 
but, did you catch the issue?
 
## What Is Wrong With This Now?
 
How do we use this as a recommendation system?

Find items where click probability is highest and recommend those to the user. But we are no longer storing representations of users or items. We have to compute them. i.e. a neural network forward pass for every $(user, item)$ pair. With millions of users and millions of items, that's a lot of forward passes. GPUs go brr...
 
The solution is a fundamental architectural choice that defines how all large-scale recommendation systems are built today.
 
*That is in [part 4](../04)*