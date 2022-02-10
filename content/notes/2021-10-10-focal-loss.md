---
title : Focal Loss
tags : [ml-theory,deep-learning]
date: 2021-10-10T05:04:51+05:30
draft: true
---

<!--<embed src="{{site.dev-images}}/2021-10-10-focal-loss.pdf" width="500" height="500"  type="application/pdf" frameborder="0" allowfullscreen>-->
<embed src="https://daxpy-website.s3.ap-southeast-1.amazonaws.com/2021-10-10-focal-loss.pdf" width="500" height="500"  type="application/pdf" frameborder="0" allowfullscreen>

---
title: Focal Loss
---

` Machine Learning notes by Nithish Divakar. More at daxpy.xyz `

For binary classification problem, the standard cross entropy loss is
given by
$$CE(p,y_t) =\begin{cases}-\log(p)&y_t=1\\-\log(1-p)&else\end{cases}$$

We can simplify this to $CE(p_t) = -\log(p_t)$ if we define
$$p_t \mathop{\mathrm{\triangleq}}\begin{cases}p&y_t=1\\1-p&else\end{cases}$$

What if there is a huge imbalance between no of positive and negative
samples? The standard way of fixing this would be to add a balancing
term $\alpha$ which is derived from inverse class frequencies. Let
$$\alpha_t \mathop{\mathrm{\triangleq}}\begin{cases}\alpha&y_t=1\\1-\alpha&else\end{cases}$$
Balanced cross entropy loss is then, $$CE(p_t) = -\alpha_t\log(p_t)$$

However, the class imbalance has another effect during training which
cannot be mitigated by this balancing factor. The model will learn to
predict the larger class quickly than the smaller one because it simply
has more samples. Focal loss was introduced to fix this problem.

If we look at the values of $p_t$, we can see clear distinction. The
samples where $p_t \to 1$ are the ones where the model is confident
about or easy examples. $p_t<0.5$ however are hard examples.

We would want the model to care most about the hard samples. So we can
add a modulating function, $(1-p_t)^\gamma$ to the cross entropy loss.
$\gamma$ is a hyper parameter which controls the severity of the
modulating function.

So we define focal loss as $$FL(p_t)=-(1-p_t)^\gamma \log(p_t)$$ From
the plots we can see that the loss value are highly diminished for easy
examples. Also, if we compare the ratio of Cross entropy loss to Focal
loss given by $\left(\frac{1}{(1-p_t)^\gamma}\right)$, the value is huge
when we approach $p_t \to 1$.

We can also add the balancing term to focal so that the model begins
with weight balances loss values.
$$FL(p_t) = -\alpha_t(1-p_t)^\gamma \log(p_t)$$ Focal loss can be easily
extended to to multi class problem as
$$FL(y,p) = -\sum_{c\in \mathop{\mathrm{\mathcal{C}}}} y_c\alpha(1-p_c)^\gamma \log(p_c)$$


    