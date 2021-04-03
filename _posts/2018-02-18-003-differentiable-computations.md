---
title: Differentiable Computations
layout: post

---


Auto gradient is a nice feature found in many computational frameworks.
Specify the computation in forward direction and the framework computes
backward gradients. Let's talk about the generic method to do this.

Let's say we have to compute the result of 'something'. It may be a
nasty heat equation or some logic driven steps to get from input to
output. Abstracting the steps involved gives us a sequence of equations
$$\begin{aligned}
  z_i = f_i(z_{a(i)})\end{aligned}$$

The $z$'s are intermediate variables of the computation steps or they may be parameters. The selections $z_{a(i)}$ are inputs to $f_i$.

*What does gradient of this sequence of computation mean?*

If is the final step of the computation, then computing gradients of the
sequence means i

$\frac{\partial z_n}{\partial z_i}$ are the gradients if $z_n=f_n(z_{a(n)})$ is the final step. Computing all those gradients gives us how parameters change w.r.to the output.

Handling Branches and loops
===========================

For any general computation to be included, we need to talk about
branches and loops. How are these handled in our model?

Conditional branches can be represented by indicator functions. See
[this
entry](https://en.wikipedia.org/wiki/Indicator_function#Derivatives_of_the_indicator_function)
for details on computing derivative of indicator functions.

Loops could be unrolled in to a sequence of functions. All of them would
simply share a same parameters, but inputs will be output of the
function representing previous iteration. For example

    begin loop 1:3
      x = x + c
    end

can be unrolled as

$$\begin{aligned}
  x_1 &= x + c
\\x_2 &= x_1 + c
\\x_3 &= x_2 + c\end{aligned}$$

This won't work for infinite loops because the unrolling will never end.
Infinite loops has no business in real world computation. If a loop
cannot be unrolled even after applying the "reality of the universe", we
are not talking about a computational system . It might be an event loop
or a queue. Neither needs gradients!

Forward computation as a Constrained optimisation problem
=========================================================

Without loss of generality, we can say that all this hoopla of computing
gradient is to minimise the final value. Even if this is not the case,
like for example, if maximising the final result was the intent, then
append a negating function at the end of the sequence. There are many
other techniques out there to convert different problems to a
minimization problem.

Now that we have *that* out of the way, lets look at the following
problem. 

$$\begin{aligned}
  &\min{z_n}
  \\
  s.t~z_i &= f_i(z_{a(i)})\end{aligned}$$

The formulation if a little bit weird. All it is saying is, minimise
$z_n$ such that, outputs of computations ($f_i$) are inputs to some
other computation (all $f$'s which has $z_i$ as input). Constraints are
maintaining integrity of the sequence. So we managed to represent same
thing is two ways, each saying the same thing. Great!

How do you solve a constrained optimisation problem?
====================================================

Using the method of [Lagrange
multipliers](https://en.wikipedia.org/wiki/Lagrange_multiplier). It
basically says that once we define Lagrange's function

 $$\begin{aligned}
L(z,\lambda) = z_n - \sum_i\lambda_i(z_i - f_i(z_{a(i)}))\end{aligned}$$

These $L$'s gradient w.r.to its parameters vanishes at optimum points of
original function as well. So we get

 $$\begin{aligned}
  \nabla_{\lambda_i}=0 &\implies z_i = f_i(z_{a(i)})
  \\
  \nabla_{z_n}=0        &\implies \lambda_n = 1
  \\ 
  \nabla_{z_i}=0        &\implies \lambda_i = \sum_{k\in b(i)}\lambda_k \frac{\partial f_k}{\partial z_i}\end{aligned}$$

Final expression of $\lambda_i$'s will give
$\frac{\partial z_n}{\partial z_i}$ and hence all the gradients of our
original computation. $b(\cdot)$ is like inverse of $a(\cdot)$. $a(i)$
gives which $z$'s are arguments of $f_i$ while $b(i)$ simply gives which
$f$ has $z_i$ as an argument. $b=a^{-1}$ ??. Anyway, these equations
fits nicely as a linear system

$$\begin{aligned}
A\lambda = 
\begin{bmatrix}
0\\
\vdots\\
0\\
-1
\end{bmatrix}
\quad
; A_{k,i} = 
\begin{cases}
   \frac{\partial f_k}{\partial z_i} & k\in b(i)
\\ -1 & k=i
\\ 0 & otherwise
\end{cases}\end{aligned}$$

$A$ is an upper triangular matrix with 1's on the diagonal. Otherwise,
we are looking at sequence of computation which needs result of a
future. That is too complicated for now(example of explicit systems).

This linear system of equations opens up myriad of possibilities of
computing gradients faster. The simplest of which is back substitution
since $A$ is triangular. If the computation we are dealing with is a
forward pass of a neural network, what we get out of the back
substitution is "backprop\" algorithm!!

Deriving backprop, in a weird way
=================================

Lets look at a very simple Neural network

 $$\begin{aligned}
a_1 &= \sigma(x w_1)
\\
a_2 &= \operatorname{sofmax}(a_1 w_2)
\\
l &= \operatorname{loss}(a_2,y)\end{aligned}$$ If we simplify (ahem!) it
up according to our problem, we get

 $$\begin{aligned}
z_1&=x,~ z_2=y, z_3=w_1, z_4=w_2
\\z_5 &= z_1z_3
\\z_6 &= \sigma(z_5)
\\z_7 &= z_6z_4
\\z_8 &= \operatorname{softmax}(z_7)
\\z_9 &= \operatorname{loss}(z_8,z_2)\end{aligned}$$ 

This gives us the linear system

 $$\begin{aligned}
\begin{bmatrix}
\\-1 &   &   &   & \frac{\partial f_{5}}{\partial z_{1}} &   &   &   &   
\\   &-1 &   &   &   &   &   &   & \frac{\partial f_{9}}{\partial z_{2}} 
\\   &   &-1 &   & \frac{\partial f_{5}}{\partial z_{3}} &   &   &   &   
\\   &   &   &-1 &   &   & \frac{\partial f_{7}}{\partial z_{4}} &   &   
\\   &   &   &   &-1 & \frac{\partial f_{6}}{\partial z_{5}} &   &   &   
\\   &   &   &   &   &-1 & \frac{\partial f_{7}}{\partial z_{6}} &   &   
\\   &   &   &   &   &   &-1 & \frac{\partial f_{8}}{\partial z_{7}} &   
\\   &   &   &   &   &   &   &-1 & \frac{\partial f_{9}}{\partial z_{8}} 
\\   &   &   &   &   &   &   &   & -1 & 
\end{bmatrix}
\begin{bmatrix}
\lambda_{1}\\
\lambda_{2}\\
\lambda_{3}\\
\lambda_{4}\\
\lambda_{5}\\
\lambda_{6}\\
\lambda_{7}\\
\lambda_{8}\\
\lambda_{9}\\
\end{bmatrix}
=
\begin{bmatrix}
0\\
0\\
0\\
0\\
0\\
0\\
0\\
0\\
-1
\end{bmatrix}\end{aligned}$$ 

Apply back substitution and we get

$$\begin{aligned}
\lambda_3 &= \lambda_5 \frac{\partial f_5}{\partial z_3}\quad
\lambda_4 = \lambda_7 \frac{\partial f_7}{\partial z_4}\\
\lambda_5 &= \lambda_6 \frac{\partial f_6}{\partial z_6}\quad
\lambda_6 = \lambda_7 \frac{\partial f_7}{\partial z_6}\\
\lambda_7 &= \lambda_8 \frac{\partial f_8}{\partial z_7}\quad
\lambda_8 = \lambda_9 \frac{\partial f_9}{\partial z_8}\\
\lambda_3 &= \frac{\partial l}{\partial z_8} \frac{\partial z_8}{\partial z_7} \frac{\partial z_7}{\partial z_6} \frac{\partial z_6}{\partial z_6} \frac{\partial z_5}{\partial w_1}\\
\lambda_4 &= \frac{\partial l}{\partial z_8} \frac{\partial z_8}{\partial z_7} \frac{\partial z_7}{\partial w_2}\end{aligned}$$

and there it is!! $\lambda_3$ is the gradient for parameter $w_1$ and $\lambda_4$ represent the gradient of $w_2$.

Now the structure of matrix $A$ for this problem isn't that interesting.
The example network is very simple. Almost too simple. The computational
graph is almost a line graph. But with more interesting cases, like for
example, [inception](https://www.cs.unc.edu/~wliu/papers/GoogLeNet.pdf)
architecture, the matrix will have very nice structure. A very
particular example is dense block from
[DenseNet](https://arxiv.org/abs/1608.06993). The matrix will have a
fully filled upper triangular.

**Attribution** I had my first encounter with the constrained
optimisation view of computation in Yann LeCunn's [1988
paper](http://yann.lecun.com/exdb/publis/pdf/lecun-88.pdf) "A
Theoretical Framework for back propagation". Incidentally, this is the
first paper I understood about deep learning and related field. Do give
it a read.
