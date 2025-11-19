---
title: "Collaborative Filtering"
type: "series_collection"
---

Whenever we discuss about collaborative filtering, the following image is
implicitly made as a anchor point to talk about how
collaborative filtering discovers  'similar users' and use that to
recommend unseen items.


Whenever collaborative filtering is talked about, the following illustration is 
brought up and then "finding users who behave similarly, then recommend items they liked but haven't seen yet" is discussed.

```

          movie 1   movie 2                                 movie n    
        ┌─────────┬─────────┬─────────┬─────────┬─────────┬─────────┐ 
 user 1 │         │    ✓    │         │    ✓    │         │    ✓    │ 
        ├─────────┼─────────┼─────────┼─────────┼─────────┼─────────┤ 
 user 2 │    ✓    │    ✓    │         │         │         │         │ 
        ├─────────┼─────────┼─────────┼─────────┼─────────┼─────────┤ 
        │    ✓    │         │         │    ✓    │    ✓    │    ✓    │ 
        ├─────────┼─────────┼─────────┼─────────┼─────────┼─────────┤ 
        │         │         │    ✓    │         │         │         │ 
        ├─────────┼─────────┼─────────┼─────────┼─────────┼─────────┤ 
        │    ✓    │    ✓    │         │    ✓    │    ✓    │    ✓    │ 
        ├─────────┼─────────┼─────────┼─────────┼─────────┼─────────┤ 
 user m │         │    ✓    │         │    ✓    │         │         │ 
        └─────────┴─────────┴─────────┴─────────┴─────────┴─────────┘ 
        
```
<center><small><b>Fig :</b> The mythical user item interaction matrix.</small></center>

It’s a helpful mental model and historically accurate for early recommender systems.

However, that similar users picture is only a small part of how modern 
recommendation models actually work. Real-world systems rarely operate 
directly on this matrix, and the notion of similarity today is far more 
nuanced than simple row-to-row comparison.

This 5 part series is walkthrough of how collaborative filtering is practiced today. 
We will talk about how the row-to-row comparison idea evolves into one of the 
corner stone component of modern day recommender systems.


**Part 1: Collaborative Filtering - The Foundations & Classic Flaws**

- Introduction - The P(click) Problem
- The "Naive" Approach: Neighborhood-Based CF
- The Classic Foundation: Matrix Factorization (MF)
- The "Zero" Problem: Why Standard MF is Wrong for Clicks

**Part 2: The "Zero" Problem - Solving for Implicit Data**

- Solution 1: Weighted Matrix Factorization (WMF / Implicit ALS)
- Solution 2: Logistic Matrix Factorization (LMF) & The Practical Hurdle of Negative Sampling

**Part 3: The Modern Solution: Scaling with Features & Neural Networks**

- The Scaling Wall: Limitations of Pure Collaborative Filtering
- The Modern Solution: Feature-Based Neural Networks
- The "Magic" Ingredient: How Features are Represented (Embeddings)

**Part 4: Retrieval & Ranking - Modern Recommendation Architectures**

- "Two-Stage" (Retrieval & Ranking) paradigm.
- Architectural Deep Dive 1: The Two-Tower Model (For Retrieval)
- Architectural Deep Dive 2: The Cross-Tower (or Fused) Model (For Ranking)

**Part 5: Evaluation and Pitfalls**

- How Do We Know It's Working? (Evaluation Metrics: Offline, Online, Biases)
- Conclusion: The Journey and What's Next. Multi-Task Learning (MTL), Reinforcement Learning (Contextual Bandits)