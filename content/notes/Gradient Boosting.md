---
title : Gradient Boosting
tags : [machine-learning]
date: 2022-04-14T04:00:00+05:30
draft: false
---
# Gradient Boosting
The general framework of Boosting is learners are added in greedy manner to minimise loss. 
$$F_t(x) = F_{t-1}(x) + f_t(x)$$
At the $t^{th}$ step, we are interested in learning the function $f$ which minimised the loss. The value of loss function at this point is given by

$$\begin{aligned}
    L &= l(y,p+f(x))
    \\\\
    &=l(y,p) + \nabla_{p} l(y,p)f(x)
\end{aligned}$$

The last step is from first order taylor series approximation of $l$.
$$f(x) = f(a) + (x-a) f^{\prime}(a)$$


We have trying find $f$ which minimises the loss  $L$.  So, we should move in negative gradient direction in function space. 
\begin{align*}
    F_t & \gets F_{t-1}-\gamma_t  \frac{\partial L}{\partial f}
    \\\\
    \frac{\partial L}{\partial f}&= \nabla_{p} l(y,p)=-r
\end{align*}

Following this, all we need to do is at step $t$, we find the learner which best approximates the pseudo-residuals $r$

**Algorithm**: Gradient Boosting
- [**input**] Dataset $D=\\{(x_i,y_i)\\}$, loss function $L$
- [**initialise**] the model with a constant (typically mean $\mathbb{E} y_i$)
    $$F_0(x) = \operatorname*{arg\\,min}_{\gamma}\sum_i L(y_i,\gamma)$$
-  For $t \in 1 \ldots T$
    - [**Compute pseudo residuals**]
    $$r_{it} = -\frac{\partial L(y_i,F_{t-1}(x_i))}{\partial F_{t-1}(x_i)}$$
    - [**Fit a weak learner on residuals**] 
     $$f_t \leftrightsquigarrow \\{(x_i,r_{it})\\}$$
    - [**Compute multiplier**] by solving the 1D optimisation problem
    $$\gamma_t = \operatorname*{arg\,min}\_{\gamma}\\, L(y,F_{t-1}(x)+\gamma f_t(x))$$
    -  [**Update model**]
    $$F_t = F_{t-1}+\gamma_t f_t$$

    