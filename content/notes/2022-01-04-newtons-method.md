---
title : Newton's Method
tags : [optimisation]
date: 2022-01-04T05:04:51+05:30
draft: false
---
# Newton's Method

To derive newton's method, we simply have to find the optimum point from second order Taylor series expansion of $f(x)$ 
$$\begin{aligned}
    x_{k+1} &= x_k - [H(x_k)]^{-1}\nabla f(x_k)^\intercal
\end{aligned}$$
*Derivation*: From a point $x_k$, we want to compute the best possible move $x_k+s$ to minimise $f$. Using taylor series expansion, we have
$$f(x_k+s) = f(x_k) + s\nabla f(x_k) + \frac{s^2}{2!} H(x_k) = g(s)$$

$$\begin{aligned}
0 &= \nabla_s g(s) = \nabla f(x_k) + s H(x_k)
\\\\
s &=H(x_k)^{-1} {\nabla f(x_k)}^\intercal
\end{aligned}$$


    