---
layout: card
title : Naive Bayes for Sentiment Analysis
tags: [machine-learning]
date: 2021-09-14T05:04:51+05:30
draft: true
---

## Naive Bayes for Sentiment Analysis

Sentiment analysis is a stand-in for a classification problem in text. Given a document $x$ with label $y \in \\{c_1, \ldots, c_K\\}$, we want $\hat{c} = \arg\max_k P(c_k | x)$. The catch: the input is a variable-length sequence. We handle this with two simplifications: bag-of-words and conditional independence.

**Bag-of-words.** Modeling $P(x | c_k)$ over full sequences is intractable. Instead, treat a document as an unordered multiset of tokens $x = (x_1, x_2, \ldots)$ drawn from vocabulary $V$, discarding word order.

**Naive Bayes assumption.** Even with BoW, the joint over all words is hard due to correlations. We assume conditional independence given the class: $$P(x | c_k) = \prod_i P(x_i | c_k)$$ This is clearly violated in practice ("not good" is not independent), but the classifier only needs the *argmax* to be correct, not well-calibrated probabilities.

Applying Bayes' rule and dropping $P(x)$, then moving to log-space:
\begin{align*}
P(c_k | x) &\propto P(c_k) \prod_i P(x_i | c_k) \\\\
&\propto \log P(c_k) + \sum_i \log P(x_i | c_k)
\end{align*}

### Estimating the Parameters

**Class priors** are the fraction of documents in each class:
$$P(c_k) = \frac{|d \in c_k|}{|D|}$$

**Token likelihoods** count how often each word appears across documents in class $c_k$:
$$P(x_i | c_k) = \frac{|x_i \in d : d \in c_k|}{\sum_{j} |x_j \in d : d \in c_k|}$$

**Zero-frequency problem.** If a word never appears in class $c_k$ during training, $P(x_i | c_k) = 0$ zeros out the entire document's score. Fix with *Laplace smoothing*: add pseudo-count $\alpha$ to every word in every class. Using $\alpha \neq 1$ is called Lidstone smoothing; $\alpha$ is a hyperparameter.

$$P(x_i | c_k) = \frac{|x_i \in d : d \in c_k| + \alpha}{\sum_{j}|x_j \in d : d \in c_k| + \alpha|V|}$$

The $\alpha|V|$ in the denominator keeps the distribution normalised.

### The Linear Classifier

Setting $b_k = \log P(c_k)$, $W_{ik} = \log P(x_i | c_k)$, and a binarised document vector:
$$u_i = \begin{cases}1 & x_i \in d \\\\ 0 & x_i \notin d\end{cases}$$

the classifier reduces to:
$$\hat{c} = \arg\max_k \; b + uW$$

This is a **linear classifier**: a sparse dot product followed by argmax. Since $u$ is sparse, inference is fast even over large vocabularies.

**Binarised vs. term frequency.** Using raw counts $u_i = \text{count}(x_i, d)$ is an alternative, but binarised features often work as well or better for sentiment; seeing "great" five times is not five times as informative. **TF-IDF** goes further by downweighting words common across all classes (e.g. "the") and upweighting distinctive ones.

### Strengths and Weaknesses

*Fast and data-efficient*: training is a single pass; parameters are estimated independently, so it works well with small datasets. *Interpretable*: $W_{ik}$ directly shows which words characterise each class. No tuning beyond $\alpha$.

On the other hand, the independence assumption is almost always violated, word order is discarded entirely (negation fails), and the posterior probabilities are poorly calibrated. The model is systematically overconfident due to double-counting correlated evidence. Use the argmax, not the raw scores.