---
title: BFGS
layout: post
tags: [optimisation]
date: 2022-03-11T00:15:30+05:30
draft: false
---
# BFGS


## Newton's Method
$$\begin{aligned}
    x_{k+1} &= x_k - [H(x_k)]^{-1}\nabla f(x_k)^\intercal
\end{aligned}$$

## Quasi Newton's Method
$$\begin{aligned}
    x_{k+1} &= x_k - \alpha_kS_k {\nabla f(x_k)}^{T} 
\end{aligned}$$

If $S_k$ is inverse of Hessian, then method is Newton's iteration; if $S_k=I$, then it is steepest descent

## BFGS
BFGS is a quasi newtons method where we approximate inverse of Hessian by $B_k$. The search direction $p_k$ is determined by solving
$$B_kp_k = -\nabla f(x_k)$$
A line search is performed in this search direction to find next point $x_{k+1}$ by minimising $f(x_k+\gamma p_k)$. The approximation to hessian is then updated as 
$$\begin{aligned}
    B_{k+1} &= B_k + \alpha_k u_ku_k^\intercal  + \beta_k v_kv_k^\intercal 
    \\\\
u_k &= \nabla f(x_{k+1})-\nabla f(x_k)
\\\\
\alpha_k &= \frac{1}{\alpha u_k^\intercal p_k}
\\\\
v_k &= B_kp_k
\\\\
\beta_k &= \frac{-1}{p_k^\intercal B_kp_k}
\end{aligned}$$
