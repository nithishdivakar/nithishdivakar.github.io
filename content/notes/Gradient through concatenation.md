---
title : Gradient Through Concatenation
tags : [computational-graph]
date: 2023-10-02T05:04:51+05:30
start_date: 2019-07-23T05:04:51+05:30
draft: false
---

# Gradient Through Concatenation

Concatenation of vectors is a common operation in Deep Learning Networks. How can we compute derivative of the
output in the computational graph? 

We can write the operation as

$$z = x\|y$$ 

Where $\|$ is concat operator. We are interested in computing ${\partial z}/{\partial x}$ and ${\partial z}/{\partial y}$

Assuming $x\in \mathbb{R}^m$ and $x\in \mathbb{R}^n$. We can rewrite the concat operation as

$$z = \begin{bmatrix}I_m & 0\end{bmatrix}x+\begin{bmatrix}0 & I_n\end{bmatrix}y$$

with $I_k$ as identity matrix of size $k \times k$. Then we have 

$$\begin{aligned}
\frac{\partial z}{\partial x} &= \begin{bmatrix}I_m & 0\end{bmatrix}
&
\frac{\partial z}{\partial y} &= \begin{bmatrix}0 & I_n\end{bmatrix}
\end{aligned}$$


    