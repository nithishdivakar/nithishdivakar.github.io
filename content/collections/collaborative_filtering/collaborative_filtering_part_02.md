---
date: 2024-01-01 00:00:00 +0000
layout: post
level: h1
slug: '02'
status: done
title: 'Collaborative Filtering Part 02 - The "Zero" Problem - Solving for Implicit Data'
---

# Collaborative Filtering Part 02

In Part 1, we discussed predicting $P(click)$ using an interaction matrix. However, we concluded that traditional matrix factorization is not viable when the matrix contains empty cells.

Our approach should account for the uncertainty of probability of a click for those empty cells. So we pivot: instead of trying to factorize a full matrix, we treat this as an **Optimisation Problem** over the data we actually have.

## Minimising the Disagreements

We no longer have a full user-item matrix. Instead, we have a collection of specific observations; user, item and outcomes of their interactions.

$$ \Omega = \\\{(u,i,r_{ui})\\\}$$

where $r_{u,i}$ is $1$ if the user clicked on item $i$ after it begin shown and 0 if they saw it and didnt't click. A key distinction: regardless of click, the user saw the item. Both values represent real observations.

*Quick recap: If $p_u$ is the latent features of a user $u$, $q_i$ is the latent features of an item $i$.*

Our objective is to find a latent representation that minimises our prediction error. Essentially, $r_{ui}$ and $p_u^Tq_i$ must agree as much as possible. Analytically, 

$$ \min  \sum_{\Omega} (r_{ui} - p_u^T q_i)^2 $$

This is our **loss function**. A loss function consolidates all the disagreements into one scalar value which we try to minimise.

The term $(r_{ui} - p_u^T q_i)$ represents disagreement between our model and reality; *residuals*. By squaring the residuals, the large errors are penalised more heavily forcing the model to minimise disagreements.

## The Catch

The $\Omega$ formulation assumes we have clean observations of both clicks and non-clicks. In practice, collecting reliable negatives is harder than it sounds.

Consider a user scrolling through a feed of 20 items and clicking one. What do we record for the other 19? Did they see all of them? Did they notice item #14 but decide against it, or did it never register? Was item #3 below the fold and never actually rendered on screen? The line between "saw and rejected" and "never really saw" is blurry, and most systems can't draw it reliably.

What we can say with confidence is much simpler:
- An item was clicked (definite positive)
- Everything else (unknown)

This is called **implicit feedback**. We only observe positive signal. The absence of a click tells us nothing on its own.

So how do we deal with this?

## Weighted Matrix Factorization (WMF)
> Treat all unobserved interactions as weak negatives, but don't trust them equally.

We bring back the full matrix, but we assign a **confidence weight** $c_{ui}$ to each cell:

$$\min \sum_{u,i} c_{ui} (r_{ui} - p_u^T q_i)^2$$


The weight $c_{ui}$ controls how much the model cares about getting cell $(u,i)$ right. This lets us express something nuanced: we have a signal for every cell, but we trust some signals far more than others.

Concretely, we define confidence as:


$$c_{ui} = 1 + \alpha \cdot f_{ui}$$

where $f_{ui}$ is the raw interaction frequency and $\alpha$ is a tunable scaling factor.

This gives us a natural confidence spectrum:

- A user who played a song 50 times $\implies$ $r_{ui} = 1$, high $c_{ui}$
- A user who played a song once $\implies$ $r_{ui} = 1$, modest $c_{ui}$
- An item the user never saw $\implies$ $r_{ui} = 0$, $c_{ui} = 1$

This is the algorithm commonly known as **Implicit ALS** (Alternating Least Squares), and it scales well because the math works out to a closed-form update at each step.

The weakness: we're still telling the model that every unseen item is a mild negative. For a user who loves jazz, every unseen jazz album is being treated as a weak dislike. At scale, this introduces a systematic bias.


## Weighted Matrix Factorization (WMF)

> Treat all unobserved interactions as weak negatives, but don't trust them equally.

We bring back the full matrix, but attach a **confidence weight** $c_{ui}$ to each cell:

$$\min \sum_{u,i} c_{ui} (r_{ui} - p_u^T q_i)^2$$

The weight $c_{ui}$ controls how much the model cares about getting cell $(u, i)$ right. We define it as:

$$c_{ui} = 1 + \alpha \cdot f_{ui}$$

where $f_{ui}$ is the raw interaction count and $\alpha$ is a tunable scaling factor. This gives us a natural confidence spectrum:

- A user who played a song **50 times** → $r_{ui} = 1$, high $c_{ui}$
- A user who played a song **once** → $r_{ui} = 1$, modest $c_{ui}$
- An item the user **never saw** → $r_{ui} = 0$, $c_{ui} = 1$

The model learns to fit "things we know to be true" signals tightly, while tolerating more error on uncertain observations.

This is the algorithm commonly known as **Implicit ALS** (Alternating Least Squares), and it scales well because the math works out to a closed-form update at each step.

### Alternating Least Squares (ALS) Derivation

*This section derives the ALS update rules. Math heavy, safe to skip. The key takeaway is at the end of this section.*

Let $P \in \mathbb{R}^{m \times k}$, $Q \in \mathbb{R}^{n \times k}$, and $C \in \mathbb{R}^{m \times n}$ be the confidence matrix. The full loss is:

$$\mathcal{L}(P, Q) = \\|C \odot (R - PQ^T)\\|_F^2$$

