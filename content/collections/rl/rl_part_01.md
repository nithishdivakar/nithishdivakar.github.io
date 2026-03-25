---
date: 2026-03-25 00:00:00 +0000
layout: post
level: h1
slug: '01'
status: todo
tags : [reinforcement learning]
title: Reinforcement Learning - Mathematical Tools
type: "series_collection"
---

## Expectation and the Log-Derivative Trick

Throughout this note we will frequently differentiate expectations whose underlying distribution depends on a parameter $\theta \in \mathbb{R}^d$. The fundamental identity that makes this tractable is the *log-derivative* (or *score function*) identity.

**Proposition:** (Log-Derivative Identity)
Let $p_\theta(x)$ be a density parameterized by $\theta$, differentiable in $\theta$ for all $x$, and let $f(x)$ be independent of $\theta$. Then

$$
\nabla_\theta \mathbb{E}\_{x \sim p_\theta}[f(x)] = \mathbb{E}\_{x \sim p_\theta}\\!\left[f(x)\\,\nabla_\theta \log p_\theta(x)\right]
$$

*Proof:*
By Leibniz's rule (assuming sufficient regularity to interchange differentiation and integration):
$$
\begin{aligned}
    \nabla_\theta \mathbb{E}\_{x \sim p_\theta}[f(x)]
    &= \int f(x)\\,\nabla_\theta p_\theta(x)\\,dx
    \\\\
    &= \int f(x)\\,\frac{\nabla_\theta p_\theta(x)}{p_\theta(x)}\\,p_\theta(x)\\,dx
    \\\\
    &= \mathbb{E}\_{x \sim p_\theta}\\!\left[f(x)\\,\nabla_\theta \log p_\theta(x)\right]
\end{aligned}
$$

The term $\nabla_\theta \log p_\theta(x)$ is the *score function*. Its key virtue is that we can estimate the gradient using only *samples* from $p_\theta$---no analytical gradient of $p_\theta$ itself is needed. This identity is the engine behind every policy gradient algorithm.

**Remark:** (Policy Gradient via the Log-Derivative Trick)
A canonical application is maximising an expected reward. Let $\pi_\theta(a \mid s)$ be a parametric policy and let $R(a, s)$ be a reward function that is independent of $\theta$. 

Define the objective
$$
    J(\theta) = \mathbb{E}\_{a \sim \pi_\theta(\cdot \mid s)}\\!\left[R(a, s)\right]
$$
Applying Log-Derivative Identity $\nabla \mathbb{E}\_{p}[f] = \mathbb{E}\_{p}\left[f\nabla \log p\right]$ with $f = R(a,s)$ and $p = \pi_\theta(\cdot \mid s)$ gives
$$
    \nabla_\theta J(\theta)
    = \mathbb{E}\_{a \sim \pi_\theta(\cdot \mid s)}\left[R(a, s)\nabla_\theta \log \pi_\theta(a \mid s)\right]
$$
This expectation can be estimated by Monte Carlo: collect a batch of actions $a^{(i)} \sim \pi_\theta(\cdot \mid s)$, evaluate their rewards, and form the estimator
$$
    \widehat{\nabla_\theta J}(\theta)
    = \frac{1}{N}\sum_{i=1}^{N} R(a^{(i)}, s)\nabla_\theta \log \pi_\theta(a^{(i)} \mid s)
$$
Crucially, $R$ need not be differentiable---or even analytically known---since only $\nabla_\theta \log \pi_\theta$ appears in the estimator. The update has a natural interpretation: directions in parameter space that produced high-reward actions are reinforced, while those that produced low-reward actions are suppressed. This is precisely the REINFORCE estimator [Williams (1992)][Williams (1992)], and it underpins modern policy-gradient methods such as TRPO and PPO.


## Variance Reduction and the Baseline Theorem

Monte Carlo estimators of gradients are unbiased but exhibit high variance. A central technique is subtracting a *baseline*.

**Proposition:** (Baseline Theorem)
Let $b(s)$ be any function independent of action $a$. Then
$\mathbb{E}\_{a \sim \pi_\theta(\cdot|s)}\\!\left[\nabla_\theta \log \pi_\theta(a|s)\cdot b(s)\right] = 0.$

*Proof:*
$b(s)\nabla_\theta \sum_a \pi_\theta(a|s) = b(s)\nabla_\theta 1 = 0.$

