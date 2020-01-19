# Softmax Classifier

Softmax Classifier
==================

Imagine we have a dataset $\{x,y\}_{i=0}^m$ where $x$ is a data point
and $y$ indicates the class $x$ belongs to. For deriving LDA classifier,
we had modelled the class conditional density $P(x|y)$ as a gaussian and
derived the posterior probabilities $P(y|x)$. Here, we will directly
model the posterior with a linear function. Since the posterior directly
models what class a data point belongs to, we don't have much to do
after to get a classifier.

But modelling $P(y|x)$ with only a linear projection $w^Tx$ has some
problems. There is no easy way to restrict $w^Tx$ to always fall in
$[0,1]$ nor assure that $\sum_k P(y=k|x) = 1$.

We want a projection of the data such that it forms a clear probability
distribution over the classes. Since this is near impossible with only a
linear function, we stack a non parametric transformation following the
linear transformation.

**Softmax** is a vector valued function defined over a sequence $(z_k)$
as

$$\begin{aligned}
\operatorname{softmax}(z)_k = \frac{\operatorname{exp}[z_k]}{\sum_j\operatorname{exp}[z_j]}\end{aligned}$$



Softmax preserves the relative magnitude of its input i.e the larger
input coordinate get the larger output value. Softmax also squashes the
values to lie in range $[0,1]$ and makes their sum equal to $1$.

$$\begin{aligned}
\sum_k \frac{\operatorname{exp}[z_k]}{\sum_j\operatorname{exp}[z_j]} = \frac{\sum_k \operatorname{exp}[z_k]}{\sum_j\operatorname{exp}[z_j]}  = 1\end{aligned}$$



So our classifier is

$$\begin{aligned}
P(y|x) = \operatorname{softmax}(w^Tx)\end{aligned}$$



Derivative of the Softmax function
==================================

We will need the derivative of softmax function later on. So let's
figure out what it is. We can begin by writing softmax in a concise
form.

$$\begin{aligned}
s_k = \frac{e_k}{\Sigma}\end{aligned}$$

 where
$e_k = \operatorname{exp}[z_k]$ and
$\Sigma = \sum_j\operatorname{exp}[z_j]$. With
$\frac{\partial e_k}{\partial z_k} = e_k$ and
$\frac{\partial \Sigma}{\partial z_p} = e_p$, we can easily derive the
derivative for softmax function as follows.

$$\begin{aligned}
\text{ when $p \neq k$}
\\
\frac{\partial s_k}{\partial x_p} &= e_k\left[ \frac{-1}{\Sigma^2} e_p\right] \\&= -s_ks_p
\\
\text{ when $p = k$}
\\
\frac{\partial s_k}{\partial x_p} &= 
\frac{  e_k \Sigma-  e_p e_k}{\Sigma^2} \\&= s_k-s_ps_k
\\
\text{in general}
\\
\frac{\partial s_k}{\partial x_p} &= s_k(\delta_{kp} - s_p)\end{aligned}$$


$\delta_{kp}$ is dirac delta function which is $1$ only when $k=p$ and
$0$ otherwise.

Estimating Model Parameter using Likelihood
===========================================

