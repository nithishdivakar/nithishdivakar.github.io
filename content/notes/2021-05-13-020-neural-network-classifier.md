---
title : Neural Network Classfier
tags : [ml-applied]
date: 2021-05-13T05:04:51+05:30
draft: true
---
# Neural Network Classifier

Biggest huddle is keeping track of axes. Its hard to juggle 3-4
different axes in your head and keep track of which one is to be dotted
with which. Then keeping track of them through differentiation is worse.
So

## Everything is a scalar 
$$\begin{aligned}
Z^{(L)}_{ti} &= W^{(L)}_{ij}P^{(L-1)}_{tj}+B^{(L)}_{i}
\\
P^{(L)}_{ti} &= act(Z^{(L)}_{ti})\end{aligned}$$

It's very easy to implement the forward computation using 'einsum' in
numpy now.

```python
Z2 = np.einsum('ij,tj->ti',W2,P1)+B2
P2 = np.where(Z2>0,Z2,0)  
```  

practically reading of the equation to write the code.

## Differentiate everything w.r.to everything

For the first equation in forward computation, we want to find
$\frac{\partial Z}{\partial W}$. For this, let differentiate in all the
axes

$$\frac{\partial Z_{ab}}{\partial W_{cd}} = P_{ad} ~~when~ b=c$$

Also,

$$\frac{\partial l}{\partial W_{cd}} = \frac{\partial l}{\partial Z_{ab}}\frac{\partial Z_{ab}}{\partial W_{cd}} = [\nabla Z]_{ab}P_{ad}= [\nabla Z]_{ac}P_{ad}$$

```python
grad_W2 = np.einsum('ac,ad->cd',grad_Z2,P1)
```

again, implementation is practically reading of the equation.


    