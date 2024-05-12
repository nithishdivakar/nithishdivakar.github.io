---
title : Gradient Through Addition with Broadcasting
tags : [computational-graph]
date: 2018-09-18T05:04:51+05:30
draft: false
---
# Gradient Through Addition with Broadcasting


Calculating gradient across an addition  is a simple
algebra trick. But this gets complicated when we look at addition of tensors which allows
broadcasting. In this post, we examine how to compute gradients in such situations.

## Gradient of Addition

Consider a simple sequence of operations. $A$ and $B$ are inputs which
ultimately leads to computation of a scalar loss/error term $l$.

$$ z  = A+B $$
$$ l   \twoheadleftarrow z $$
 
 We are interested in the gradient of both the inputs
w.r.to $l$. Apply chain rule and we get

$$ \frac{\partial l}{\partial A}  = \frac{\partial l}{\partial z} $$
$$ \frac{\partial l}{\partial B}  = \frac{\partial l}{\partial z} $$


## Addition in Neural Networks {#addition-in-neural-networks .unnumbered}

Consider a simple feed forward layer with $x$ as input. We will ignore the activation function to keep things cimple. The transformation of the layer is given by 

$$ z  = W^Tx+b $$
$$ l  \twoheadleftarrow z  $$

The gradients of the parameters w.r.to the loss terms are
$$ \frac{\partial l}{\partial b}  =\frac{\partial l}{\partial z} $$
$$ \frac{\partial l}{\partial W}  = x \frac{\partial l}{\partial z}^T $$

$W^Tx$ is a vector which is of same size dimensions as $b$ if $x$ is
also a vector. But in practise, networks are always trained with
min-batches of samples at a time. Which makes $x$ a 2 dimensional tensor
and suddenly the quantities $W^Tx$ and $b$ have different dimensions.

## Addition with broadcasting {#addition-with-broadcasting .unnumbered}

An implicit assumption we make while adding two multi dimensional
quantities is that their dimensions always match. But numerical
frameworks allow addition even when the dimensions of the operands are
not the same. This is called addition with broadcasting.

Addition is allowed if the arrays are broadcast compatible with each
other. Numpy's docs describes two arrays are broadcast compatible if
their dimensions are compatible. Two dimensions are compatible if they
are

1.  Equal
2.  One of them is 1

When arrays do not have same number of dimensions, the arrays are
compatible if the smaller array's dimensions can be stretched to both
sides by simply adding dimensions of 1 and then the dimensions of both
arrays become compatible.

## Gradient through Broadcasting {#gradient-through-broadcasting .unnumbered}

Lets unwrap what actually happens during a broadcast operation. For
simplicity, lets say we are trying to add two tensors $A$ and $B$. $A$
and $B$ agree on all dimensions except the last where A has a dimension
of size $3$ while $B$ is dimensionless.

In this case, $B$ would be broadcast over $A$ to facilitate the addition
as follows.
$$ A+B = \begin{bmatrix} A_{:,0} & A_{:,1} &  A_{:,2} \end{bmatrix}+B  $$
$$ =\begin{bmatrix} A_{:,0}+B & A_{:,1}+B &  A_{:,2}+B \end{bmatrix} $$

This allows us to visualise the computations better. For the following
computation,

$$  z = A+B $$
$$  l \dashleftarrow z $$
 
 we know that $\frac{\partial l}{\partial A}$ remains
the same. But $\frac{\partial l}{\partial B}$ is for the tensor that was broadcasted. The gradient for original B needs to be
amplified by the factor of the broadcasting. Hence $$\frac{\partial l}{\partial B} = \mathbf{n}\frac{\partial l}{\partial z}$$ A curious case to note here that, the gradient of parameter $B$ has a dimension of $A$ in it and hence is dependent on size of $A$. This might be the reason for differing behaviour of neural networks when they are trained with different batch sizes.


    