Now that we have a complete model of the classifier,
$P(y|x) = \operatorname{softmax}(w^Tx)$, all that is remaining is to
estimate the model's parameters $w$ from the dataset. We can begin by
using
[likelihood](https://en.wikipedia.org/wiki/Maximum_likelihood_estimation)
of the model explaining the training data.

$$\begin{aligned}
L(w) &= \prod_x \prod_k P(k|x;w)^{y_k} 
\\
&= \prod_x \prod_k \operatorname{softmax}(w_k^Tx)^{y_k} \end{aligned}$$



Likelihood gives a measure of how much the model explains the data
$\{x,y\}$ for a given parameter $w$. To get the optimum value for the
parameter, all we have to do find the value of $w$ which maximises the
likelihood.

The likelihood function is a bit difficult to work with on its own. But
we take negative of the log of likelihood function[^1] so that all
products gets converted to sum and all exponentials gets converted to
products. $$\begin{aligned}
E(w) &= -\log L(w) 
\\
&= -\sum_x \sum_k y_k \log s_k\end{aligned}$$



All we have to do to get the best parameter is to minimise the negative
log likelihood (thereby maximising likelihood)

$$\begin{aligned}
w_{opt} = \operatorname{argmin}_w  E(w)\end{aligned}$$



*Note: If we think of $y$ as a probability distribution of data
belonging to each of the classes and $s$ as our model's prediction of
the same, then $E(w)$ is cross entropy between the two distributions.*

For computing $w_{opt}$, we simply have to find derivative of $E(w)$
w.r.to $w$ and equate it to 0. But finding derivative over then entire
$w$ is difficult and non-intuitive. So let's break it down and find
derivatives over each the columns $w_p$ separately.

$$\begin{aligned}
\nabla&_{w_p} E(w) 
\\
&= -\sum_x \sum_k y_k \frac{1}{s_k} \frac{\partial s_k}{\partial w_p}
\\
&=-\sum_x \sum_k y_k \frac{1}{s_k} \frac{\partial s_k}{\partial z_p} \frac{\partial z_p}{\partial w_p} 
\\
&=-\sum_x \sum_k y_k \frac{1}{s_k} s_k(\delta_{kp} - s_p) x
\\
&= -\sum_x \sum_k y_k (\delta_{kp} - s_p) x\end{aligned}$$


$\sum_k y_k (\delta_{kp} - s_p)$ can be expanded as
$\sum_k y_k \delta_{kp} - s_p\sum_k y_k$. Only $\delta_{pp}=1$ and
$\sum y_k =1$. Thus the original term evaluates to $y_p - s_p$.
$$\begin{aligned}
\nabla_{w_p} E(w) &= \sum_x (s_p - y_p) x
\\
\nabla_{w} E(w) &= \sum_x (s - y) x\end{aligned}$$



Now we have a problem here. Setting $\nabla_w E(w)=0$ does not give any
information about $w$. However, what the gradient do tells is that in
space of $w$, which is the direction to move (change $w$) so that the
change in $E$ is the largest. So if we move in the exact opposite
direction (negative of gradient), we will get maximum reduction in $E$.
Since $E$ is measuring the difference between model's prediction and the
true labels, decreasing $E$ would mean our model is getting better.
Enter **Gradient Descent**.

Gradient Descent Algorithm
==========================

Gradient descent is exactly that; gradient-descent. If you want to
minimise a function, keep moving in negative direction of its gradient
(thereby descending).

[Gradient descent](https://en.wikipedia.org/wiki/Gradient_descent) is an
optimisation algorithm for cases where there is no analytic or easy
solution for the parameters, but gradients of the models can be computed
at each point. The algorithm simply says, if $L$ is some loss function
which measures how good the model is with parameter $\theta$, then we
can update $\theta$ as to make the model better. $$\begin{aligned}
\theta_{new} = \theta - \alpha \nabla_\theta L\end{aligned}$$



Now repeat the same with new $\theta_{new}$ and the model with keep
getting better. There are some caveats however. The behaviour of
gradient descent entirely depends on choice of step size $\alpha$ and
even then, convergence to global optimum is not guaranteed.

In practise however, gradient descent performs well. We do have some
tricks to pick the (seemingly) best step size and some other ways to
ensure model improves. In our case, the update step is simply,

$$\begin{aligned}
w_{new} = w - \alpha \nabla_{w}E(w)\end{aligned}$$



To compute the true gradient direction of the model, we need to evaluate
the model over every possible data. This is impossible because (1)
intractable amount of computation and (2) we don't have labels for all
possible data (if we did, what is the point of building a classifier).

So, we are computing an approximate model gradient over the data that we
have. But even this is a lot of work for getting an approximate gradient
and that is not end of the story. We have to keep iterating. Since we
are approximating, why not approximate further. Pick a sample at random,
compute gradient over it and update the model. This is Stochastic
Gradient Descent.

[Stochastic Gradient
Descent](https://en.wikipedia.org/wiki/Stochastic_gradient_descent) is
not that stable. Gradient of each samples do not agree with each other
and hence, the frequent updates simply results in random motion in the
parameter space. To make more stable, we compute gradient over a small
set of samples or a batch. This is batched stochastic gradient descent.
Batched SGD updates the model more frequently than pure gradient descent
and is more stable than vanilla SGD. In fact, batched SGD is so commonly
used that now it has become the vanilla. SGD now refers to batched SGD.

This is how you implement SGD.

$idx \gets 1$ $W = initialise\_weights()$ $x_b,y_b$ = next(get\_batch)
$s_b  = M(x_b;W)$\
$g_b  = \nabla_W s_b$ $W  \gets W - \alpha g_b$ break

Implementing Softmax classifier and its gradients
=================================================

Implementing the forward prediction of the classifier is pretty straight
forward. First we have to do a matrix vector multiplication to implement
$z=w^Tx$ and then point-wise exponentiate all the terms in $z$.

However, we have to sum all of these exponentiated terms to get the
denominator in the softmax step. Since exponentiation creates huge
numbers if components of $z$ are greater than $1$, this creates some
numerical errors.

![image](figures/exponential-curve){width="0.7\\linewidth"}

To get rid of the numerical errors we use the following trick.
$$\begin{aligned}
\operatorname{softmax}(z)_k &= \frac{e^{z_k}}{\sum_i e^{z_i}}
\\
&= \frac{e^{-M}e^{z_k}}{e^{-M}\sum_i e^{z_i}}
\\
&= \frac{e^{z_k-M}}{\sum_i e^{z_i-M}}\end{aligned}$$



If we choose $M$ large enough such that all the terms in the powers are
negative or $0$, all the exponentiated terms will be small. So we set
$M = \max z_i$.

Following code sample shows how the model's prediction is implemented.
The code has been vectorised so that it can predict for a batch of $x$
at once.

    def get_predictions(x,W):
      z = np.matmul(x,W.T)
      M = np.max(
            z,
            axis=-1,
            keepdims=True
          )
      e = np.exp(z-M)
      # normalisation trick so
      # that largest of z is 0

      sigma = e.sum(
                axis=-1,
                keepdims=True
              )
      s = e/sigma
      return s

Unlike forward pass, implementing gradient is very simple. It's only an
outer product between two vectors $s-y$ and $x$. But, when we implement
it for a batch of samples and it's predictions, the outer product can be
implemented as a matrix multiplication. See the code sample below.

    def get_batch_gradient(
        x_b, # input
        y_b, # target
        s_b  # prediction
      ):
      g_b = np.matmul(
              (s_b-y_b).T,
              x_b
            )
      return g_b/batch_size

Model Performance
=================

[Cifar 10](https://www.cs.toronto.edu/~kriz/cifar.html) is a image
dataset having 10 image classes. In this section, we test our simple
softmax classifier's performance on it.

To tune the model to get optimum performance, we first need to find the
best hyper-parameters (batch size and learning rate). For this, we first
split the training set into two. A smaller set for validation and the
rest to be used solely for training. The model is trained only on this
new training set and validation set will be like our proxy test set
while we find the best hyper parameter.

So we train the model for relative shorter duration (10000 gradient
updates) and see its performance on validation set for different choices
of hyper parameters. The following table list model performances for
different hyper parameter combinations.

  -------------- ------ ------ ------ ------ -- -- -- --
                                                      
                 4      8      16     32              
  $10^{-1}$      0.20   0.16   0.28   0.31            
  $10^{-2   }$   0.22   0.29   0.35   0.38            
  $10^{-3  }$    0.33   0.34   0.36   0.36            
  $10^{-4 }$     0.29   0.30   0.30   0.30            
  $10^{-5}$      0.18   0.19   0.18   0.19            
                                                      
                 64     128    256    512             
  $10^{-1}$      0.26   0.29   0.22   0.28            
  $10^{-2   }$   0.38   0.39   0.40   0.40            
  $10^{-3  }$    0.37   0.37   0.37   0.37            
  $10^{-4 }$     0.31   0.30   0.30   0.30            
  $10^{-5}$      0.19   0.19   0.19   0.17            
  -------------- ------ ------ ------ ------ -- -- -- --

Batch size $256$ and learning rate $0.01$ gave the best performance. So
we will train the model for longer duration(1000000 gradient updates)
with these parameters. The following plot shows validation loss during
training progress.

![image](figures/validation-loss){width="1.0\\linewidth"}

We get a final test accuracy of 38.05%.

Conclusion
==========

LDA model gave us 37.85% accuracy on Cifar 10 dataset. The softmax
classifier is giving us 38% accuracy. It appears to be a close tie
between both the models, but one important distinction is that LDA
distinctly modelled the data as gaussian while we made no such
assumption while designing the softmax classifier.

Our simple linear classifier appear useless when compared to bigger and
complex models(CNNs) that achieves near perfect accuracy on cifar 10.
But there is some values in learning these simple ones first. They do
teach some very valuable lessons about data modelling. They are also
very good to test implementing optimiser algorithms like SGD we have
implemented for this post. Do test them out on some other problems.

Code
====

The code is
[here](https://github.com/nithishdivakar/blog-post-codes/tree/master/softmax-classifiers).

[^1]: $\log$ is a strictly increasing function
