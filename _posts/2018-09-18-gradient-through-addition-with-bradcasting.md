# Gradient Through Addition with broadcasting



Calculating gradient across an addition op is considered a simple algebra trick. But addition of tensors in real applications allow broadcasting. In this post, we examine how to compute gradient even in such situations.  Let us begin with fundamentals.

## Gradient of Addition

Consider a simple sequence of operations. $A$ and $B$ are inputs which ultimately leads to computation of a scalar loss/error term $l$. 

$$
 \begin{aligned}
  z &= A+B
  \\
  l &\dashleftarrow z
 \end{aligned}
$$

We are interested in the gradient of both the inputs w.r.to $l$. Lets just go ahead and apply chin rule to get

$$
\begin{aligned}
  \frac{\partial l}{\partial A} &= \frac{\partial l}{\partial z}
  \\ 
  \frac{\partial l}{\partial B} &= \frac{\partial l}{\partial z}
\end{aligned}
$$

## Addition in Neural Networks.

Lets examine how addition in a feed forward layer is computed. This revels how additions are generally done in real use cases. Consider a simple linear feed forward layer with $x$ as input. The transformation of the layer is given by

$$
\begin{aligned}
  z &= W^Tx+b
  \\
  l &\dashleftarrow z
\end{aligned}$$

The gradients of the parameters w.r.to the loss terms are 

$$
\begin{aligned}
  \frac{\partial l}{\partial b} &=\frac{\partial l}{\partial z}
  \\
  \frac{\partial l}{\partial W} &= x \frac{\partial l}{\partial z}^T
\end{aligned}
$$

$W^Tx$ is a vector which is of same size dimensions as $b$ if $x$ is also a vector. But in practise, networks are always trained with min-batches of samples  at a time. Which makes $x$ a 2 dimensional tensor and suddenly the quantities $W^Tx$ and $b$ have different dimensions. 

## Addition with broadcasting

An implicit assumption we make while adding two multi dimensional quantities is that their dimensions always match. But numerical frameworks allow addition even when the dimensions of the operands are not the same. This is called addition with broadcasting.

Addition is allowed if the arrays are broadcast compatible with each other. [Numpy's docs](https://docs.scipy.org/doc/numpy/user/basics.broadcasting.html) describes two arrays are broadcast compatible if there dimensions are compatible. Two dimensions are compatible if they are 

1. Equal
2. one of them is 1

When arrays do not have same number of dimensions, the arrays are compatible if the smaller array's dimensions can be stretched to both sides by simply adding dimensions of 1 and then the dimensions of both arrays become compatible.

## Gradient through Broadcasting

Lets unwrap what actually happens during a broadcast operation. For simplicity, lets say we are trying to add two tensors $A$ and $B$. $A$ and $B$ agree on all dimensions except the last where A has a dimension of size $3$ while $B$ is dimensionless. 

In this case, $B$ would be broadcast over $A$ to facilitate the addition as follows. 

$$
\begin{aligned}
A+B &=\begin{bmatrix} A_{:,0} & A_{:,1} & A_{:,2} \end{bmatrix}+B 
\\&= 
\begin{bmatrix} A_{:,0} & A_{:,1} & A_{:,2} \end{bmatrix}+\begin{bmatrix} B & B & B \end{bmatrix}
\\&=
\begin{bmatrix} A_{:,0}+B & A_{:,1}+B & A_{:,2}+B \end{bmatrix}
\end{aligned}
$$

This allows us to visualize the computations better. For the following computation,  

$$
 \begin{aligned}
  z &= A+B
  \\
  l &\dashleftarrow z
 \end{aligned}
$$

we know that $\frac{\partial l}{\partial A}$ remains the same. But $\frac{\partial l}{\partial B}$ is for the tensor that has been broadcast and hence needs to be adjusted. The gradient needs to be amplified by the factor of the broadcasting. Hence


$$\frac{\partial l}{\partial B} = \mathbf{n}\frac{\partial l}{\partial z}$$ 


A curious case to note here that, the gradient of parameter $B$ has a dimension of $A$ in it and hence is dependent on size of $A$. This might be the reason for differing behaviour of neural networks when they are trained with different batch sizes.  
