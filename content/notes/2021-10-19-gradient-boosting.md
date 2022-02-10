---
title : Gradient Boosting
tags : [ml-theory]
date: 2021-10-19T05:04:51+05:30
draft: true
---

<!--<embed src="{{site.dev-images}}/2021-10-19-gradient-boosting.pdf" width="500" height="500"  type="application/pdf" frameborder="0" allowfullscreen>-->
<embed src="https://daxpy-website.s3.ap-southeast-1.amazonaws.com/2021-10-19-gradient-boosting.pdf" width="500" height="500"  type="application/pdf" frameborder="0" allowfullscreen>

---
title: Gradient Boosting
---

` Machine Learning notes by Nithish Divakar. More at daxpy.xyz `

Boosting is an ensembling technique which combines many weak learners in
an additive manner to produce a string learner.
$$F(x) = \sum_t \gamma_t f_t(x)$$
$$\mathop{\mathrm{arg\,min}}_{\{f_t,\gamma_t\}} \sum_i l(y_i,F(x_i))$$

The general problem is too hard to optimise, so we add one learner after
another in a greedy manner. Such a framework is
$$F_t(x) = F_{t-1}(x) + f_t(x)$$ At the $t^{th}$ step, we are interested
in learning the function $f$ which minimised the loss. The value of loss
function at this point is given by $$\begin{aligned}
    L &= l(y,p+f(x))
    \\
    &=l(y,p) + \nabla_{p} l(y,p)f(x)\marginnote{First order Taylor series approximation. $f(x) = f(a) + (x-a) f^{\prime}(a)$}\end{aligned}$$
We have trying find $f$ to minimise $L$. So we should move in negative
gradient direction in function space. $$\begin{aligned}
    F_t & \gets F_{t-1}-\gamma_t  \frac{\partial L}{\partial f}
    \\
    \frac{\partial L}{\partial f}&= \nabla_{p} l(y,p) \mathop{\mathrm{\triangleq}}-r\end{aligned}$$
What this entails is at step $t$, we find the learner which best
approximates the pseudo-residual $r$. This algorithm is called Gradient
Boosting.

-   $D=\{(x_i,y_i)\}$, loss function $L(y,F(x))$

-   the model with a constant (typically mean
    $\mathop{\mathrm{\mathbb{E}}}[y_i]$)
    $$F_0(x) = \mathop{\mathrm{arg\,min}}_{\gamma}\sum_i L(y_i,\gamma)$$

-   For $t \in 1 \ldots T$

    -   $$r_{it} = -\frac{\partial L(y_i,F_{t-1}(x_i))}{\partial F_{t-1}(x_i)}$$

    -   $$f_t \leftrightsquigarrow \{(x_i,r_{it})\}$$

    -   by solving the 1D optimisation problem
        $$\gamma_t = \mathop{\mathrm{arg\,min}}_{\gamma} L(y,F_{t-1}(x)+\gamma f_t(x))$$

    -   $$F_t = F_{t-1}+\gamma_t f_t$$


    