*Detailed Proof:*
We begin with the identity that the sum of probabilities over the action space must equal unity:$\sum_a \pi_\theta(a|s) = 1$.
Differentiating both sides with respect to $\theta$ gives

$$\nabla_\theta \sum_a \pi_\theta(a|s) = \nabla_\theta 1 = 0$$

Moving the gradient through the sum -- $\sum_a \nabla_\theta \pi_\theta(a|s) = 0$ -- and applying the log-derivative identity $\nabla \pi = \pi\nabla \log \pi$ we obtain:

$$\sum_a \pi_\theta(a|s)\nabla_\theta \log \pi_\theta(a|s) = 0.$$

This is precisely $\mathbb{E}\_{a \sim \pi_\theta(\cdot|s)}\\!\left[\nabla_\theta \log \pi_\theta(a|s)\right] = 0$. Since $b(s)$ is independent of $a$, it factors out of the expectation:

$$\mathbb{E}\_{a \sim \pi_\theta(\cdot|s)}\\!\left[\nabla_\theta \log \pi_\theta(a|s)\cdot b(s)\right] = b(s)\cdot 0 = 0.$$

Thus, the proposition.

**Remark:** (Baseline Subtraction and the Advantage Function)
The Baseline Theorem has an immediately useful consequence: for any baseline $b(s)$ independent of $a$, the modified estimator
$$
    \nabla_\theta \log \pi_\theta(a|s)\cdot\bigl(f(s,a) - b(s)\bigr)
$$
remains an *unbiased* estimator of $\nabla_\theta J(\theta)$, since subtracting $b(s)$ contributes zero in expectation. The freedom to choose $b(s)$ is then used to *reduce variance*: the optimal baseline is the one that minimises the variance of the estimator without introducing bias.

The canonical choice is $b(s) = V^\pi(s)$, the *state value function*, defined as the expected cumulative reward from state $s$ under policy $\pi$. This yields the *advantage function*
$$
    A^\pi(s, a) = Q^\pi(s,a) - V^\pi(s),
$$
where $Q^\pi(s,a)$ is the action-value function. Intuitively, $A^\pi(s,a)$ measures how much better action $a$ is compared to the average action taken by $\pi$ in state $s$ --- a positive advantage means the action is better than average, and a negative advantage means it is worse. The policy gradient then becomes
$$
    \nabla_\theta J(\theta) = \mathbb{E}\_{a \sim \pi_\theta(\cdot|s)}\\!\left[\nabla_\theta \log \pi_\theta(a|s)\cdot A^\pi(s,a)\right],
$$
which updates the policy to increase the probability of advantageous actions and decrease the probability of disadvantageous ones. The advantage function is the central quantity in all modern policy-gradient methods for LLM alignment, including PPO and GRPO.


## Synopsis
This section builds a single pipeline for computing tractable, low-variance policy gradients in three steps.
1. **Log-derivative identity.** The gradient of an expectation under $p_\theta$ is rewritten as another expectation under $p_\theta$, making it estimable from samples without differentiating through the distribution directly.
    $$\nabla \\,\mathbb{E}\_{p}[f] = \mathbb{E}\_{p}\\!\left[f\\,\nabla \log p\right]$$
2. **Policy gradient.** Setting $f = R$ in the identity above yields an unbiased, sample-based estimator of $\nabla_\theta J(\theta)$, where $J(\theta) = \mathbb{E}[R]$, even when the reward $R$ is a black box.
3. **Baseline subtraction and the advantage function.** Subtracting any state-dependent baseline $b(s)$ from $R$ leaves the estimator unbiased but reduces its variance. The optimal choice $b(s) = V^\pi(s)$ produces the advantage function $A^\pi(s,a) = Q^\pi(s,a) - V^\pi(s)$, the central quantity in all modern policy-gradient methods.



## References
<reference>
<small>

- [Williams (1992)]: Ronald J Williams. Simple statistical gradient-following algorithms for connectionist reinforcement learning. Machine learning, 8:229–256, 1992.


[Williams (1992)]: <https://link.springer.com/content/pdf/10.1007/BF00992696.pdf>
    "Ronald J Williams. Simple statistical gradient-following algorithms for connectionist reinforcement learning. Machine learning, 8:229–256, 1992."
    
</small>
</reference>