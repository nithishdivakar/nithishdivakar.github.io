---
layout: post
title: Linear Classifier
date: 2018-02-18 06:35 +0530
comments: true
---


In the [last post]({% post_url 2018-02-11-bayes-error %}), we discussed what is the best classifier if the features are not completly enough to tell the class apart. We also derived the best classifier in such situation to be

$$ h(x) = sign \left( n(x) - \frac{1}{2} \right) $$

This cannot be used in general situations as there is no easy way to estimate \\( n(x) = P(y=+1\|x) \\) for any data distribution. But what if \\( x \\) does follow a simple distribution?

Lets assume that the data is a gaussian for each class [**assumption 1**]

$$P(x|y) = N(\mu_y,\Sigma_y) = f_y$$

The parametric form of \\( P(x\|y) \\) immediately give us a closed form for \\( n(x) \\) by a simple application of bayes rule

$$ n(x) = \frac{pf_{+1}}{p f_{+1}+(1-p)f_{-1}}$$

which in turn gives us a simple classifier

$$ n(x) - \frac{1}{2} = \frac{pf_{+1}}{pf_{+1}+(1-p)f_{-1}} - \frac{1}{2} $$

$$ = \frac{f_{+1}}{f_{-1}} - \frac{1-p}{p} $$

To simplify it further, we use a strictly increasing property of \\(log\\) function and write

$$h = sign \left( \log \frac{f_{+1}}{f_{-1}}- \log\frac{1-p}{p} \right)$$

This gives us simpler form of the classifier

$$ h(x) = sign(x^TAx + b^Tx+c)$$

where \\( A = \Sigma_{-1}^{-1}-\Sigma_{+1}^{-1} \\). If we further assume that class covariances are the same( \\(\Sigma_{-1}=\Sigma_{+1}\\)), then we get a linear classifier.

$$ h(x) = sign(b^Tx+c)$$


---
## Appendix

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



