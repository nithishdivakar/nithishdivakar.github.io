---
title: LoRA
tags : []
date: 2025-02-24T07:30:00+05:30
start_date: 2025-02-24T07:30:00+05:30
draft: true
---

# LoRA: Low-rank adaptation of large language models


Fine tuning a model can be thought of as computing a weight $H$ corresponding to each weight matrix $W$ in the model such that finetuned model's weight is $W+H$. LoRA explicitly models each weight in the base model as $W+H$ with $H$ and only tunes $H$ during finetuning.

Further more, since the fintuning might not need full expressive power of a full rank $H$, it is  is approximated as product of 2 low rank matrices $H=UV$. This reduced the total number of parameters to tune.

$U$ is initlised with $0s$ and $V$ is initialised with random gaussian so that the effect of $H$ is $0$ at the begning of the finetuning.

## Advantages and uses
- We can fintune a base model to multiple usecases with each having its own set of parameters and the base weights preserved. 
- Parameters to save per usecase is very less. 
- Serving a different usecase requires only switchign out $Us$ and $Vs$. 
- Number of parameters to tune are small. For example, if the original weight matrix is $1000\times 1000$ and we use rank 5 approximation, then the number of parameters we have to tune is only $\frac{(2\*1000\*5)}{(1000^2)} =1\\%$ if we have used normal finetuning. This also carries over as less parameters to compute gradient for.

## DoRA

$$\bar{W} = m\frac{W + UV}{\\|W + UV\\|_c}$$

[LoRA paper][Edward and Yelong (2022)]

[DoRA paper][Shih and Chien (2014)]
## References
<reference>
 <small>


- [Edward and Yelong (2022)]: Hu, Edward J and Shen, Yelong and Wallis, Phillip and Allen-Zhu, Zeyuan and Li, Yuanzhi and Wang, Shean and Wang, Lu and Chen, Weizhu and others "_LoRA: Low-rank adaptation of large language models._" In ICLR 1, (2022)


- [Shih and Chien (2014)]: Liu, Shih-Yang and Wang, Chien-Yi and Yin, Hongxu and Molchanov, Pavlo and Wang, Yu-Chiang Frank and Cheng, Kwang-Ting and Chen, Min-Hung "_DoRA: Weight-decomposed low-rank adaptation_" In Forty-first International Conference on Machine Learning pp. , (2024)


[Edward and Yelong (2022)]:    <https://arxiv.org/abs/2106.09685>
    "Hu, Edward J and Shen, Yelong and Wallis, Phillip and Allen-Zhu, Zeyuan and Li, Yuanzhi and Wang, Shean and Wang, Lu and Chen, Weizhu and others \"LoRA: Low-rank adaptation of large language models.\" In ICLR 1, (2022)"


[Shih and Chien (2014)]:    <https://arxiv.org/abs/2402.09353>
    "Liu, Shih-Yang and Wang, Chien-Yi and Yin, Hongxu and Molchanov, Pavlo and Wang, Yu-Chiang Frank and Cheng, Kwang-Ting and Chen, Min-Hung \"DoRA: Weight-decomposed low-rank adaptation\" In Forty-first International Conference on Machine Learning pp., (2024)"

</small>
</reference>
