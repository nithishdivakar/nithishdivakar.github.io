---
title : Common Optimisers
tags : [machine-learning,deep-learning]
date: 2021-10-24T05:04:51+05:30
draft: false
---

# Common Optimisers
$E$ is the loss function and $w$ is the model parameters;


## Stochastic Gradient Descent
$$\begin{aligned}
    w_{t+1}&= w_t -   \alpha \nabla E(w_t)\end{aligned}$$

## SGD with Momentum

*Use gradient to update velocity/direction of a particle instead of only updating its position*


$$\begin{aligned}
m_{t+1} &= \eta m_t + \alpha \nabla E(w_t)
\\\\
w_{t+1}&= w_t -  m_{t+1}
\end{aligned}$$ 
This results in equivalent single update as 
$$w_{t+1}= w_t - \alpha \nabla E(w_t)  - \eta m_{t}$$

$\eta$ is the exponential decay factor in $[0,1]$ which determines
contribution of previous gradients to the weight change.

## Nesterov Accelerated Gradient

The observation behind nesterov momentum is that we will update the
parameters by the momentum term anyway, why not calculate gradient at
the updated step instead? 

$$\begin{aligned}
    m_{t+1} &= \eta m_t + \alpha \boldsymbol{\nabla E(w_t-\eta m_t)}
    \\\\
    w_{t+1}&= w_t -  m_{t+1}
\end{aligned}$$ 

Since we calculate the gradient at the new location, if there is a difference in direction, the
update will be able to correct for the difference. It increases responsiveness of the optimiser.

## RMSProp

Root Mean Square Propagation. Divide learning rate of each weight by
running average of magnitudes of recent gradients for that weight.
$$\begin{aligned}
v_{t+1} &= \gamma v_{t} + (1-\gamma)(\nabla E(w_t))^2
\\\\
w_{t+1}&=w_{t} - \frac{\alpha}{\sqrt{v_{t+1}}} \nabla E(w_t)
\end{aligned}$$

*Note*: $\nabla E(w_t)^2=\|\nabla E(w_t)\|_F^2$

## Adam

Adaptive Moment Estimation is an update to RMSProp. It uses a running
average for the gradient as well 
$$\begin{aligned}
v_{t+1} &= \beta_1 v_{t} + (1-\beta_1)(\nabla E(w_t))^2
\\\\
m_{t+1} &= \beta_2 m_{t} + (1-\beta_2)\nabla E(w_t)
\\\\
m &= \frac{m_{t+1}}{1-\beta_2} \quad v = \frac{v_{t+1}}{1-\beta_1}
\\\\
w_{t+1}&=w_{t} - \alpha \frac{m}{\sqrt{v}+\epsilon}
\end{aligned}$$