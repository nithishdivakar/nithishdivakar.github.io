---
date: 2026-03-15 00:00:00 +0000
layout: post
level: h1
slug: '04'
tags : [recommendation system]
status: todo
draft: done
title: "A Tale of Two Towers"
type: "series_collection"
---

# A Tale of Two Towers

*4/5 of [Collaborative Filtering](/collections/collaborative_filtering) Collection* 


In [part 3](../03), we replaced lookup tables with parameterised functions realised by neural networks. User and item representations are now *computed* from features, not retrieved from a table.

$$P(\text{click} \mid \\{u, i\\}) = \sigma\left( g_{\theta}(x_u)^\top h_\phi(x_i)\right)$$

How do we use this to serve recommendations to user?

The immediate answer to this also reveals its flaw: for a given user, score every item in the catalogue and recommend the top-k ... but (from [part 01](../01))

- R1: We have lots of users
- R2: We have lots of content

Thats a lot of formward passes. 

## Neighbours in Two Towers

Half the solution is already there. We just have to look at it differently. Our model is:

$$P(\text{click} \mid \\{u, i\\}) = \sigma\left( g_{\theta}(x_u)^\top h_\phi(x_i)\right)$$

Lets look at an expanded version of the same equation.

$$
\begin{array}{ccccc}
 & & P(\text{click} \mid \\{u, i\\}) && \\\\
 & & \Big\uparrow &  &\\\\
p_u & \longrightarrow& \sigma(p_u^Tq_i)  &\longleftarrow& q_i \\\\
\Big\uparrow &    & & & \Big\uparrow \\\\
\boxed{g_\theta} &  & & &  \boxed{h_\phi} \\\\
\Big\uparrow &  & & & \Big\uparrow \\\\
x_u &  & & &  x_i \\\\
\end{array}
$$

The user side and the item side are completely independent until the very last step. $g_\theta$ only ever sees user features. $h_\phi$ only ever sees item features. They interact exactly once for the dot product.

The illustration also shows two parallel structures that interact only at the very top. This model is hence known as the **Two-Tower model**. Its more of an architecture name or a architecture template name. 

The structure also means we don't have to evaluate the whole network for every request. We can evaluate the towers independently and reuse the results again and again.
 
**Item embeddings:** Item features don't change on every request. A movie's genre, duration, and release date are fixed. So we can run every item through $h_\phi$ once, offline, and store all the resulting vectors $q_i$. Every item in the catalogue, computed once. In a production system these are periodically refreshed as the model is retrained.
 
**User embeddings:** User features are more dynamic. Recent watch history, for example, updates frequently. For existing users, we can pre-compute $p_u$ periodically and store it. For brand-new users, we compute it on the fly at request time. Either way, it's one forward pass through $g_\theta$.
 
So at serving time, we have $p_u$ in hand and a table of pre-computed $q_i$. The scoring problem reduces to: find the items $i$ where $p_u^T q_i$ is highest.
 
## Finding the Nearest Neighbours
 
Maximising $p_u^T q_i$ over all items is equivalent to finding the items whose embedding is closest to the user's embedding. In other words, its nearest neighbours.
 
The obvious approach is to compute the dot product with all item embeddings and fetch the top-k items with the highest score. We've gone from needing a humongous number of neural network forward passes to a humongous number of dot products. To put this in perspective, the difference is needing GPUs to needing only CPUs for recommendations.
 
