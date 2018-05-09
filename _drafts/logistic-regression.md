---
layout: post
title: Implementing Logistic Regression
date: 2018-03-17 16:30 +0530
comments: true
---

In the post about LDA, we have seen how to implement a classifier using generative assumption. Now lets do the other thing. Let's built a classifier with discriminative assumption. 

## Logistic Regression
Imagine we have a dataset \\(\{x,y\}\\). For deriving LDA classifier, we had modeled the class conditionals \\(P(x\|y)\\) and derived the posterior \\(P(y\|x)\\). Here, we will directly model the posterior with a linear function. Since the posterior directly models what class a data point belongs to, we dont have to do much after computing it to get a classifier.

Modelling \\(P(y=k\|x)  \\) with only a linear function \\( w_k^Tx\\) has some problems. This function does not easily satisfy a probabilty distribution. There is no easy way to restrict \\(w_k^Tx\\) to \\([0,1]\\) nor assure that \\(\sum_k P(y=k\|x) = 1\\). We want the modelling to projection the data such that it forms a clear probability distribution over the classes. Since this is near impossible with only a linear function, we stack a non parametric transformation on top of the linear projections. 


**Softmax function** is that transformation. Softmax is a vector valued function  defined over a sequence \\({z_k}\\) as 

<div>$$
S(z) = \left[\frac{\operatorname{exp}[z_k]}{\sum_j\operatorname{exp}[z_j]}\right]
$$</div>

Stacking softmax function over the linear transformation w_k^Tx gives us a final distribution which is almost like a probabilty density. Hence our classifier is this

<div>$$
P(y|x) = S(W^Tx)
$$</div>


## Softmax function is differentiable

Lets figure out what its derivative is. First we will write softmax in a concise form.

<div>$$
s_k = \frac{e_k}{\Sigma}
$$</div>
where \\(e_k = \operatorname{exp}[z_k]\\) and \\(\Sigma = \sum_j\operatorname{exp}[z_j]\\). With \\(\frac{\partial e_k}{\partial z_k} = e_k\\) and \\(\frac{\partial \Sigma}{\partial z_p} = e_p \\) , we can easily derive the derivative fo softmax function as follows.

<div>$$
\begin{aligned}
\text{ when $p \neq k$}
\\
\frac{\partial s_k}{\partial x_p} &= e_k\left[ \frac{-1}{\Sigma^2} e_p\right]

&&= -s_ks_p
\\
\text{ when $p = k$}
\\
\frac{\partial s_k}{\partial x_p} &= 
\frac{  e_k \Sigma-  e_p e_k}{\Sigma^2}
&&=s_k-s_ps_k
\\
\text{in general}
\\
\frac{\partial s_k}{\partial x_p} &= s_k(\delta_{kp} - s_p)
\end{aligned}
$$</div>

\\(\delta_{kp}\\) is delta function which is \\(1\\) only when \\(k=p\\) and \\(0\\) otherwise.



## Estimating the parameters of the model

Now that we have a complete model of the classifier, \\(P(k\|x) = S(w_k^Tx) \\),  all that is remaining is to estimate \\(w_k\\)'s to have the classifier. Fot this we use maximum likelyhood [ref] of the model explaining the training data.  

<div>$$
\begin{aligned}
L(w) &= \prod_x \prod_k P(k|x;w)^{y_k} = \prod_x \prod_k S(w_k^Tx)^{y_k} 
\\
-\log L(w) & = -\sum_x \sum_k y_k \log s_k
\end{aligned}
$$</div>

If we think of y as a true probabilty of the data over all the classes and z as our model's prediction of this distribution, then the negative likelyhood is essentially minimising cross entropy[ref] between the two distributions. 

<div>
$$E(w) =  -\sum_x \sum_k y_k \log s_k$$
</div>

Maximising likelyhood of the model over the data essentially is minimising the cross entropy loss. **Logistic regression minimises cross entropy loss**. 
<div>$$
\begin{aligned}
\nabla_wE(w) %&= -\sum_x \sum_k y_k \nabla_w \log S(w_k^Tx)
\\
&=\sum_{(x,y)} (s-y)\cdot x
\end{aligned}
$$</div>


See Appendix 2 on derivation of \\(\nabla_w E(w)\\)






## Appendix 2: Derivative of cross entropy loss with softmax activations


<div>$$
\begin{aligned}
E(w) &=  -\sum_x \sum_k y_k \log s_k
\\
\nabla_{w_p} E(w) &= -\sum_x \sum_k y_k \frac{1}{s_k} \frac{\partial s_k}{\partial w_p}
\\
&=-\sum_x \sum_k y_k \frac{1}{s_k} \frac{\partial s_k}{\partial z_p} \frac{\partial z_p}{\partial w_p} 
\\
&=-\sum_x \sum_k y_k \frac{1}{s_k} s_k(\delta_{kp} - s_p) x
\\
\nabla_{w_p} E(w) &= -\sum_x \sum_k y_k (\delta_{kp} - s_p) x
\\
\sum_k y_k (\delta_{kp} - s_p) & = \sum_k y_k \delta_{kp} - s_p\sum_k y_k
\\
&= \text{sincle only $\delta_{pp} = 1$}
\\
&= y_p - s_p 
\\
\nabla_{w_p} E(w) &= \sum_x (s_p - y_p) x
\\
\nabla_{w} E(w) &= \sum_x (s - y) \cdot x
\end{aligned}
$$</div>