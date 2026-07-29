---
date: 2026-03-15 00:00:00 +0000
layout: post
level: h1
slug: '05'
tags : [recommendation system]
status: todo
draft: true
title: How Do We Know It’s Working?
type: "series_collection"
---


# Collaborative Filtering Part 05
5/5 of [Collaborative Filtering](/collections/collaborative_filtering) Collection*

## Evaluation and Pitfalls

Building a recommendation system is one thing. Knowing whether it's good is another.

## Offline Metrics

The standard approach: hold out a portion of interactions as a test set. Have the model produce a ranked list for each user. Measure how well the ranked list recovers the held-out interactions.

**Precision@k**: Of the top-k items recommended, what fraction did the user actually interact with?

$$\text{Precision@k} = \frac{|\text{top-k} \cap \text{interacted}|}{k}$$

**Recall@k**: Of all items the user interacted with, what fraction appear in the top-k?

$$\text{Recall@k} = \frac{|\text{top-k} \cap \text{interacted}|}{|\text{interacted}|}$$

**NDCG@k** (Normalized Discounted Cumulative Gain): Precision@k and Recall@k treat all positions in the top-k equally. NDCG discounts hits that appear lower in the list, rewarding models that surface relevant items earlier.

$$\text{DCG@k} = \sum_{i=1}^{k} \frac{\text{rel}_i}{\log_2(i+1)}, \quad \text{NDCG@k} = \frac{\text{DCG@k}}{\text{IDCG@k}}$$

where IDCG is the DCG of the ideal ranking — all relevant items at the top.

**AUC** (Area Under the ROC Curve): Measures the probability that the model ranks a random positive higher than a random negative. Useful for overall discriminative power but insensitive to ranking order within the top-k.

## Why Offline Metrics Are Misleading

Offline metrics measure agreement with historical data. The problem is that historical data is not a neutral record of preferences. It's a biased sample, shaped by the very system we're trying to improve.

**Exposure bias.** Users can only click items they were shown. If the old system never showed users certain items, those items have zero clicks — not because users dislike them, but because they never had the chance. A new model that recommends these items will look worse offline, even if it's genuinely better.

**Popularity bias.** Popular items are shown to more users and accumulate more interactions. A model optimised for offline metrics learns to recommend popular items because they generate more training signal. Niche items are systematically underfitted.

**Position bias.** Items shown at the top of a feed get clicked more than items at the bottom, regardless of quality. If we don't correct for this, the model learns that top-positioned items are good — not that good items end up at the top.

**Feedback loops.** If the deployed model's recommendations generate the next round of training data, errors compound. The model reinforces its own biases, quietly, over time.

These biases mean offline evaluation is necessary but not sufficient. A model that improves offline metrics by 2% might degrade the actual user experience. A model that barely moves offline metrics might substantially improve engagement once deployed. The ground truth is production behaviour.

## Online Evaluation

**A/B testing** is the standard. Split users randomly into two groups. The control group gets recommendations from the current system. The treatment group gets recommendations from the new model. After a defined period, compare the groups on business metrics: click-through rate, watch time, session length, retention.

A/B testing is reliable but slow. A meaningful experiment typically runs one to two weeks to accumulate statistical power and account for day-of-week effects. Running many sequential experiments is expensive in time.

**Interleaving** is a faster alternative. Instead of showing each group one system's recommendations, we interleave the top-k lists from both systems into a single merged list for each user. Items from each system are tracked invisibly. We measure which system's items attracted more clicks within the same session.

Interleaving converges on a winner much faster than A/B testing because it eliminates user-level variance — the same user is comparing both systems simultaneously. It's well-suited for quickly identifying which of two model variants is better. It's less suited for estimating the magnitude of a business metric improvement.

*In practice, most teams use interleaving for fast iteration and A/B tests for the final gate before a full rollout.*

## Conclusion: The Journey and What's Next

We started with a user-item matrix and a simple lookup. We found similar users, inferred their preferences, and recommended what they liked. It was intuitive and it broke quickly — on composite taste, on scale, on sparsity.

We moved to matrix factorization. A predictive model instead of a lookup. Latent features instead of surface similarity. We ran into the zero problem: the matrix was full of missing data masquerading as negatives.

We solved that with WMF and LMF — confidence weighting and negative sampling respectively. Both work and both are still in production today. Both hit the same ceiling: they can only reason from interaction history. No history, no recommendations.

We fixed that with feature-based neural networks. Brought in user attributes, item metadata, context signals. Showed that MF was a special case all along — just a two-embedding model with a dot product. Every generalisation adds features, adds layers, adds expressiveness.

We scaled that to production with the two-stage architecture. Retrieval uses a Two-Tower model to narrow millions of items to hundreds, fast. Ranking uses a Cross-Tower model to precisely score those hundreds, slow. Each stage designed around its own computational budget.

The core idea throughout — user-item compatibility captured in learned representations — has proven remarkably durable. Nearly every component of a modern recommender system is an elaboration of that idea.

Two directions are worth watching.

### Multi-Task Learning (MTL)

Real recommendation systems optimise multiple objectives at once. A video platform cares about clicks, but also watch time, shares, and long-term retention. These objectives often conflict. Optimising purely for clicks surfaces clickbait. Optimising purely for watch time can trap users in recommendation spirals.

Multi-task learning trains a single model jointly on several objectives, sharing representations across tasks while learning task-specific output heads. The shared layers benefit from richer combined signal. The task-specific heads express different preferences for different objectives. How you weight these objectives is a system design decision — and it directly encodes what the platform values.

### Contextual Bandits

Both supervised learning and A/B testing share a structural weakness: they are offline. Train on historical data, deploy, collect new data, retrain. The feedback loop is slow. The model can only learn from interactions that the deployed model itself generated.

Contextual bandits offer a path toward online learning. Each recommendation is a decision under uncertainty: given what we know about the user and context, choose an item and observe the outcome. The model updates continuously, balancing exploitation (recommending items it's confident about) with exploration (occasionally trying uncertain items to gather signal).

In production, bandit approaches are usually applied to specific sub-problems — how much to explore in retrieval, or how to dynamically reweight content types in ranking — rather than replacing the full stack. But the direction is toward systems that adapt in real time, rather than through periodic batch retraining.

That's the journey. From a lookup table to a live, multi-objective, continuously-learning system. Collaborative filtering, all the way down.