A humongous number of dot products is also obviously expensive, but it is a highly [data parallel](https://en.wikipedia.org/wiki/Data_parallelism) computation. So we can throw a lot of parallel compute at it and make it work fast. This approach does scale to moderately sized systems.
 
But what if we have a lot more users, a lot more items, or both?
 
If we have that many items, do we actually need the exact top-100? If we miss a few here and there, would it be so bad?

***Approximate* Nearest Neighbours**.
 
The idea behind ANN search is quite simple. Instead of scanning every vector, ANN algorithms build an index structure over the stored embeddings by clustering nearby vectors together so that at query time, only a small fraction of the space needs to be searched. We skip the obviously distant regions entirely.
 
Libraries like [FAISS](https://github.com/facebookresearch/faiss), [ScaNN](https://github.com/google-research/scann), and [HNSW](https://github.com/nmslib/hnswlib) can find the top-k approximate nearest neighbours among millions of vectors in under 10 milliseconds.
 
So the full serving pipeline for a user request is:
1. Compute $p_u = g_\theta(x_u)$.
2. Query the ANN index with $p_u$. We get results in milliseconds.
3. Return the top-k items.
 
The item tower is never invoked at request time. All of that computation happens offline, and the ANN index is built ahead of serving.
 
## Making the Model Better
 
The architecture above works. But how do we make it better?
 
Because $g_\theta$ and $h_\phi$ are completely separate, the model can never learn signals that depend on the *combination* of a user and an item.

- It cannot learn that a user who just finished a three-hour documentary is more likely to click on another long-form piece.
- It cannot learn that sensitivity to release date depends on the genre the user is currently in the mood for. 

These are **cross-feature interactions**. Patterns that only become visible when you look at user and item features together.
 
In our current model, all of this has to be compressed into a single dot product between $p_u$ and $q_i$.
 
One natural extension is instead of a dot product, use another network.
 
$$P(\text{click} \mid \\{u, i\\}) = f_\psi(p_u \oplus q_i)$$
 
where $f_\psi$ takes both embeddings as input and produces a score. The final step can now learn richer interactions between the two representations. This gains expressiveness while keeping the towers separate. Item embeddings can still be pre-computed.

$$
\begin{array}{c}
P(\text{click} \mid \\{u, i\\})\\\\
\Big\uparrow\\\\
\boxed{f_\psi}\\\\
\Big\uparrow\\\\
\underset{\textstyle
\begin{array}{c}
\Big\uparrow\\\\
\boxed{g_\theta}\\\\
\Big\uparrow\\\\
x_u
\end{array}
}{p_u}
\oplus
\underset{\textstyle
\begin{array}{c}
\Big\uparrow\\\\
\boxed{h_\phi}\\\\
\Big\uparrow\\\\
x_i
\end{array}
}{q_i}
\end{array}
$$

The $f_\psi$ network's output has to be computed eveytime we need the click porbability. But $p_u$ and $q_i$ can be cached. So usually, we keep the $f_\psi$ small.

But we can take this design to the end of the spectrum. We can simply concatenate the raw user and item features and feed everything into a single shared network. The network is just $f_\psi$ and nothing else. 
 

$$
\begin{array}{c}
P(\text{click} \mid \\{u, i\\})\\\\
\Big\uparrow\\\\
\boxed{f_\psi}\\\\
\Big\uparrow\\\\
x_u
\oplus
x_i
\end{array}
$$

This is the **Cross-Tower** model. Every layer of the network can attend to both user and item features simultaneously. Models like [DCN v2](https://arxiv.org/abs/2008.13535), [DeepFM](https://arxiv.org/abs/1703.04247), and [DLRM](https://arxiv.org/abs/1906.00091) are all variations on this theme, each with different approaches to how cross-feature interactions are modelled.


This family of architectures is also described using the language of **fusion**: the Cross-Tower model is *early fusion* and the Two-Tower model is *late fusion*. The entire design space is defined by where along the network the two towers fuse into one.

## The Fusion Model Family

The Fusion model family represents a tradeoff spectrum. Each architecture sits somewhere between how much cross-feature interaction it allows and how much can be pre-computed.

Why can't we simply maximise both?

- More pre-computable means the towers stay separate for longer $\implies$ less opportunity for cross-feature interaction.
- More expressive means fusing earlier $\implies$ less to pre-compute.

These pull in opposite direction. Its basically a *speed vs performance* tradeoff.

The Two-Tower model is fast because the towers never see each other, and that's also why it's limited. The Cross-Tower model is expressive because user and item features are fused early, and that's also why it can't pre-compute anything.

Neither model is right for the whole problem.
 
## The Two-Stage Framework

> "The most fundamental problem in software development is complexity. There is only one basic way of dealing with it: divide and conquer." -- Bjarne Stroustrup

Neither model is right for the whole problem. But they don't have to be. We can split the problem into two stages, each designed around what it is actually good at.

Stage 1 does cheap computation to filter out most of the irrelevant items. Stage 2 then uses expensive but precise compute to carefully score the smaller, relevant set that remains.
This is a two-stage recommendation pipeline.
 
**Retrieval** uses the Two-Tower model to quickly narrow millions of items to a few hundred plausible candidates. Speed is the constraint. Precision is negotiable.
 
**Ranking** uses the Cross-Tower model to score those candidates carefully. Precision is the constraint. Speed is negotiable. We are only scoring hundreds, not millions.

$$
\begin{array}{c}
\underset{(millions)}{\text{All items}}\\\\
\Big\downarrow\\\\
\boxed{\begin{array}{c}\\\\ \\, \underset{(Two-Tower + ANN)}{\text{Retrieval}}\\,\\\\ \\,\end{array}}\\\\
\Big\downarrow\\\\
\underset{(hundreds)}{\text{Candidates}}\\\\
\Big\downarrow\\\\
\boxed{\begin{array}{c}\\\\ \\, \underset{(Cross-Tower)}{\text{Ranking}}\\,\\\\ \\,\end{array}}\\\\
\Big\downarrow\\\\
\text{Final Ranked List}
\end{array}
$$


Each stage does what it's actually good at. This two-stage architecture is how virtually every large-scale recommendation system is built today.
 
We can add more stages. An inverted index or partition system to filter out content in languages the user is not interested in. But these are tail end optimisations. The main structure is done.

The last question: how do we know if any of this is actually working?
 
*Read more in [part 5](../05)*.