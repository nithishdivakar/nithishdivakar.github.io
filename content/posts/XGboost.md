---
title: XGBoost
tags : [machine-learning]
date: 2024-04-28T21:30:00+05:30
start_date: 2023-10-25T06:17:00+05:30
draft: false
---

# XGBoost

**Extreme Gradient Boosting** or XGBoost is a technique that has become quite useful for solving prediction problems. XGBoost is also quite interesting academically; for it combines quite few techniques together to give us one robust method. The technique is composed from  gradient boosting, decision trees, matching pursuit and gradient descent in function space among others. In this post, we will explore and derive the inner workings of XGBoost.

## The Regression Problem
We are given a set of samples from population $\\{(y_i,x_i)\\}\_{i=1}^{N}$ which we call a dataset. $y$'s are scalars and $x$ are vectors.

There is also some function $F^{\ast}$ on the population which perfectly determines the entire population i.e. $y = F^{\ast}(x)$. However, this function is unknown and all we have is the dataset.

Regression problem is computing some $\hat{F}$ which is the best approximation  of $F^{\ast}$ that minimises some loss function $L(y,F(x))$ over all values of $(y,x)$.


Different choices of $L$ and restriction on the structrue of $F$ leads to different algorithms. For example; mean squared error and linear function on $x$ gives [linear regession][Linear Regression].


## T.H.E family of functions 
Let assume (to make things easier) that $F$ has a simpler structure. The all powerful $F$ is from the family of functions which are weighted combination of simpler functions. 

$$F(x) = \sum \beta_m h_m(x)$$

