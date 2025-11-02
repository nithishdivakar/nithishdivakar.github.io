---
date: 2024-01-01 00:00:00 +0000
slug: '02a'
layout: post
status: doing
title: Kitchen sink optimiser model
tags: [optimisers]
---


## Kitchen sink optimiser model
A typical loss function of a model is comprised of loss from data (E) and loss from weight or a regulariser (R)


$$ loss =  E(w_t) + \gamma R(w_t) $$

gradient 

$$ g_t  = \nabla E(w_t)  + \gamma \nabla R(w_t)  $$

velocity

$$ v_{t+1} = f\left(\beta_1 v_t + (1 - \beta_1)(g_t)^2\right) $$

momentum

$$ m_{t+1} = h\left(\beta_2 m_t +(1  - \beta_2) g_t\right) $$


weight update

$$ w_{t+1} =  w_t   - \alpha  \left( \frac{m_{t+1} }{\sqrt{v_{t+1}} + \epsilon} \right)  - \lambda w_t $$

The final term is weight decay. We can derive all the optimisers based on the value of constants and the nature of $f$ and $h$


