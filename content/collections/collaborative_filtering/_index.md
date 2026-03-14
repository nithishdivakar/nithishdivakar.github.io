---
title: "Collaborative Filtering"
type: "series_collection"
---

Whenever we discuss about collaborative filtering, the following image is
implicitly made as a anchor point to talk about how
collaborative filtering discovers  'similar users' and use that to
recommend unseen items.

$$
\begin{array}{c|cccccc|}
 & i_1 & i_2 &  & \cdots &  & i_n \\\\
\hline
u_1 & & \checkmark & & & & \checkmark \\\\
%\hline
u_2 & \checkmark & \checkmark & & & & \\\\
%\hline
& \checkmark & & & \checkmark & \checkmark & \checkmark \\\\
%\hline
\vdots& & & \checkmark & & & \\\\
%\hline
& \checkmark & \checkmark & & \checkmark & \checkmark & \checkmark \\\\
%\hline
u_m & & \checkmark & & \checkmark & & \\\\
\hline
\end{array}
$$
<center><small><b>Fig:</b> The mythical user item interaction matrix.</small></center>


It's a helpful mental model and historically accurate for early recommender systems.

However, that *similar users* picture is only a small part of how modern recommendation models actually work. Real-world systems rarely operate directly on this matrix, and the notion of similarity today is far more nuanced than simple row-to-row comparison.

This 5 part series is a walkthrough of how collaborative filtering is practiced today. We will talk about how the row-to-row comparison idea evolves into one of the cornerstones of modern recommender systems.

1. [Collaborative Filtering - The Foundations and Flaws](01)
2. [The "Zero" Problem](02)
3. [Scaling CF with Neural Networks and Features](03)
4. A Tale of Two Towers: Scalable Architectures for Ranking
5. How Do We Know It’s Working?