---
date: 2026-03-01 00:00:00 +0000
layout: post
level: h1
slug: '03'
tags : [recommendation system]
status: done
title: Collaborative Filtering Part 03
---

# Collaborative Filtering Part 03  - Scaling with Features & Neural Networks

In Part 2, we ended with the cold start problem. WMF and LMF are powerful, but they are built entirely on interaction history. No interactions means no recommendations. A new user or a new item is effectively invisible to these models.

But cold start is only one symptom of a deeper issue.

## The Scaling Wall

Pure CF models — MF, WMF, LMF — each learn one vector per user and one vector per item. The entire model is a lookup table. Given a user ID, retrieve $p_u$. Given an item ID, retrieve $q_i$. Dot product. Done.

This breaks in three distinct ways.

**Cold start (as established).** No interactions → no vector → no recommendations.

**Feature blindness.** The model knows nothing about *what* a user or item actually is. Two movies could be nearly identical — same genre, same director, same runtime — but if their click histories look different, the model treats them as unrelated. All the rich signals that describe users and items are completely ignored.

**Catalog churn.** In real systems, new content arrives constantly. A news recommender might ingest thousands of articles per day. A music platform adds hundreds of tracks per hour. Every new item needs interactions before it can be recommended — but it can't get interactions until it's recommended. Pure CF has no way out of this loop.

The fix requires a fundamentally different framing. Instead of asking "what has this user clicked?", we ask "who is this user, and what is this item?"

## The Modern Solution: Feature-Based Neural Networks

Recall from Part 1 the core framing:

$$P(click) = f(user, item)$$

In MF, *user* and *item* were bare ID lookups and $f$ was a dot product. The generalisation is simple: let *user* and *item* be rich feature descriptions, and let $f$ be a neural network.

What counts as features?

**User features**: user ID, age, country, device, time of day, recently watched genres, historical click rate.

**Item features**: item ID, genre tags, release year, duration, language, creator ID.

**Context features**: what device, what time, what did they just finish watching.

The key insight: user ID and item ID are still valid features. They just aren't the *only* features anymore. For a user with a rich click history, the ID embedding carries a lot of signal. For a brand new user, the model falls back on age, country, device. Cold start becomes a graceful degradation rather than a hard failure.

### MF as a Special Case

It helps to see MF as a specific instantiation of this broader framework.

In MF, the user representation is $p_u$ — a vector looked up by ID. The item representation is $q_i$ — same. The scoring function is a dot product. That's it.

In a feature-based neural network, we replace each lookup with a learned transformation over all available features:

$$\hat{r}_{ui} = f\bigl(g_u(\text{features}_u),\ g_i(\text{features}_i)\bigr)$$

where $g_u$ and $g_i$ are neural networks that produce dense vector representations, and $f$ is a scoring function. MF is just the case where $g_u$ is a single embedding lookup, $g_i$ is a single embedding lookup, and $f$ is a dot product. Every generalisation from there adds expressiveness.

## The "Magic" Ingredient: Embeddings

Before we can feed features into a neural network, we have to deal with a practical problem. Features come in very different forms.

**Continuous features** — age, duration, timestamp — can be fed in directly as floats after normalisation.

**Categorical features** — country, genre, device type, item ID — are trickier.

The naive approach is one-hot encoding. If we have 10 million items, each item becomes a vector of 10 million zeros with a single 1. Two problems immediately. First, this is enormous. Second, it's completely uninformative. "Horror" and "Thriller" are as far apart as "Horror" and "Cooking" under one-hot encoding. The encoding says nothing about relationships between categories.

The solution is **embeddings**.

### What Is an Embedding?

An embedding is a learned dense vector for each categorical value. Instead of a 10-million-dimensional one-hot vector, we learn a compact 64 or 128-dimensional vector for each item. These vectors live in a continuous space where geometry carries meaning.

Formally, an embedding layer is a matrix $E \in \mathbb{R}^{V \times d}$ where $V$ is the vocabulary size and $d$ is the embedding dimension. Looking up the embedding for category $c$ is just selecting row $c$:

$$\text{embed}(c) = E[c] \in \mathbb{R}^d$$

The values in $E$ are learned during training like any other model parameter. The model organises the space however it needs to — the only constraint is that the representations must help minimise the loss.

What emerges in practice: semantically similar categories end up close together. Horror and Thriller drift toward each other. Users with similar taste cluster. Items from the same creator form loose neighbourhoods.

This is where everything from Parts 1 and 2 snaps into focus. The user matrix $P$ and item matrix $Q$ from MF are exactly embedding tables — one row per user, one row per item. MF is a two-embedding model with a dot-product scoring function. The cold start problem is just the problem of having an untrained row in an embedding table.

### Combining Multiple Features

Once we have embeddings for categorical features and normalised values for continuous ones, combining them is straightforward: concatenate.

$$\mathbf{v}_u = \text{concat}\bigl[\text{embed}(\text{user\_id}),\ \text{embed}(\text{country}),\ \text{embed}(\text{device}),\ \text{normalised\_age},\ \ldots \bigr]$$

Feed this into a neural network. The network learns how to blend these signals into a useful final representation.

For a user with a long click history, the user ID embedding dominates. For a brand new user, the model leans on country, device, and time of day. The balance is learned automatically from data.

*This concatenate-then-transform pattern is the skeleton of most production recommendation models today. The architecture choices around it vary by system. But the skeleton is the same.*

### Cold Start, Revisited

With feature-based embeddings, cold start is no longer a hard failure.

- **New user, no interactions**: The user ID embedding is untrained. The model falls back on demographics and context. Recommendations are generic at first, but not absent.
- **New item, no interactions**: The item ID embedding is untrained. The model uses genre, creator, duration, language. Items from similar creators or genres end up nearby in embedding space. The item is immediately recommendable.

As interactions accumulate, the ID embeddings get trained and the model blends them in. Cold start is a sliding scale, not a binary failure.

---

We now have a model that can handle rich features and generalise beyond interaction history. But we've introduced a new problem. This model is expensive.

In MF, scoring an item for a user was a single dot product. Now it's a neural network forward pass — for every (user, item) pair. With millions of users and millions of items, this is completely infeasible in real time.

The solution is a fundamental architectural choice that defines how all large-scale recommendation systems are built today.

*Read more in [Part 4](../04)*