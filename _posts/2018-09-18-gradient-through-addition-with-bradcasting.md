---
Title: Gradient Through Addition with broadcasting
---

Calculating gradient across an addition op is considered a simple algebra trick. But addition of tensors in real applications allow broadcasting. In this post, we examin how to compute gradient even in such situations.  Let us begin with fundamentals.
## Gradient of Addition

Consider a simple sequence of operations. $x$ and $y$ are inputs which ultimately leads to computation of a loss/error term $l$. 

$$
 \begin{aligned}
  z &= x+y
  \\
  l &\dashleftarrow z
 \end{aligned}
$$

We are interested in the gradient of both the inputs w.r.to $l$. LEts just go ahead and apply chin rule to get

$$
\begin{aligned}
  \frac{\partial l}{\partial x} &= \frac{\partial l}{\partial z}
  \\ 
  \frac{\partial l}{\partial y} &= \frac{\partial l}{\partial z}
\end{aligned}
$$

## Addition in Neural Networks.

Lets examine how addition in a feed forward layer is computed. This revels how additions are generally done in real usecases. Consider a simple linear feed forward layer with $x$ as input. The transformation of the layer is given by

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

$W^Tx$ is a vector which is of same size dimentions as $b$ if $x$ is also a vector. But in practise, netowrks are always trained with min-batches of samples  at a time. Which makes $x$ a 2 dimnetional tensor and suddenly the quantities $W^Tx$ and $b$ have differt dimensions. 

## Addition with broadcasting

An implicit assumption we make while adding two multi dimensional quantities is that their dimensions always match. But numerical frameworks allow addition even when the dimensions of the operands are not the same. This is called addition with boadcasting.

```python
A = np.ones([2,3])
B = np.ones([4,2,3])
C = A+B
print(A.shape, B.shape, C.shape)
print(C)
```

    (2, 3) (4, 2, 3) (4, 2, 3)
    [[[2. 2. 2.]
      [2. 2. 2.]]
    
     [[2. 2. 2.]
      [2. 2. 2.]]
    
     [[2. 2. 2.]
      [2. 2. 2.]]
    
     [[2. 2. 2.]
      [2. 2. 2.]]]


Addition is allowed if the arrays are broadcast compatible with each other. [Numpy's docs](https://docs.scipy.org/doc/numpy/user/basics.broadcasting.html) describes two arrays are broadcast compatible if there dimensions are compatible. Two dimensions are compatible if they are 

1. Equal
2. one of them is 1

When arrays do not have same number of dimensions, the arrays are copatible if the smaller array's dimensions can be stretched to both sides by simply adding dimensions of 1 and then the dimensions of both arrays become compatible.

## Gradient through Broadcasting

TODO

