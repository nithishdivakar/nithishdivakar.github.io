---
title : Implementing ArcFace Loss
tags : [paper, clustering]

---

[ArcFace]() is a loss fucnction. But it is much more. It is used to solve similarity problem in an alebit unconventional way. 

The  problem is simple, we are to learn a representation from a dataset which can be used to identify similar things from the different. This problem is officially known by a few names. retrieval, clustering to name a few. 

ArcFace solves the problem by converting it into a classification problem. There is a model $M$ which computed the embedding $z=M(x)$ and ArcFace simply uses the embedding to classify the sample into its target class $y$. 

The classification part is a bit tricky though. The loss presumes that the class centers of all the class is represented by columns of $W$ which itself is learnt during training. The model is trained such that $z$'s angle to the target class center vector $W_y$ is minimised. After ensuring that $\lVert z\rVert_2=1$ and  $\lVert W_i\rVert_2 =1$, we can write 


$$\cos \theta_i = \langle z, W_i \rangle$$


Now to ensure that angle between $z$ and $W_y$ is small we add an update

$$\theta_y \gets \theta_y+m$$

the final loss is simply

$$loss = \operatorname{softmax}(target, [\cos \theta_i])$$

All well and good. Now comes the problem in implementing. The following graph will be very useful for discussions. 

# Problem 1: Ensuring the norm
If you update the parameter while ensuring its norm is 1, then the gradient update will have a loop. ie,

Dont do,

```python
W = torch.nn.functional.normalize(W,p=2,dim=1)
```
instead, do
```python
W_normed = torch.nn.functional.normalize(W,p=2,dim=1)
```

This error looks silly, but it has implications. The equations simply says to ensure the norm is 1. But we have to actually work with a normalised copy of the parameter. That means the actual parameter is free to grow to any norm, but what is used in computation is always a normed copy. 


# Problem 2: Adding angles

To add $m$ to  $\theta_y$, we first have to do the following.

$$ \theta = \cos^{-1} (\cos \theta)$$

$$ \theta_y \gets \theta_y + m$$

Now the problem is, what happens when $\theta_y+m > \pi$ and we take cosine of that angle? Now the final loss is telling the model to increase the angle to minimise the loss and the embedding just ends subtending larger and larger angles to the class center. The soution is to never use $\cos^{-1}$ in the first place. Instead we do

$$\cos (\theta + m) =  \cos\theta \cos m - \sin\theta \sin m$$  

Now everything is inside bounds.


