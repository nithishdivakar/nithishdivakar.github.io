---
title: XGBoost
tags : [machine-learning]
date: 2023-10-25T06:17:00+05:30
start_date: 2023-10-25T06:17:00+05:30
draft: true
---

# XGBoost

**Extreme Gradient Boosting** or XGBoost is a technique that has become quite useful for solving regression problems. XGBoost is also quite interesting academically; for it combines quite few techniques together to give us one robust method. It has gradient boosting, decision trees, matching pursuit, steepest descent in function space among others. Lets explore and derive how XGBoost works. 

## The Regression Problem
Lets start with the basics. We are given a set of samples from population $\\{y_i,x_i\\}\_{1}^{N}$ or a dataset. $y$'s are scalars and $x$ are vectors. There is also some function $F^{\ast}$ on the population which perfectly determines the entire population i.e. $y = F^{\ast}(x)$. However, this function is unknown and all we have is the dataset. Regression problem is computing $\hat{F}$ which is the best approximation  of $F^{\ast}$ that minimises some loss function $L(y,F(x))$ over all values of $(y,x)$.


Different choices of $L$ and restriction of the form of $F$ leads to different algorithms. Say, mean squared error and linear function on $x$ gives [linear regession][Linear Regression].


## T.H.E family of functions 
Let assume (cause why not) that $F$ has a simpler structure. The all powerful $F$ is from the family of functions which are weighted combination of simpler functions. 

$$F(x) = \sum \beta_m h_m(x)$$

