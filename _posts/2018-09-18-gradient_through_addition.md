# Gradient Through Addition

Gradient of Addition
====================

Adding two variables to get another is arguably one of the fundamental
operations in computation.

 $$\begin{aligned}
  z &= x+y
  \\
  l &\dashleftarrow z\end{aligned}$$

 That's all there is to it. $z$
contains the sum of values of $x$ and $y$ and $l$ is some error value
which the computation leads to. The gradient of this graph is then

$$\begin{aligned}
  \frac{\partial l}{\partial x} &= \frac{\partial l}{\partial z}
  \\ 
  \frac{\partial l}{\partial y} &= \frac{\partial l}{\partial z}\end{aligned}$$



Addition in real graphs
=======================

Adding bias to the transformed input is a basic op in an affine layer of
a neural network.

 $$\begin{aligned}
  z &= W^Tx+b
  \\
  l &\dashleftarrow z\end{aligned}$$

 In this case, the gradients we are
interested in are $\frac{\partial l}{\partial b}$ and
$\frac{\partial l}{\partial W}$. Here again,

 $$\begin{aligned}
  \frac{\partial l}{\partial b} &=\frac{\partial l}{\partial z}
  \\
  \frac{\partial l}{\partial W} &= x \frac{\partial l}{\partial z}^T\end{aligned}$$


Everything is as expected.

But in practice, there is more the equation than meets the eye. Networks
are seldom trained one sample at a time. It always a mini-batch. Hence
the $x$ is no longer a vector. It is a collection of samples. We end up
adding two quantities of different dimensions.

Addition with broadcasting
==========================

An implicit assumption we make while adding two multi dimensional
quantities is that their dimensions match. This is hardly the case. This
begs the question, when is addition allowed when dimensions mismatch?

    >>> A = np.ones([2,3])
    >>> B = np.ones([4,2,3])
    >>> C = A+B
    >>> C
    array([[[2., 2., 2.],
            [2., 2., 2.]],

           [[2., 2., 2.],
            [2., 2., 2.]],

           [[2., 2., 2.],
            [2., 2., 2.]],

           [[2., 2., 2.],
            [2., 2., 2.]]])

Addition is allowed if the arrays are broadcast compatible with each
other.
