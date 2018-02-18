---
layout: post
title: Linear Discriminant Analysis(LDA) Classifier
date: 2018-02-18 06:35 +0530
---


## tl;dr

LDA classifier is the bayes optimum classifier when class densities are mulit dimensional gaussian.


## What are we doing here?

In the last post, we discussed what is the best classifier if the features are not completly enought to tlee the class apart. We also derived the best classifier in this situation as 

$$ h(x) = sign \left( n(x) - \frac{1}{2} \right) $$

This equation is basically useless as there is no easy way to estimate \\( n(x) = P(y=+1\|x) \\) for a general situation. So we try to see if  assuming something about \\( x \\) can make it work.

## The assumptions
**Assumption 1**

The first assumption we make will be that the data is distributes as gaussians for each class.

$$P(x|y) = N(\mu_y,\Sigma_y) = f_y$$

**Assumption 2**

The covariance of the classes are same. 
$$\Sigma_{+1} = \Sigma_{-1}$$
This assumption will only be used in the later stages, but still, its nice to know all the assumptions up front.

## The classifier
Parametric form of \\( P(x\|y) \\) immediately give us a closed form for \\( n(x) \\) by simple application of bayes rule

$$ n(x) = \frac{pf_{+1}}{p f_{+1}+(1-p)f_{-1}}$$

Let us use this to derive a classifier.
$$ n(x) - \frac{1}{2} = \frac{pf_{+1}}{pf_{+1}+(1-p)f_{-1}} - \frac{1}{2} = \frac{f_{+1}}{f_{-1}}- \frac{1-p}{p} $$

So our classifier is \\( sign( \frac{f_{+1}}{f_{-1}}- \frac{1-p}{p}) \\). Directly using this would result in an expression with exponentials and we could not simply it further. So we apply the following trick to this equation. \\( sign(a-b) = sign(\log a - \log b)\\). This trick works because log is a striclty increasing function.

$$h^* = sign \left( \log \frac{f_{+1}}{f_{-1}}- \log\frac{1-p}{p} \right)$$

## Simplify

$$\log \frac{f_{+1}}{f_{-1}} = 
\log 
	\frac{|\Sigma_{-1}}{|\Sigma_{+1}} 
	- 
	\frac{1}{2}
		\left[
		(x-\mu_{+1})^T\Sigma_{+1}^{-1}(x-\mu_{+1}) 
		- 
		(x-\mu_{-1})^T\Sigma_{-1}^{-1}(x-\mu_{-1})  
	\right] 
$$

These equations are quadratic. So lets say
$$ h(x) = sign(x^TAx + b^Tx+c)$$

Where \\( A = \Sigma_{-1}^{-1}-\Sigma_{+1}^{-1} \\). 

\\( b \\) and \\( c \\) can be easy derived. This is where we use *assumption 2* to say that A=0. Hence our classifier becomes \\( h(x) = sign(b^Tx+c) \\). This is LDA classifier.

\\(\mu_y, \Sigma_y\\) can be estimated from data using maximum likelyhood estimation.