We do such approximations all the time. See [mean field approximation for variational inference](https://www.cs.cmu.edu/~epxing/Class/10708-17/notes-17/10708-scribe-lecture13.pdf) for a family which is _product_ of simpler functions. 


This makes our _learning_ easier. Its easier to see if we look at the explict for of our assumed stricure of $F$.

$$F(x;\\{\beta_i,\alpha_i\\}) = \sum \beta_m h_m(x;\alpha_m)$$

All we need to do now is compute values of parameters $\beta$'s and $\alpha$'s which minimised $L$.

By the way, did we just sneak in a constraint on structure of $F$ ??? Are all the $h$'s same or different? 

Well the structure allows everything. B.U.T, for XGBoost, all $h$'s are [Decision Trees][Decision Tree].


## Gradient Boosting
> All we need to do is compute $\beta$'s and $\alpha$'s

But how?? `¯\_(ツ)_/¯`

Its very difficult. Joint optimisation will lead to a situation where adjusting $\alpha$ of one tree would require us to adjust $\alpha$ of another. And $\alpha$ of a tree is basically the decision of where to split. This is not productive at all or in optimisation land, not continous objective.

So lets fix that problem by fixing things. We find the best parameters of $h_1$ and then never change it. Then find best parameters of $h_2$ and so on. This idea is "Gradient Boosting" from the paper [Greedy Function Approximation: A Gradient Boosting Machine by Friedman][Friedman (2001)]. Lets quickly derive it.

> Given an loss function $l$ and parameterised objective function $f(x;\theta)$, we can find best $\theta$ which minimises $l$ using [Gradient Descent]. $$\theta \gets \theta - \gamma \nabla_l f$$

Let say we are following the approach of fixing things as listed above. We are in some intermediate step $m$. We have already found and fixed the parameters of $\beta_{1:m-1}$ and $\alpha_{1:m-1}$ and the current best regressor we have is  

$$F_{m-1}(x) = \sum_{i=1}^{m-1} \beta_i h_i(x; \alpha_i)$$

We want to add to this a $p_m(x) = \beta_mh_m(x;\alpha_m)$ and reduce the error further.

$$\operatorname{argmin} \sum_{i=1}^{N} L(y_i, F_{m-1}(x)+p_m(x))$$ 


---

- [Chen et al. (2016)]
- https://xgboost.readthedocs.io/en/latest/tutorials/model.html
- https://hastie.su.domains/ElemStatLearn/printings/ESLII_print12.pdf#page=380

![image](https://docs.aws.amazon.com/images/sagemaker/latest/dg/images/xgboost_illustration.png)

===

XGBoost stands for "Extreme Gradient Boosting", where the term "Gradient Boosting" originates from the paper [Greedy Function Approximation: A Gradient Boosting Machine by Friedman][Friedman (2001)]

## Boosting

If F is the final function, which is used for solving regression. Say we are only interested in additive expansions. 

$$F(x;\alpha, \beta) = \sum_i \beta_i h_i(x; \alpha_i)$$


This form allows for a general structure of boosting where the $n^{th}$ function $h_n$ learns to predict the part of the target that the other $h_1, \ldots h_{n-1}$ functions missed; or residue. 


>  Given any approximator $F_{m−1}(x)$, the function $\beta_m h(x;a_m)$ can be viewed as the best greedy step toward the data-based estimate of $F^* (x)$, under the constraint that the step "direction" $h(x; a_m)$ be a member ofthe parameterized class offunctions $h(x;a)$. It can thus be regarded as a steepest descent step under that constraint. By construction, the data-based analogue of the unconstrained negative gradient. -[Friedman 2001]


## Boosting Old
Boosting is an ensembling algorithm which primarily reduces bias (and also variance). It combines many weak learners to make a strong learner.

The main idea of boosting is to learn a ensemble of trees whose output can be summed to get the final score. 
$$F(x) = \sum_t f_t(x)$$
With $p_i = F(x_i)$, the objective function is 
$$\operatorname{argmin}\_{F} l(y_i, p_i)$$
This objective includes functions as parameters and cannot be computed using traditional methods. Hence trees are learnt in a iterative (greedy) manner.
$$\mathbb{L}_t = \operatorname{argmin}\_{f_t} \sum_i l(y_i, p^{t-1}_i+f_t(x_i))$$

Boosting works by iteratively learning weak learners and adding it to the strong learner. After the latest weak learner is added, the data samples are \textbf{re-weighted} to reflect misclassified and correctly classified samples. The weights of misclassified samples are increased and correctly classified samples  are diminished to allows future weak learner to concentrate on misclassified samples. 





## Algorithm

XGBoost is a decision-tree-based ensemble Machine Learning algorithm that follows the gradient boosting framework.
$$F_t(x) = F_{t-1}(x) + f_t(x)$$
One key difference is it uses _second order taylor approximation_ for the loss function

$$L = l(y,p+f(x))$$
$$=l(y,p) + \nabla_{p} l(y,p)f(x)+ \nabla^2_{p} l(y,p)\frac{f(x)^2}{2}$$
$$\frac{\partial L}{\partial f} = \nabla_{p} l(y,p)+ \nabla^2_{p} l(y,p)f(x)=\nabla^2_{p}\left(\frac{\nabla_{p} }{\nabla^2_{p} } + f(x)\right)$$


- [input] $D=\{(x_i,y_i)\}$, loss function $L(y,F(x))$
- [initialise] the model with a constant (typically mean $\mathbb{E} y_i$)
    $$F_0(x) = \operatorname{argmin}_{\gamma}\sum_i L(y_i,\gamma)$$
- For $t \in 1 \ldots T$
    - [Compute gradients and hessians]
    \begin{align*}
        \nabla_F  &= \frac{\partial L(y_i,F_{t-1}(x_i))}{\partial F_{t-1}(x_i)}
        &%\\
        \nabla^2_F  &= \frac{\partial^2 L(y_i,F_{t-1}(x_i))}{\partial F_{t-1}(x_i)^2}
    \end{align*}
    
    - [Fit a weak learner on residuals] 
     $$f_t \leftrightsquigarrow \left\\{\left(x_i,-\frac{\nabla_F}{\nabla^2_F }\right)\right\\}$$
      
     $$f_t = \operatorname{argmin}_f \sum_i \frac{1}{2} \nabla^2_F
    \left(-\frac{\nabla_F}{\nabla^2_F } - f(x_i)\right)^2 $$
    - [Update model]
    $$F_t = F_{t-1}+\gamma_t f_t$$




## Notes on [Greedy Function Approximation: A Gradient Boosting Machine by Friedman][Friedman 2001]
- $\{y_i,x_i\}_{1}^{N}$ is data and goal is to learn the best approximation $\hat{F}(x)$ of the actual function $F(x)$ by minimising some loss criteria $L(y,F(x))$.

- For the scope of this paper, we restrict the possible $F$ to a family of additive expansions.
$$F(x) = \sum \beta_m h(x)$$
- In signal processing this stagewise strategy is called "matching pursuit" [Mallat and Zhang (1993)]

## References
<reference>
 <small>


- [Friedman (2001)]: Friedman, Jerome H. "_Greedy function approximation: a gradient boosting machine_" In Annals of statistics , (2001)


- [Mallat and Zhang (1993)]: Mallat, Stephane G and Zhang, Zhifeng "_Matching pursuits with time-frequency dictionaries_" In IEEE Transactions on signal processing 41, (1993)


- [Chen et al. (2016)]: Chen, Tianqi and Guestrin, Carlos "_Xgboost: A scalable tree boosting system_" In Proceedings of the 22nd acm sigkdd international conference on knowledge discovery and data mining pp. 785--794, (2016)


- _[Decision Tree]_<br><small>_`https://en.wikipedia.org/wiki/Decision_tree_learning`_ </small>


- _[Gradient Descent]_<br><small>_`https://en.wikipedia.org/wiki/Gradient_descent`_ </small>


- _[Linear Regression]_<br><small>_`https://en.wikipedia.org/wiki/Linear_regression`_ </small>


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

</small>
</reference>
