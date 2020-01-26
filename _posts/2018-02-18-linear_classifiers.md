# Linear Classifiers


In the [post on bayes error](/2018/02/11/bayes-error), we discussed what
is the best classifier if the features are not enough to tell the class
apart. We also derived that in such situation, the best classifier is
$$\begin{aligned}
  h(x) = sign \left( n(x) - \frac{1}{2} \right) \end{aligned}$$

 This
formulation cannot be used in general situations as there is no easy way
to estimate $n(x) = P(y=+1|x)$ for a general distribution. But what if
$x$ has a simple distribution?

Lets assume that the data is a gaussian for each class

 $$\begin{aligned}
P(x|y) = N(\mu_y,\Sigma_y) = f_y\end{aligned}$$

 The parametric form of
$P(x|y)$ immediately give us a closed form for $n(x)$ by a simple
application of bayes rule

 $$\begin{aligned}
 n(x) = \frac{pf_{+1}}{p f_{+1}+(1-p)f_{-1}}\end{aligned}$$

 which in
turn gives us a simple classifier

 $$\begin{aligned}
 n(x) - \frac{1}{2} = \frac{pf_{+1}}{pf_{+1}+(1-p)f_{-1}} - \frac{1}{2} \end{aligned}$$



$$\begin{aligned}
 = \frac{f_{+1}}{f_{-1}} - \frac{1-p}{p} \end{aligned}$$



To further simplify, we use a strictly increasing property of $\log$
function and write

 $$\begin{aligned}
  h(x) = \operatorname{sign} \left( \log \frac{f_{+1}}{f_{-1}}- \log\frac{1-p}{p} \right)\end{aligned}$$


This gives us simpler form of the classifier

 $$\begin{aligned}
 h(x) = sign(x^TAx + b^Tx+c)\end{aligned}$$

 where
$A = \Sigma_{-1}^{-1}-\Sigma_{+1}^{-1}$.

If we further assume that class covariances are the same(
$\Sigma_{-1}=\Sigma_{+1}$), then what we get a linear classifier.
$$\begin{aligned}
  h(x) = \operatorname{sign}(b^Tx+c)\end{aligned}$$



LDA for multi-class classification
==================================

[Bayes error](/2018/02/11/bayes-error) tell us that in general case, the
classifier that has least error is

 $$\begin{aligned}
   h(x) = \operatorname{arg max}_y n_y(x) \end{aligned}$$

 where
$n_y(x) = P(y=k|x)$ is the class-wise densities. In general, the data
need not follow any distribution and hence, the class-wise densities
need not have a closed form. To mitigate this, we first assume that the
data does follow a parametric distribution.

We will assume that the class conditional densities $p(x|y)$ are
Gaussian distributed. This means that each class of the data is centred
around some point in the data space(class-wise mean), the density of the
data belonging to this class decreases as we go further away from this
mean point. We will further assume that all these class-wise
distributions have same covariance. Although this assumption is
restrictive, this helps in keeping our classifier simple. Deriving a
variant of classifier which accommodates for different covariances is
fairly straightforward from the following steps. Thus, we have
$$\begin{aligned}
p(x|y) & = f_y(x) \sim N(\mu_y, \Sigma) 
\\
\mu_y &= \frac{1}{m_y} \sum_{x\in class[y]}x
\\
\Sigma &= \frac{1}{m} \sum_{(x,y)} (x-\mu_y)(x-\mu_y)^T\end{aligned}$$



With these analytic forms, it is easy to get a closed form for $n_y$ by
a straight forward application of Bayes rule with $p_y=p(y=k)$ and we
get

 $$\begin{aligned}
  n_y(x) = \frac{p_y f_y(x)}{\sum_yp_y f_y(x)}\end{aligned}$$



From here, getting our classifier in only a matter of simplifying the
equations. So we have

 $$\begin{aligned}
  h(x) &= \operatorname{arg max} p_yf_y(x)
  \\
  &= \operatorname{arg max} w_y^Tx + b_y\end{aligned}$$



Where $w_y = \Sigma^{-1}\mu_y$ and
$b_y = \log p_y - \frac{1}{2} \mu_y^{T}\Sigma^{-1}\mu_y$. See **Appendix
1** for full derivation.

