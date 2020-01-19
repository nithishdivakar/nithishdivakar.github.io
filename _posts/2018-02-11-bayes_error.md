# Bayes Error

The God Function
================

In an ideal world, everything has reason. Every question has a
unambiguous answer. The data in sufficient to explain its behaviours,
like the class it belongs to.

 $$\begin{aligned}
   g(x) = y \end{aligned}$$

In the non ideal world, however, there is always something missing that
stops us from knowing the entire truth. $g$ is beyond reach. In such
cases we resort to probability.

 $$\begin{aligned}
  n(x) = P(y=1|x)\end{aligned}$$ 

It simply tells us how probable is the
data belonging to a class($y=1$) if my observations are $x$.

*If we build a classifier on this data, how good will it be?* This is
the question Bayes error answers.

Bayes Error
===========

Lets say I've built a classifier $h$ to predict the class of data.
$h(x)=\hat{y}$ is the predicted class and $y$ is the true class. Even
ambiguous data needs to come from somewhere, So we assume $D$ is the
joint distribution of $x$ and $y$.

 $$\begin{aligned}
  er_D[h] = P_D[h(x) \neq y]\end{aligned}$$ Using an old trick to
convert probability to expectation, $P[A] = E[1(A)]$, we have
$$\begin{aligned}
  er_D[h] = E_{x,y}[1(h(x)\neq y)] = E_x E_{y|x}[1(h(x)\neq y)]\end{aligned}$$
The inner expectation is easier to solve when expanded.
$$\begin{aligned}
  E_{y|x}[1(h(x)\neq y)] = 1(h(x)\neq +1) P(y=+1|x) + 1(h(x)\neq -1)P(y=-1|x)\end{aligned}$$
Which give the final error to be

 $$\begin{aligned}
  er_D[h] = E_x[1(h(x)\neq +1) n(x) + 1(h(x)\neq -1)(1-n(x))]\end{aligned}$$

The last equation means, if the classifier predicts $+1$ for the data,
it will contribute $n(x)$ to the error. On the other hand if it predicts
$-1$ for the data, the contribution will be $1-n(x)$.

The best classifier would predict $+1$ when $n(x)$ is small and $-1$
when $n(x)$ is large. The minimum achievable error is then
$$\begin{aligned}
  er_D = E_x [\min(n(x),1-n(x))]\end{aligned}$$ This error is called
**Bayes Error**.

References
==========

[Shivani Agarwal's
lectures](http://drona.csa.iisc.ernet.in/~e0270/Jan-2015/)
