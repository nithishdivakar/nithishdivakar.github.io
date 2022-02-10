---
title : Gradient Through Concatenation
tags : [computational-graph]
date: 2019-07-23T05:04:51+05:30
draft: true
---

<!--<embed src="{{site.dev-images}}/2019-07-23-011-gradient-through-concatenation.pdf" width="500" height="500"  type="application/pdf" frameborder="0" allowfullscreen>-->
<embed src="https://daxpy-website.s3.ap-southeast-1.amazonaws.com/2019-07-23-011-gradient-through-concatenation.pdf" width="500" height="500"  type="application/pdf" frameborder="0" allowfullscreen>

---
title: Gradient Through Concatenation
---

` Machine Learning notes by Nithish Divakar. More at daxpy.xyz `

Concatenation of vectors is a common operation in computational graph of
modern day Deep Learning Networks. How can we compute derivative of the
output? $$z = x\|y$$ Where $\|$ is concat operation. We are interested
in computing ${\partial z}/{\partial x}$ and ${\partial z}/{\partial y}$
Assuming $x\in \mathbb{R}^m$ and $x\in \mathbb{R}^n$. We can rewrite the
concat operation as
$$z = \begin{bmatrix}I_m\\0\end{bmatrix}x+\begin{bmatrix}0\\I_n\end{bmatrix}y$$
which gives $$\begin{aligned}
\frac{\partial z}{\partial x} &= \begin{bmatrix}I_m\\0\end{bmatrix}
&
\frac{\partial z}{\partial y} &= \begin{bmatrix}0\\ I_n\end{bmatrix}\end{aligned}$$


    