This is non-convex in $P$ and $Q$ jointly, but convex in each separately. So we can fix one, solve the other in closed form, update and itertate towards a lower loss value.


- *Fixing $Q$, solving for $p_u$:*
  Let $C_u = \text{diag}(c_{u1}, \dots, c_{un})$. The per-user loss reduces to $\mathcal{L}\_u = \\|C_{u}^{1/2}(r_u - Qp_u)\\|^2$, a standard [weighted least squares](https://en.wikipedia.org/wiki/Weighted_least_squares#Motivation) problem. Setting $\nabla_{p_u}\mathcal{L}_u = 0$:
  
  $$p_u = (Q^T C_u Q)^{-1} Q^T C_u r_u$$
- *Fixing $P$, solving for $q_i$:* By symmetry

  $$q_i = (P^T C_i P)^{-1} P^T C_i r_i$$

The algorithm
- Initialise P, Q randomly
- Repeat until convergence
    -  for each user u:
        - $p_u = (Q^T C_u Q)^{-1} Q^T C_u r_{u}$
    -  for each item i:
        - $q_i = (P^T C_i P)^{-1} P^T C_i r_i$

**The key takeaway:** ALS alternates between re-solving all user vectors and all item vectors, each time computing an exact closed-form update. Every iteration is guaranteed to reduce the loss. In practice it converges in a handful of iterations.

As each user and item update is independent, both steps parallelise trivially; making WMF practical at the scale of millions of users and items through parallelism.

### So what's wrong with WMF?

WMF works by pulling every unobserved cell toward zero with a small but nonzero weight. This is a practical compromise, but it encodes a quiet assumption: every item a user hasn't interacted with is slightly bad for them.

At scale, this compounds quietly. Popular items accumulate interactions across many users, so the model sees plenty of positive signal to counteract the weak negatives. Meanwhile niche items accumulate false negatives quietly.

The root cause is structural. WMF must say something about every cell, so it assigns weak beliefs everywhere.

We must allow the model to have no opinion on items where there are no interactions. *Negative Sampling.*


## Logistic Matrix Factorization (LMF)
*\... and Negative Sampling*

> Only learn from what you've seen ... and a few carefully chosen counterexamples.

Quick recap from part 1 where we said, 
$$P(click \mid \\\{u, i\\\}) = \sigma(p_u^T q_i)$$

The $\sigma(\square)$ is new as we are now modelling probabilities and sigmoid function properly bound the output as a probabilities. $\sigma(z) = \frac{1}{1+e^{-z}}$.

If we train this against the full matrix, we're back to the same opinion problem as WMF. Every unobserved cell is a negative.

So instead, for each user we take their clicks as positives and sample a small number of unobserved items as negatives. Everything else, no opinion. The model simply doesn't model them. 

This is now a [logistic regression](https://en.wikipedia.org/wiki/Logistic_regression) problem over a chosen set of observations. The standard way to fit logistic regression is through [Maximum Likelihood Estimation (MLE)](https://en.wikipedia.org/wiki/Maximum_likelihood_estimation). The resulting loss is binary cross-entropy:

LMF maximises log-likelihood over positives and sampled negatives only 

$$\mathcal{L}(P,Q) = - \sum_{(u,i) \in \text{clicks}} \log \sigma(p_u^T q_i) - \sum_{(u,j) \in \text{sampled}} \log(1 - \sigma(p_u^T q_j))$$

But now the model's quality depends entirely on how we choose negatives.

### Sampling Negatives

- Uniform sampling: Pick any unseen item at random with equal probability ... but if item X has been seen by 80% of users, it almost never appears as a negative even though it should for the 20% who haven't engaged with it. Undersamples popular items.
- Popularity-based sampling: If a user has never clicked on a widely-loved item, that's more informative than never clicking on an obscure one. So sample negatives proportional to item popularity. 
  $$P(\text{sample item } i) \propto f_i^\alpha$$
  where $f_i$ is the item's interaction frequency and $\alpha \in (0,1)$ is a smoothing factor (commonly $0.75$, see [word2vec](https://arxiv.org/abs/1301.3781)). 

- Hard negative sampling: Deliberately sample items the model currently thinks the user *would* like, but hasn't clicked. See *Dynamic Negative Sampling* in [this paper](https://wnzhang.net/papers/lambdarankcf-sigir.pdf). Also [this](https://www.yuan-meng.com/posts/negative_sampling/) deep dive for a thorough treatment of hard negative strategies in production systems.

In practice, most production systems use popularity-based sampling as the default, with a fraction of hard negatives mixed in.


## The Cold Start Problem

WMF and LMF solve the zero problem from different directions. WMF keeps all the data but up-weights what it trusts. LMF throws most of the data away and samples strategically. Both work and both are still widely used in production today.

But they share a deeper limitation.

Both models learn by adjusting $p_u$ and $q_i$ vectors to agree with observed interactions ... and therein lies the flaw. The whole system breaks down when there are no observations to learn from.

This surfaces in two concrete scenarios:

**New user** A user signs up and hasn't clicked anything. So we have no interactions to learn $p_u$ from.

**New item** A new piece of content is added to the catalogue. No user has interacted with it yet, so $q_i$ is uninitialised. The item is effectively invisible.



This is the **cold start problem**. WMF and LMF have no mechanism to handle it because they are built entirely on interaction history. They cannot reason about a user an item from its inherent features. They only know what has been clicked.

The fix requires a fundamentally different approach,  where the system understands *who* the user is and *what* the item is, independent of past interactions.

*Read more in [Part 3](../03)*