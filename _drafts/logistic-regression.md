---
layout: post
title: Logistic Regression
date: 2018-03-17 16:30 +0530
comments: true
---







## Softmax function 

Softmax is a vector to vector function which. continuous equivalent to max function.
<div>$$
s(x_k) = \frac{\operatorname{exp}[x_k]}{\sum_j\operatorname{exp}[x_j]}
$$</div>
### Derivative
Lets write softmax in a simplified form.

<div>$$
s_k = \frac{e_k}{\Sigma}
$$</div>
where \\(e_k = \operatorname{exp}[x_p]\\) and \\(\Sigma = \sum_j\operatorname{exp}[x_j]\\). With \\(\frac{\partial e_k}{\partial x_k} = e_k\\) and \\(\frac{\partial \Sigma}{\partial x_p} = e_p \\) , we can easily derive the derivative fo softmax function as

<div>$$
\begin{aligned}
\text{ when $x_p \neq s_k$}
\\
\frac{\partial s_k}{\partial x_p} &= e_k\left[ \frac{-1}{\Sigma^2} e_p\right]

&&= -s_ks_p
\\
\text{ when $x_p = s_k$}
\\
\frac{\partial s_k}{\partial x_p} &= 
\frac{  e_k \Sigma-  e_p e_k}{\Sigma^2}
&&=s_k-s_ps_k
\\
\text{in general}
\\
\frac{\partial s_k}{\partial x_p} &= s_k(\delta_{kp} - s_p)
\end{aligned}
$$</div>

\\(\delta_{kp}\\) is delta function which is \\(1\\) only when \\(k=p\\) and \\(0\\) otherwise.

