---
title: Optimum Aggregate Candidate Pool Selection
tags : [machine-learning, reocmmender-system]
date: 2026-07-27T00:00:00+00:00
start_date: 2026-07-27T00:00:00+00:00
draft: false
type: post
---

# Optimum Aggregate Candidate Pool Selection

Let $U$ be a set of users with request distribution $P(u)$, and let $I$ be a catalog of items.

In large-scale systems, constraints often force serving systems to commit in advance to a single, small shared candidate pool $C \in I_k$ and serve all users from within this bounded set (of size $k$). $$I_k= \\{ C \subseteq I : \vert{}C\vert{} \leq k \\}$$

No universal set will satisfy everyone (short of the entire catalog). Then how do we select a pool that minimizes selection loss and maximizes overall utility across the population?

Let us define the utility of item $i$ to user $u$ as the probability of engagement:

$$f(u, i) = P(\text{click} \mid u, i)$$

To restrict the scope of our discussion here, we will also assume that once a candidate pool is fixed, the downstream ranker serves item to user that maximises utlity from withing $C$ by serving $\arg\max_{i \in C} f(u,i)$ to the user.

So the expected utility across the population, as a function of the candidate pool, is:

$$\mathcal{U}(C) = \sum_{u \in U} P(u) \cdot \max_{i \in C} f(u, i)$$

And the problem is to choose the pool that maximizes this:

$$C^\ast = \operatorname*{arg\\,max}_{C \in I_k}\\;\mathcal{U}(C)$$


## Why Is This Problem Hard?

**[Maximum Coverage Problem][Maximum Coverage Problem]** <br>
Given a universe $U = \\{i_1, i_2, \ldots i_n\\}$ and a collection of subsets $S = \\{S_1, S_2, \ldots, S_m\\}$ where $S_i \subseteq U$ and a budget $k$; select a subcollection $S^\prime \subseteq S$ such that $$\max_{S^\prime \subseteq S} \\, \sum_{i \in \bigcup {S^\prime}} w(i) \qquad \text{s.t.} \quad\vert{}S^\prime \vert{} \le k$$


**Optimum Pool $\mapsto$  Max-Cover**<br>
Set $U$ to be the universe, let each item $i$ correspond to a set $S_i$, and define $f(u,i)= w(u) \text{ If } u \in S_i \text{ else } 0$. Then $\max_{i \in C} f(u,i)$ is exactly *'is u covered by some chosen set'* and $\mathcal{U}(C)$ is exactly the total covered weight.
  
  *It helps thinking of user$\times$item matrix to visualise this reduction.*


## Near-Optimal Solution

So our problem is also NP-hard, ergo, no tractable exact solution exists. However $\mathcal{U}(C)$ has some very useful structural property :

- **Monotone**: adding an item to $C$ can only weakly increase $\max f(u,i)$ for every user, so $\mathcal{U}(C) \leq \mathcal{U}(C')$ whenever $C \subseteq C'$.
- **Submodular** (diminishing returns): for $C \subseteq C'$ and item $i \notin C'$, $$\mathcal{U}(C \cup \\{i\\}) - \mathcal{U}(C) \\;\geq\\; \mathcal{U}(C' \cup \\{i\\}) - \mathcal{U}(C')$$
    Larger the $C$, less likely will adding a new item improve the $\arg\max_{i \in C} f(u,i)$

*Proof Sketch: Each of the user coverage function $\max_{i \in C} f(u,i)$ is monotone submodular. Both properties are closed under non-negative linear combinations.*

Consider the greedy algorithm. Start with empty pool $C = \emptyset$ and repeatedly add the item $i$ from the remaining pool that provides the maximum marginal gain $\mathcal{U}(C \cup \\{i\\}) - \mathcal{U}(C)$ until $\vert{}C\vert{} = k$.


Because $\mathcal{U}$ is monotone submodular, the classic [Nemhauser–Wolsey–Fisher][Nemhauser et al. (1978)] result guarantees that this simple greedy approach achieves at least a $(1 - 1/e)$ approximation of the true optimal pool $C^\ast$

$$\mathcal{U}(C\_{\text{greedy}}) \geq \left(1 - \tfrac{1}{e}\right) \mathcal{U}(C^\ast) \approx 0.632\\, \mathcal{U}(C^\ast)$$

The 63.2% is a worst case lower bound and in practise the realised gain closer to the true optimum.


## Leaky Abstraction Layers

Let's take a closer look at what we optimized for here. The capstone of our expected utility $\mathcal{U}(C)$ is the inconspicuous function $f(u,i)$, which is the probability of a user clicking (or engaging) with the content. More importantly, this is the future probability of that click.

There are two problems with this: We might have millions of users and items, so estimating this for everyone$\times$everything is computationally impractical. Estimating a future probability is inherently difficult.


So we take on two more leaky layers of abstraction to solve this. 
1. Tomorrow, most users are likely to click on what is popular then. *Something is popular because most users are clicking on it*.
2. What was popular yesterday will remain popular tomorrow. *At least the top-1 yesterday would be in top-10 tomorrow.*

Hence we replace $f(u,i)$ with historical click-through rates. The complex, personalized prediction is simply replaced by an ordered list of most popular items.

So if we approximate the `personlised future click probability` with `what will be most popular tomorrow` with
 `what was popular yesterday` and simply do a `ORDER BY clicks DESC LIMIT k` and hope for the best :)



## References
<small>

- [Nemhauser et al. (1978)]: Nemhauser, George L., Laurence A. Wolsey, and Marshall L. Fisher. \"An analysis of approximations for maximizing submodular set functions—I.\" Mathematical programming 14.1 (1978): 265-294.
- _Maximum Coverage Problem_ : [https://en.wikipedia.org/wiki/Maximum_coverage_problem][Maximum Coverage Problem]

[Nemhauser et al. (1978)]:    <http://www.cs.cmu.edu/~aarti/Class/10704_Fall16/submod-max.pdf>
    "Nemhauser, George L., Laurence A. Wolsey, and Marshall L. Fisher. \"An analysis of approximations for maximizing submodular set functions—I.\" Mathematical programming 14.1 (1978): 265-294."
    
[Maximum Coverage Problem]:    <https://en.wikipedia.org/wiki/Maximum_coverage_problem>
        "Maximum Coverage Problem"

</small>