How to build one
================

To make the classifier, we first need to estimate the class-wise mean
and common covariance from the training data. Computing class-wise mean
is can be done simply by.

    mu[y] = np.mean(X[Y==y],axis=0)

The common covariance can then be calculated as

    M = np.empty_like(X)
    for y in cls:
      M[Y==y,:] = mu[y]
    S  = np.cov((X-M).T)/X.shape[0]

The classifier parameters can then be computed as

    for y in cls:
      w[y] = S_inv.dot(mu[y])
      b[y] = np.log(p[y]) - 0.5* mu[y].T.dot(S_inv).dot(mu[y]) 

Predicting class of a new data is simply

    for y in w:
      W[:,y] = w[y]
      B[y]   = b[y]
    pred = np.argmax(X.dot(W)+B,axis=1)

That is it! A complete classifier in 20 lines of code. See **Appendix
2** for full code.

How good are they
=================

Here are the accuracies I got for different datasets on using our
classifier. All Accuracies are computed for test sets of the
corresponding datasets which are not used in computing the parameters.

    * 83.90% for MNIST 
    * 76.51% for Fashion-MNIST 
    * 37.85% for cifar 10 
    * 16.67% for cifar 100

The classifier does well for MNIST and Fashion MNIST, But not so well
for both the cifars. All these accuracies are in no way close to the
state of the art, which is in high 90 for both MNISTs and cifar 10 and
high 70 for cifar 100
([link](http://rodrigob.github.io/are_we_there_yet/build/classification_datasets_results.html))
. Regardless, these are good baselines considering how cheap the
computation and effort is required to build them.

Appendix 0
==========

$$\begin{aligned}
\log \frac{f_{+1}}{f_{-1}} &= 
\log 
    \frac{|\Sigma_{-1}|}{|\Sigma_{+1}|} 
    \\&- 
    \frac{1}{2}
        \left[
        (x-\mu_{+1})^T\Sigma_{+1}^{-1}(x-\mu_{+1}) 
        - 
        (x-\mu_{-1})^T\Sigma_{-1}^{-1}(x-\mu_{-1})  
    \right] \end{aligned}$$



Appendix 1
==========

$$\begin{aligned}
  h(x) &= \operatorname{arg max} \left( p_yf_y(x) \right)
  \\
  &= \operatorname{arg max} \left( \log p_y + \log f_y(x)  \right)
  \\
  &= \operatorname{arg max} \left( \log p_y -\frac{1}{2} \log |\Sigma| + \frac{x^T\Sigma^{-1}x}{2} - \frac{\mu_y^T\Sigma^{-1}\mu_y}{2} + \frac{2(\mu_y^T\Sigma^{-1})x}{2}  \right)
  \\
  &= \operatorname{arg max} \left( \log p_y - \frac{\mu_y^T\Sigma^{-1}\mu_y}{2} + (\mu_y^T\Sigma^{-1})x  \right)\end{aligned}$$



Appendix 2
==========

    def get_linear_classifier(X,Y,cls):
      mu = {}
      p  = {}
      w  = {}
      b  = {}
      # class-wise mean and probabilities
      for c in cls:
        mu[c] = np.mean(X[Y==c],axis=0)
        p[c] = (Y==c).sum()/X.shape[0]

      # common covariance matrix and its inverse
      M = np.empty_like(X)
      for c in cls:
        M[Y==c,:] = mu[c]

      S  = np.cov((X-M).T)/X.shape[0] 
      S_inv = linalg.pinv(S)
      
      # classifier parameters
      for c in cls:
        w[c] = S_inv.dot(mu[c])
        b[c] = np.log(p[c]) - 0.5* mu[c].T.dot(S_inv).dot(mu[c]) 
      return w,b

    def test_model(w,b,X,Y):
      W = np.zeros((X.shape[1],len(w)))
      B = np.zeros((len(b),))
      for c in w:
        W[:,c] = w[c]
        B[c]   = b[c]
      pred = np.argmax(X.dot(W)+B,axis=1) 
      acc  = sum(pred==Y)/Y.shape[0]
      return acc
