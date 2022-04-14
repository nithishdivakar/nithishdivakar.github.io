---
title: Attribute Selection in Decision Trees
layout: post
tags: [machine-learning]
date: 2022-04-14T00:15:30+05:30
draft: false
---

# Attribute Selection in Decision Trees
For constructing a new node in decision tree, choosing which attribute to partition the data on is important. Choosing  a less desirable attribute to split the data on may result in lower performance. Lets look into a few important measures which helps us find the best attribute. 

## Information Gain

Information Gain is defined as amount of information gained about a random variable (outcome) from observing another (attribute). 
We can quantify information gain as difference in entropy when random variable is observed.

$$\begin{aligned}
    IG(T,A) &= H(T) - H(T|A)
	\\\\
    H(T) &= -\sum_{c\in C}^{}p_c\log_2 p_c
	\\\\
	H(T|A) 
	&= \sum_{a
    \in A}p_a H(T_a)
\end{aligned}$$
Here $H(T)$ is the entropy of set $T$ and $T_a = \\{t\in T: t_{A} = a\\}$ is its subset of items with attribute $A=a$. Also, $p_a = \frac{\left|T_a\right|}{|T|}$.

## GINI Impurity

GINI Impurity is a measure of how often a randomly chosen element from a set would be incorrectly labeled if it was randomly labeled according to the distribution of an attribute in the set.

Let say we partition the input set $T$ according to the values of attribute $A$ such that $T = \bigcup_{a\in A} T_a$.
The split would be ideal if each of the partitions would have only a single class (different subset can have same class). 

GINI impurity quantifies having multiple classes in same partition. 
$$\begin{aligned}
        G(T_a) &= 
        \sum_{c\in C}p_{a,c}\left(\textstyle\sum_{k \neq c} p_{a,k}\right)
        \\\\
		&=\sum_{c\in C}p_{a,c}(1-p_{a,c})
        \\\\
        &= 1 - \sum_{c\in C}p_{a,c}^2
\end{aligned}$$

Overall GINI Impurity score of partitioning $T$ according to $A$ is 
$$\begin{aligned}
    G(A) &= 
    \sum_{a\in A}p_{a}G(T_a) \quad 
	\\\\
	&= \sum_{a\in A} p_{a} \left(1- \sum_{c\in C}p_{a,c}^{2}\right)
\end{aligned}$$


$p_a$ fraction of elements which has attribute $a$
$p_{a,c}$ fraction of elements in class $c$ and has attribute $a$



## Variance Reduction

Variance reduction is used when target variable is continuous (tree is a regression tree). If the set $T$ is being partitioned into $T_L$ and $T_R$,  the reduction in variance is given by 
$$\begin{aligned}
    V(T) = Var(T) &- \left(\frac{|T_L|}{|T|}Var(T_L)+\frac{|T_R|}{|T|}Var(T_R)\right)  
\end{aligned}$$
For calculating the best split point, the standard variance calculation formula would require recalculation of mean repeatedly. But we can compute variance without explicitly calculating mean as
$$Var(S) = \frac{1}{|S|^2}\sum_{i,j\in S}(y_i-y_j)^2 $$
