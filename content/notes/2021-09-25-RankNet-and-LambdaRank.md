---
title : RankNet and LambdaRank
tags : [ranking,search]
date: 2021-09-25T05:04:51+05:30
draft: true
---

<!--<embed src="{{site.dev-images}}/2021-09-25-RankNet-and-LambdaRank.pdf" width="500" height="500"  type="application/pdf" frameborder="0" allowfullscreen>-->
<embed src="https://daxpy-website.s3.ap-southeast-1.amazonaws.com/2021-09-25-RankNet-and-LambdaRank.pdf" width="500" height="500"  type="application/pdf" frameborder="0" allowfullscreen>

---
title: RankNet and LambdaRank
---

` Machine Learning notes by Nithish Divakar. More at daxpy.xyz `

The ranking problem is about ordering a collection of documents
according to their relevance to the given query.

Their are multiple approaches to the problem, but in pairwise approach,
we simply care about predicting order of document pairs for the query.
Given 2 documents $d_i$ and $d_j$ the true relative ordering is
specified as
$$h_{ij} = \begin{cases}1& d_i>d_j\\0& d_i=d_j\\-1& d_i<d_j\\\end{cases}$$

In terms of modelling, we assume there is a base model takes in features
$x_i$ corresponds to document $d_i$ and predict a score depicting
relevance to the given query. $$s_i = f(x_i)$$

A comparator model is feed these scores which predicts
$\mathop{\mathrm{\operatorname{P}}}(d_i>d_j)$.

The comparator model can be a binary classifier by setting
$$y_{ij} \mathop{\mathrm{\triangleq}}\frac{1+h_{ij}}{2}$$ as target
variable. The a comparator is trained to predict 1 for verifying the
order and 0 for negating it.

RankNet
=======

RankNet uses a logistic regression as comparator which is feed the
difference of scores.
$$\hat{y}_{ij} = \mathop{\mathrm{\operatorname{P}}}(d_i>d_j) = \frac{1}{1+e^{-\alpha(s_i-s_j)}}$$
$\alpha$ is a parameter which controls the slope of sigmoid function.

We can define binary cross entropy loss on this model as
$$C_{ij} = -(y_{ij}\log \hat{y}_{ij}+(1-y_{ij})\log (1- \hat{y}_{ij}))$$

Now consider a mini-batch of document $\{d_1,\ldots,d_n\}$ corresponding
to a particular query. The documents have some perfect ordering to
answer the query which is specified by values of $h_{ij}$.

For gradient update, we are interested in computing the gradients
generated by each documents. $$\begin{aligned}
 \frac{\partial C}{\partial w} &=  \frac{1}{n} \sum_{i=1}^{n} \frac{\partial C_i}{\partial w}
\\
w&\gets w-\eta \frac{\partial C}{\partial w}\end{aligned}$$ Now, if we
assume the documents follow the order $d_b>d_i>d_a$, then the loss
incurred by the $d_i$ can be written as $$\begin{aligned}
C_i  &= - \sum_{a: d_i>d_a}y_{ia}\log \hat{y}_{ia} - \sum_{b:d_b>d_i}(1-y_{ib})\log (1-\hat{y}_{ib})\end{aligned}$$
Note that the ground truth labels $y_{ia}=1$ and $y_{ib}=0$. The
gradient from $d_i$ can also be simplified as $$\begin{aligned}
\frac{\partial C_i}{\partial w}&=\sum_{a}\frac{\partial C_i}{\partial s_a}\frac{\partial s_a}{\partial w}+ \sum_{b}\frac{\partial C_i}{\partial s_b}\frac{\partial s_b}{\partial w}\end{aligned}$$

The ${\partial s_\square}/{\partial w}$ part of the gradient only
depends on the score prediction network. For computing the gradient of
the comparator, we have $$\begin{aligned}
%\log \hat{y}_{ia} &= \log \frac{1}{1+e^{-\alpha(s_i-s_a)}} = \log (1+e^{-\alpha(s_i-s_a)})
%\\
%\log (1- \hat{y}_{bi}) &= \log (1+e^{\alpha(s_b-s_i)})= \log (1+e^{-\alpha(s_i-s_b)})
%\\
\frac{\partial C_i}{\partial s_a}&=-\frac{\partial \log \hat{y}_{ia}}{\partial s_a} =  \frac{-\alpha}{1+e^{\alpha(s_i-s_a)}}=-\alpha(1-\hat{y}_{ia})
\\
\frac{\partial C_i}{\partial s_b}&=-\frac{\partial \log (1- \hat{y}_{ib})}{\partial s_b} = \frac{-\alpha}{1+e^{-\alpha(s_i-s_b)}}=-\alpha\hat{y}_{ib}\end{aligned}$$
If we randomly select a document pair $(d_i,d_j)$, the gradients would
be $$\begin{aligned}
\frac{\partial C_i}{\partial s_j} &= 
\begin{cases} 
    \alpha(\hat{y}_{ij}-1) &d_i>d_j~or~h_{ij}=1
    \\
    -\alpha\hat{y}_{ij}&d_j>d_i~or~h_{ij}=-1
\end{cases}\end{aligned}$$ Now if we define the quantities
$$\lambda_{ij} \mathop{\mathrm{\triangleq}}\alpha\left[ \frac{(1-h_{ij})}{2} -(1-\hat{y}_{ij})\right]$$
we can write the individual gradient as $$\begin{aligned}
\frac{\partial C_i}{\partial w}&= \sum_a\lambda_{ia}\frac{\partial s_a}{\partial w} - \sum_b\lambda_{ib}\frac{\partial s_b}{\partial w}
%\end{aligned}$$ and the gradient of the batch as $$\begin{aligned}
\frac{\partial C}{\partial w}&= \frac{1}{n}\sum_{i=1}^{n}\lambda_{i}\frac{\partial s_i}{\partial w} 
\\
\lambda_i &= \sum_{d_i > d_j} \lambda_{ij} - \sum_{d_i < d_j} \lambda_{ij}\end{aligned}$$

So for each document in the batch, we can simply accumulate $\lambda$
and then apply it to the gradient thus not requiring $n^2$ gradient
computation.

Each $\lambda_i$ can also be thought of as the strength of gradient,
getting larger for every inversions in the the ordering and getting
smaller for correct orderings.

LambdaRank
==========

At this point explaining lambda rank is very simple. Its exactly same as
RankNet, but we modify computation of $\lambda$s as follows.
$$\lambda_{ij} \mathop{\mathrm{\triangleq}}-\alpha(1-\hat{y}_{ij})|\Delta_{NDCG}|$$
$\Delta_{NDCG}$ is the change in $NDCG$ measure if we swap $d_i$ and
$d_j$ in the ordering. This results in gradient updates optimising for
NDCG measure. Since in terms of NDCG, higher is better, we have to do
gradient ascent instead of gradient descent
$$w \gets w + \eta  \left(\frac{1}{n}\sum_{i=1}^{n}\lambda_{i}\frac{\partial s_i}{\partial w} \right)$$


    