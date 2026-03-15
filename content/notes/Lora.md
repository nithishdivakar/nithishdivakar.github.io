---
title: LoRA
layout: post
tags : [llm]
date: 2025-02-24T07:30:00+05:30
start_date: 2025-02-24T07:30:00+05:30
draft: false
---

# LoRA: Low-rank adaptation of large language models

Fine tuning a model can be thought of as computing a weight $\Delta W$ corresponding to each weight matrix $W$ in the model such that the finetuned model's weight is $W + \Delta W$. [LoRA][Edward and Yelong (2022)] explicitly models this as $W + \Delta W$ and only tunes $\Delta W$ during finetuning, keeping $W$ frozen.

Further more, since finetuning might not need the full expressive power of a full rank $\Delta W$, it is approximated as a product of 2 low rank matrices $\Delta W = UV$ where $U \in \mathbb{R}^{d \times r}$, $V \in \mathbb{R}^{r \times k}$ and $r \ll \min(d, k)$. This reduces the total number of parameters to tune.

$U$ is initialised with $0$s and $V$ is initialised with random Gaussian so that the effect of $\Delta W$ is $0$ at the beginning of finetuning.

## Advantages and uses
- We can finetune a base model to multiple usecases with each having its own set of $U, V$ parameters and the base weights preserved.
- Parameters to save per usecase is very small.
- Serving a different usecase requires only switching out $U$s and $V$s.
- Number of parameters to tune are small. For example, if the original weight matrix is $1000 \times 1000$ and we use a rank $r=5$ approximation, then the number of parameters we have to tune is only $\frac{2 \times 1000 \times 5}{1000^2} = 1\%$ of what full finetuning would require. This also carries over to fewer gradient computations.

## DoRA

[DoRA][Shih and Chien (2024)] (Weight-Decomposed Low-Rank Adaptation) extends [LoRA][Edward and Yelong (2022)] by decomposing the adapted weight into a magnitude and a direction component. Any matrix $W$ can be written as a magnitude scalar times a unit-norm matrix. DoRA finetunes both:

$$\bar{W} = m \frac{W + UV}{\|W + UV\|_c}$$

where $\|\cdot\|_c$ is the column-wise norm and $m$ is a learnable magnitude vector. $UV$ is the same low-rank update as in LoRA. This decoupling lets the model adjust the scale and direction of each weight column independently, which the authors show better mimics the behaviour of full finetuning compared to LoRA alone.

## References
<reference>
 <small>

- [Edward and Yelong (2022)]: Hu, Edward J and Shen, Yelong and Wallis, Phillip and Allen-Zhu, Zeyuan and Li, Yuanzhi and Wang, Shean and Wang, Lu and Chen, Weizhu and others "_LoRA: Low-rank adaptation of large language models._" In ICLR 1, (2022)

- [Shih and Chien (2024)]: Liu, Shih-Yang and Wang, Chien-Yi and Yin, Hongxu and Molchanov, Pavlo and Wang, Yu-Chiang Frank and Cheng, Kwang-Ting and Chen, Min-Hung "_DoRA: Weight-decomposed low-rank adaptation_" In Forty-first International Conference on Machine Learning, (2024)

[Edward and Yelong (2022)]:    <https://arxiv.org/abs/2106.09685>
    "Hu, Edward J and Shen, Yelong and Wallis, Phillip and Allen-Zhu, Zeyuan and Li, Yuanzhi and Wang, Shean and Wang, Lu and Chen, Weizhu and others \"LoRA: Low-rank adaptation of large language models.\" In ICLR 1, (2022)"

[Shih and Chien (2024)]:    <https://arxiv.org/abs/2402.09353>
    "Liu, Shih-Yang and Wang, Chien-Yi and Yin, Hongxu and Molchanov, Pavlo and Wang, Yu-Chiang Frank and Cheng, Kwang-Ting and Chen, Min-Hung \"DoRA: Weight-decomposed low-rank adaptation\" In Forty-first International Conference on Machine Learning, (2024)"

</small>
</reference>