---
title: Gradient Through Concatenation
layout: post

---

Concatenation of vector is a common operation in computational graph of modern day Deep Learning Networks. This post describes how to compute derivative of the output w.r.to the parameters of concatenation.

$$ z = C(x,y)$$

Where $C$ is concat operation. We are interested in computing $\frac{\partial z}{\partial x}$ and $\frac{\partial z}{\partial y} $

Assuming $x\in \mathbb{R}^m$ 
  and $x\in \mathbb{R}^n$ 

  We can rewrite the concat operation as

$$z = \begin{bmatrix}I_m\\0\end{bmatrix}x+\begin{bmatrix}0\\I_n\end{bmatrix}y$$

which implies

$$\frac{\partial z}{\partial x} = \begin{bmatrix}I_m\\0\end{bmatrix}$$

$$\frac{\partial z}{\partial y} = \begin{bmatrix}0\\ I_n\end{bmatrix}$$