We do such approximations all the time. See [mean field approximation for variational inference](https://www.cs.cmu.edu/~epxing/Class/10708-17/notes-17/10708-scribe-lecture13.pdf) for a family which is _product_ of simpler functions. 


This makes our _learning_ easier. It's easier to see if we look at the explict structure of $F$.

$$F(x;\\{\beta_t,\alpha_t\\}) = \sum_t \beta_t h_t(x;\alpha_t)$$

All we need to do now is compute values of parameters $\beta$'s and $\alpha$'s which minimised $L$.

By the way, did we just sneak in a constraint on structure of $F$ ??? Are all the $h$'s same or different? 

Well the structure allows everything. B.U.T, for XGBoost, all $h$'s are [decision trees][Decision Tree].


## Gradient Boosting
> All we need to do is compute $\beta$'s and $\alpha$'s

This is easier said than done.


Joint optimisation will lead to a situation where adjusting $\alpha$ of one tree would require us to adjust $\alpha$ of another. And $\alpha$ of a decision tree determines where to add a split. This is not productive at all as we will have to throw away the existing tree and construct a whole new tree.  In optimisation land this is classif case of a dis-continous objective.


So lets fix that problem by fixing things. We first find the best parameters for $h_1$ and then never change it. Then find best parameters for $h_2$ and so on. This idea is called "Gradient Boosting" where we restrict $F$ to the family of *additive expansion* is from the paper [Greedy Function Approximation: A Gradient Boosting Machine][Friedman (2001)]. This stage wise stratergy is also very similar to [matching pursuit algorithm][Mallat and Zhang (1993)] in signal processing. 

> Given an loss function $l$ and parameterised objective function $f(x;\theta)$, we can find best $\theta$ which minimises $l$ using [Gradient Descent]. $$\theta \gets \theta - \gamma \nabla_l f$$

Let say we are following the approach of fixing things as listed above. We are in some intermediate step $m$. We have already found and fixed the parameters of $\beta_{1:m-1}$ and $\alpha_{1:m-1}$ and the current best regressor we have is  

$$F_{t-1}(x) = \sum_{i=1}^{t-1} \beta_i h_i(x; \alpha_i)$$

We want to add to this a $p_t(x) = \beta_t h_t(x;\alpha_t)$ and reduce the error further.

$$ l_t = \operatorname{arg min} \sum_{i=1}^{N} \operatorname{L}(y_i, F_{t-1}(x)+f_t(x))$$ 

In this situation we can find best parameters for $f_t$ using gradient descent on function space. But we need $\frac{\partial l_t}{\partial f_t}$.
Let ignore a few things a write this situation simply as

$$l = \operatorname{L}(y, p+f(x))$$

If we squint our eyes, r.h.s looks like a function with a fixed point $p$ and a small delta $f(x)$. We can expand it around the fix point using second order [taylor's series][Taylor Series] approximation.

$$l = \operatorname{L}(y, p) + \nabla_p \operatorname{L}(y,p) f(x) + \nabla_p^2 \operatorname{L}(y,p) \frac{f(x)^2}{2} $$

This immediatly gives us an opening to get the derivative of loss w.r.to $f(x)$.

$$\frac{\partial l}{\partial f} =0 +  \nabla_p \operatorname{L}(y,p) + \nabla_p^2 \operatorname{L}(y,p) f(x)  = \nabla_p^2 \left( \frac{\nabla_p}{\nabla_p^2} + f(x)\right)$$


Since optimum occurs at the saddle point, the optimum $f(x)$ is the one which makes the derivative zero. So at $\frac{\partial l}{\partial f} =0$ we have 
$$f(x) = - \frac{\nabla_p}{\nabla_p^2}$$

Ultimately, to find the best additive function to the model at stage $t$, we simply have to fit $h_t(x)$ to predict the residuals $\\{-{\nabla_p}/{\nabla_p^2} \\}$. This again is another regression problem.

$$h_t \leftrightsquigarrow \left\\{\left(x_i,-{\nabla_{F_{t-1}(x_i)}}\middle/{\nabla^2_{F_{t-1}(x_i)} }\right)\right\\}_{i=1}^{n}$$

**Addendum**: What if we use first order taylor's series approximation instead on the loss function? What will be the residuals in the last step? 

## XGBoost Algorithm
- We begin by setting $h_0$ to simply predict $\mathbb{E}(y)$. 
- At each step we first compute the residuals
$$ r_i = -\frac{\nabla_{\bar{y}\_i}\operatorname{L}(y_i, \bar{y}\_i)}{\nabla^2_{\bar{y}\_i}\operatorname{L}(y_i, \bar{y}\_i)}  ; with~\bar{y}\_i = F_{t-1}(x_i)$$
*Note:* Most loss functions have easy analytical form of first and second derivatives e.g. mse loss.
- Fit $h_t$ to predict $r_i$ given $x_i$.
- Compute $\beta_t$ using line search which will optimise
$$\operatorname{arg min}\_{\beta_t}\operatorname{L}(y, F_{t-1} + \beta_t h_t)$$
- Update the model as 
$$F_t = F_{t-1} + \beta_t h_t$$
 

## Addendum
There is a lot more to implementing XGBoost. Most of it is centered around the "fitting a new tree to residuals" part. A few scenarios that arise in this step are
- How to prevent overfitting of the intermediate tree on residuals?
- How to let user direct/control some part of the tree construction so that the complexity vs performance tradeoff can be tunable?

[Chen et al. (2016)] gives an excellet account of these issues among other, but the official [XGBoost library' documentation](https://xgboost.readthedocs.io/en/latest/tutorials/model.html) is also a great source for discussion on these topics.


## References
<reference>
 <small>


- [Friedman (2001)]: Friedman, Jerome H. "_Greedy function approximation: a gradient boosting machine_" In Annals of statistics , (2001)


- [Mallat and Zhang (1993)]: Mallat, Stephane G and Zhang, Zhifeng "_Matching pursuits with time-frequency dictionaries_" In IEEE Transactions on signal processing 41, (1993)


- [Chen et al. (2016)]: Chen, Tianqi and Guestrin, Carlos "_Xgboost: A scalable tree boosting system_" In Proceedings of the 22nd acm sigkdd international conference on knowledge discovery and data mining pp. 785--794, (2016)


- _[Decision Tree]_<br><small>_`https://en.wikipedia.org/wiki/Decision_tree_learning`_ </small>


- _[Gradient Descent]_<br><small>_`https://en.wikipedia.org/wiki/Gradient_descent`_ </small>


- _[Linear Regression]_<br><small>_`https://en.wikipedia.org/wiki/Linear_regression`_ </small>


- _[Taylor series]_<br><small>_`https://en.wikipedia.org/wiki/Taylor_series`_ </small>


[Friedman (2001)]:    <https://projecteuclid.org/journals/annals-of-statistics/volume-29/issue-5/Greedy-function-approximation-A-gradient-boosting-machine/10.1214/aos/1013203451.pdf>
    "Friedman, Jerome H. \"Greedy function approximation: a gradient boosting machine\" In Annals of statistics , (2001)"


[Mallat and Zhang (1993)]:    <http://www.iro.umontreal.ca/~pift6080/H09/documents/papers/sparse/mallat_zhang_matching_pursuit.pdf>
    "Mallat, Stephane G and Zhang, Zhifeng \"Matching pursuits with time-frequency dictionaries\" In IEEE Transactions on signal processing 41, (1993)"


[Chen et al. (2016)]:    <https://arxiv.org/pdf/1603.02754.pdf>
    "Chen, Tianqi and Guestrin, Carlos \"Xgboost: A scalable tree boosting system\" In Proceedings of the 22nd acm sigkdd international conference on knowledge discovery and data mining pp.785--794, (2016)"


[Decision Tree]:    <https://en.wikipedia.org/wiki/Decision_tree_learning>
    "Decision Tree"


[Gradient Descent]:    <https://en.wikipedia.org/wiki/Gradient_descent>
    "Gradient Descent"


[Linear Regression]:    <https://en.wikipedia.org/wiki/Linear_regression>
    "Linear Regression"


[Taylor series]:    <https://en.wikipedia.org/wiki/Taylor_series>
    "Taylor's Series"

</small>
</reference>
