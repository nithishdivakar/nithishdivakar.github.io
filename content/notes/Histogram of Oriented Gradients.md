---
title: Histogram of Oriented Gradients
layout: post
tags: [computer-vision]
date: 2022-03-12T00:00:30+05:30
draft: false
---

# Histogram of Oriented Gradients

Steps to compute HoG of an image.
- **Gradients computation:** Compute image gradients $G_x$ and $G_y$ by convolving the image with $[−1,0,1]$  and $[−1,0,1]^{T}$ respectively
- **Magnitude and direction** of each pixel 
$$\begin{aligned}
    m &= \sqrt{G_x^2+G_y^2}
    &
    \theta &=  \tan^{-1}\left(\frac{G_y}{G_x}\right)
\end{aligned}$$
-  For each cell in the image ($8 \times 16$)
	- **Oriented histogram** The histogram is created by binning pixel orientation $\theta$ 
    - For a consecutive bin pair $(\theta_l,\theta_r)$ where a pixel $(m,\theta)$ falls, the histogram is populated as
    $$\begin{aligned}
    V(\theta_l) &= \frac{(\theta-\theta_L)}{|bin|}m
    &
    V(\theta_r) &= \frac{(\theta_r-\theta)}{|bin|}m
        \end{aligned}$$
- **Normalise histograms**
Combine(concatenate) histograms of neighbouring $2 \times 2$ overlapping cells blocks and $\ell_2$ normalise this histogram. This step is to prevent lighting based variations in the image on the histogram 
