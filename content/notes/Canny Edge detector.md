---
title: Canny Edge detector
layout: post
tags: [computer-vision]
date: 2022-03-12T12:00:00+05:30
draft: false
---


# Canny Edge detector

Steps:
- Apply **Gaussian filtering** to smooth out noise in the image
- **Compute gradients**: Compute horizontal($G_x$) and vertical gradients ($G_y$). Magnitude and direction of gradients can then be compluted as 
    $$\begin{aligned}
        m &= \sqrt{G_x^2+G_y^2}
        &
        \theta &= \tan ^{-1}\left(\frac{G_y}{G_x}\right)
    \end{aligned}$$
    The angle is then rounded off so that $\theta \in \{0,45,90,135\}$
- **Non-maximal suppression**:  For each  pixel $(m,\theta)$, if its gradient intensity is maximum among the pixels in negative and positive gradient direction, the value is preserved. Otherwise it is suppressed. 
- **Double thresholding**
    $$\begin{aligned}
        m \geq t_h &\implies  \text{strong edge pixel}
        \\\\
        t_l  < m < t_h &\implies  \text{weak edge pixel}
        \\\\
		m \leq t_l &\implies  \text{suppress}
    \end{aligned}$$
- **Edge tracking by hysteresis**: All strong pixels are selected as true edge pixels. All the weak pixels which has a strong pixel in its $8 \times 8$ neighbourhood are also selected as a true edge. All the others are removed. 