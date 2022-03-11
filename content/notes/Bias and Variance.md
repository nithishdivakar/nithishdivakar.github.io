---
title: Bias and Variance
layout: post
tags: [machine-learning]
date: 2022-03-10T10:15:30+05:30
draft: false
---
# Bias and Variance 


A training set is only a subset of the population of data. Bias-variance trade-off talks about characteristics of predictions from the same algorithm if we use different subsets of the population as training set.

**Bias** is difference between true value and average predictions from model trained on different training set.

**Variance** is an estimate of how much the average prediction varies when we change the training set.

> Bias and variance are the properties of an algorithm rather than a trained model. 

Given  a training set $D$ from a population $T$ and an algorithm $h$ (eg. linear regression, decision tree),  we construct a model by training $h$ on $D$. Lets call such a model $h_D$. 

For a sample $(x,y) \in T$, the prediction of the model is $y_D= h_D(x)$. The average prediction of the model over different training set is $\mu_D=\mathbb{E}_D[y_D]$

$$\begin{aligned}
Bias[h]  &= \mu_D-y
\\\\
Variance[h] &=\mathbb{E}_D\left[(\mu_D-y_D)^2 \right]
\end{aligned}$$

Note that both measures are over $D$, i.e how is the algorithm $h$ behaves over different subset of $T$ as training data.



## Bias variance decomposition of least squared error

Least squares error for the model $h_D$ is 
$$l_D = \|y-y_D\|^2$$
Expected least squared error over $D$ is given by

$$\begin{aligned}
    \mathbb{E}_D\left[(y-y_D)^2\right] 
    &= \mathbb{E}_D \left(y - \mu_D + \mu_D-y_D\right)^2
    \\\\
    &= \underset{bias^2}{(y - \mu_D)^2}+ \underset{variance}{\mathbb{E}_D(\mu_D-y_D)^2}
    \\\\&\quad
    + 2\mathbb{E}_D(y - \mu_D)(\mu_D-y_D)
\end{aligned}$$

$$\mathbb{E}_D\left[(y - \mu_D)(\mu_D-y_D)\right]
    =(\mathbb{E}_D[y] - \mu_D)(\mu_D - \mu_D)=0$$


Thus, for squared loss we have
$$loss = bias^2+variance$$


## Bias and Variance decomposition under uncertain measurements

Assume that there is some true function $f(x)$ which explains a distribution. But we can only sample a subset $D=\{(x,y)\}$. There is some noise $\epsilon$ in the sampling. We can model this situation as  

$$\begin{aligned}
    y &= f(x) + \epsilon
	\\\\ 
	\mathbb{E}(\epsilon) &= 0 
	\\\\ 
	\operatorname{Var}(\epsilon)&=\sigma_\epsilon^2
\end{aligned}$$

We use algorithm $h$ to model the data and train it to minimise squared error on $D$. Let $y_D = h_D(x)$ be the prediction from such model. The expected prediction from the model is $\mu_D = \mathbb{E}_D[h_D(x)]$. The expected error  is given by 

$$\begin{aligned}
\mathbb{E}&_D[(y - y_D)^2] 
\\\\
&= \mathbb{E}_D[(f(x) + \epsilon - h_D(x))^2 ]
\\\\
&=\mathbb{E}_D[(f(x) -h_D(x))^2] + \mathbb{E}_D[\epsilon^2] -2\mathbb{E}_D[\epsilon (h_D(x) - \mu_D)]
\\\\
&= \mathbb{E}_D[(f(x) - h_D(x))^2] + \sigma\_{\epsilon}^2
\\\\
&= (f(x) -\mu_D)^2 + \mathbb{E}_D[(\mu_D -h_D(x))^2] + \sigma\_{\epsilon}^2
\\\\
&=\text{bias}^2+\text{variance} + \text{irreducible error}
\end{aligned}$$
