---
layout: post
title: Bayes Error
date: 2018-02-11 20:57 +0530
---


> What is the best classifier you can build when your data is not enought to predict the labels?


## The god function. 

In an ideal world, everything has reason. Every question has a unambiguous answer. The data in sufficient to explain its behavious, like the class it belongs to.

$$ g(x) = y $$

In the non ideal world, however, there is always something missing that stops us from knowing the entire truth. No such function g exsit. In such cases we resort to probability.

$$n(x) = P(y=1|x)$$

It simply tells us how probable is the data belonging to a class(y=1) if my observations are x.

If I want to build a classifier on the data, how good can it be?

## Lets do the math.

Lets say I've built a classifier $h$ to predict the class of data. \(h(x)=\hat{y}\) is the predicted class and $y$ is the true class. Even ambiguous data needs to come from somewhere, So we assume $D$ is the joint distribution of $x$ and $y$. 

$$er_D[h] = P_D[h(x) \neq y]$$

Using an old  trick to convert probabilty to expectation, $P[A] = E[1(A)]$,  we have

$$er_D[h] = E_{x,y}[1(h(x)\neq y)] = E_x E_{y|x}[1(h(x)\neq y)]$$

The inner expectation is easier to solve when expanded.

$$E_{y|x}[1(h(x)\neq y)] = 1(h(x)\neq +1) P(y=+1|x) + 1(h(x)\neq -1)P(y=-1|x)$$

Which give the final error to be

$$er_D[h] = E_x[1(h(x)\neq +1) n(x) + 1(h(x)\neq -1)(1-n(x))]$$

## What does it all mean ?

The last equation means, if the classifier predicts +1 for the data, it will contribute n(x) to the error. On the other hand if it predicts -1 for the data, the contribution will be 1-n(x). 

The best classifier would predict +1 when n(x) is small and -1 when n(x) is large. The minumum achoevable error is then 

$$er_D = E_x [\min(n(x),1-n(x))]$$

This error is called **Bayes Error**.


### References

1. [Shivani Agarwal's lectures](http://drona.csa.iisc.ernet.in/~e0270/Jan-2015/)