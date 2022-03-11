---
title: KKT conditions and Lagrange multipliers
layout: post
tags: [optimisation]
date: 2022-03-11T06:15:30+05:30
draft: false
---

# Karush-Kuhn-Tucker conditions

A typical constrained optimisation problem is as follows. 
$$\begin{aligned}
    \min_{x\in\mathbb{R}^n}&f(x)
    \\\\
    s.t.~h_i(x) &= 0
    \\\\
    g_j(x) &\leq 0
\end{aligned}$$

## Karush-Kuhn-Tucker conditions
If the negative of the gradient (of $f$) has any component along an equality constraint $h(x)=0$, then we can take small steps along this surface to reduce $f(x)$. 

Since $\nabla h(x)$, the gradient of the equality constraint is always perpendicular to the constraint surface $h(x)=0$, at optimum, $-\nabla f(x)$ should be either parallel or anti-parallel to $\nabla h(x)$
$$-\nabla f(x) = \mu \nabla h(x)$$
A similar argument can be made for inequality constraints. These form KKT conditions. So at an optimum point $x^\ast$ we have, 
$$\begin{aligned}
    h_i(x^\ast)&=0
    &
    g_j(x^\ast) &\leq 0
    \\\\
    \lambda_j g_j(x^\ast) &= 0
    &
    \lambda_j &\geq 0
\end{aligned}$$
$$\nabla f(x^\ast) +\sum_{i} \mu_i\nabla h(x^\ast) + \sum_j \lambda_j \nabla g_j(x^\ast)= 0$$
These are the KKT conditions for constrained optimisation. 

## Lagrange multipliers
The method of Lagrange multipliers relies on KKT conditions. For a constrained optimisation problem, we introduce a Lagrange function
$$\begin{aligned}
    \mathcal{L}(x,\mu,\lambda) = f(x) + {\mu}^{T} h(x) + {\lambda}^{T} g(x)
\end{aligned}$$
*Stationary points are points where  derivative of the function is zero.*

The sationary points  of Lagrange function satisfies all of the KKT conditions. Hence we can solve for $\nabla_x\mathcal{L} =0$ to find the optimum point of $f(x)$. $\nabla_\mu \mathcal{L}=0$ and $\nabla_\lambda \mathcal{L} =0$ gives us the constraints. 
