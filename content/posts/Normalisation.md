---
title: Normalisation Layers
tags : [machine-learning]
date: 2023-10-24T18:33:10+05:30
start_date: 2023-08-12T15:16:00+05:30
draft: false
---


# Normalisation

Regulating the magnitude of activations inside a neural network is crucial for an effective training regime. We may get stuck in local minima or worse yet, the training may diverge otherwise. For this, we make use of normalisation.

Normalisation comes in two flavours. Weight normalisation and Layer normalisation. We briefly touch on some fundamental techniques in both. 


## Weight normalisation
In weight normalisation, we focus on the magnitude of the parameters of the network; preventing them from uncontrollable growth or collapse. The basic technique appeared in [Salimans et al. (2016)] which describes a simple scenario. 

Given a network layer

$$y = \phi(w \cdot x+b)$$

We constrain the weight by reparameterising it as

$$w = g\frac{v}{\\|v\\|}$$
 
This constraints the norm of $w$ to be always $g$, the growth parameter.

### Spectral Normalization

If we consider the parameter of the layer/network as matrix, then we can device normalisation schemes using matrix norms. One such technique is spectral norm. It was first described in [Miyato et al. (2018)]. 

Given the weight matrix, we normalise it by its spectral norm

$$W \gets \frac{W}{\sigma(W)}$$

[Spectral norm][Matrix Norm] is an induced vector norm defined as 

$$\sigma(A) = max_{h \neq 0}\frac{\\|Ah\\|_ 2}{\\|h\\|_ 2}$$

To recall, this is the formulation of the largest singular value of $A$ and hence, spectral norm stabilizes the [Lipschitz constant][Lipschitz Continuity] of the weight matrix. 

Spectral norm had found its initial use in [Generative Adversarial Networks (GANs)][Miyato et al. (2018)] for stabilising training by preventing mode collapse.


## Normalisation Layers

Normalisation layers are like any other layers in a neural network which takes applied transformations on its input. But their primary purpose is to stablise the activations. They are places in the computational graph such that the further layers recieve a more stable inputs due to their action. 

### Batch Normalisation

The key idea behind batch norm is to normalise each feature of a sample. Ideally, if $x$ is the input feature, then the best normalisation is achieved if we do
$$x_f = \frac{x_f - \mathbb{E}[x_f]}{\sqrt{\operatorname{Var}[x_f]}}$$

But we don't have access to the exact population mean and variance. So we approximate it at run time with the mean and variance of the features in the mini-batch. Hence the name "batch norm".

Batch norm was introduced by [Ioffe et al. (2015)] and it has has 4 learnable parameters, each of size $F$, the number of features. 

$$y \gets \operatorname{BatchNorm}(x; \\{\bar{\mu}, \bar{\sigma}^2, \gamma, \beta \\})$$
After (and during) training, the layer converges its output to $\mathcal{N}(\beta, \gamma^2I)$. The layer does the following transforms during the forward pass of the training.

$$y_{b,f} = \gamma_{f}\left( \frac{x_{b,f}-\mu_{f}}{\sqrt{\sigma^2_{f}-\epsilon}} \right) + \beta_{f}$$
$$\mu_{f} \gets \frac{1}{B}\sum_b x_{b,f}$$
$$\sigma^2_{f} \gets \frac{1}{B} \sum_t (x_{b,f}-\mu_{f})^2$$

During inference batch statistics are not available. So batch norm keeps track of running average of the batch statistics during training in $\bar{\mu}$ and $\bar{\sigma}^2$. These are used during inference as mean and variance.

$$\bar{\mu}\_{f} \gets \operatorname{running-mean}(\mu_{f})$$
$$\bar{\sigma}\_{f}^2 \gets \operatorname{running-mean}(\sigma^2_{f})$$

Each of the features are normalised independently using batch statistics. The $\epsilon$ is constant added for numerical stability. 

**Why does batch norm work?**

_Internal co-variate shift_ was the original reasoning for batch norm discussed in [Ioffe et al. (2015)]. During training, when the lower layer's parameter changes, the output distribution changes. This leads to the following layers needing to constantly readjust its parameters. 

There has been some evidence against the internal covariate shift theory. See [Santurkar et al. (2018)]


### Layer Normalisation

While batch norm normalises each features independently, Layer norm normalises the total activation of a sample. Since we do not need to keep track of batch statistics, it only has 2 scalar parameters.

$$y \gets \operatorname{LayerNorm}(x; \\{\gamma, \beta \\})$$

Layer norm was introduces in [Lei Ba et al. (2016)] with the following definitions.

$$y_{b,f} = \gamma \left(\frac{x_{b,f}-\mu_{b}}{\sqrt{\sigma^2_{b}-\epsilon}}\right) + \beta$$

$$\mu_{b} = \frac{1}{F}\sum_f x_{b,f}$$
$$\sigma^2_{b} = \frac{1}{F} \sum_f (x_{b,f}-\mu_f)^2$$

Layer normalization is used in recurrent neural networks (RNNs) like architectures to address vanishing gradient problems.

> In a standard RNN, there is a tendency for the average magnitude of the summed inputs to the recurrent units to either grow or shrink at every time-step, leading to exploding or vanishing gradients. In a layer normalized RNN, the normalization terms make it invariant to re-scaling all of the summed inputs to a layer, which results in much more stable hidden-to-hidden dynamics. ~ *from [Lei Ba et al. (2016)]*

Since layer norm does not have any contribution from different samples of a same batch, it does the same computation during inference as well. For the same reason, it is also distributed training friendly as gradients depend only on the single sample. 

## RMSNorm
[Root Mean Square Layer Normalization][Zhang et al. (2019)] is a variant of Layer norm. The difference is that instead of normalising the data by mean centering and dividing by variance, the data is simply divided by RMS.

$$y \gets \operatorname{RMSNorm}(x; \\{\gamma\\})$$

RMS measures the quadratic mean of inputs.

$$\operatorname{RMS}(x_b) = \sqrt{\frac{1}{F}\sum_f x_{b,f}^2}$$

Then RMS norm is computed as

$$y_{b,f} = \gamma_f \frac{x_{b,f}}{\operatorname{RMS}(x_b)}$$

The main difference to LayerNorm is that RMSNorm is not re-centered and thus does not show similar linearity property for variable shifting. 

RMSNorm forces the summed inputs into a √n-scaled unit sphere. By doing so, the output distribution remains same regardless of the scaling of input. RMSNorm is invariant to the scaling of its inputs. It is not invariant to all re-centering operations.

## Normalisation Layers for data with channels

### Instance Normalization

For data with multiple channels, applying a normalisation technique like layer normalisation might result in one of the channels being saturated. For such scenario, we use [Instance Normalization][Ulyanov et al. (2016)].

The technique is similar to layer normalization, but the mean and variance statistics are calculated for each channels and instance independently. Instance normalization is commonly used in style transfer and image generation tasks.

### Group Normalization

[Group Normalization][Wu et al. (2018)] is a variant of Instance normalisation which attempts to strike a balance between Layer norm and Instance norm. The channels of a layer are divided into groups, and mean and variance statistics are computed for each group separately.

## References
<reference>
 <small>


- [Ioffe et al. (2015)]: Ioffe, Sergey and Szegedy, Christian "_Batch normalization: Accelerating deep network training by reducing internal covariate shift_" In  , (2015)


- [Lei Ba et al. (2016)]: Ba, Jimmy Lei and Kiros, Jamie Ryan and Hinton, Geoffrey E "_Layer normalization_" In arXiv preprint arXiv:1607.06450 , (2016)


- [Miyato et al. (2018)]: Miyato, Takeru and Kataoka, Toshiki and Koyama, Masanori and Yoshida, Yuichi "_Spectral normalization for generative adversarial networks_" In arXiv preprint arXiv:1802.05957 , (2018)


- [Salimans et al. (2016)]: Salimans, Tim and Kingma, Durk P "_Weight normalization: A simple reparameterization to accelerate training of deep neural networks_" In Advances in neural information processing systems 29, (2016)


- [Santurkar et al. (2018)]: Santurkar, Shibani and Tsipras, Dimitris and Ilyas, Andrew and Madry, Aleksander "_How does batch normalization help optimization?_" In Advances in neural information processing systems 31, (2018)


- [Ulyanov et al. (2016)]: Ulyanov, Dmitry and Vedaldi, Andrea and Lempitsky, Victor "_Instance normalization: The missing ingredient for fast stylization_" In arXiv preprint arXiv:1607.08022 , (2016)


- [Yang et al. (2019)]: Yang, Greg and Pennington, Jeffrey and Rao, Vinay and Sohl-Dickstein, Jascha and Schoenholz, Samuel S "_A mean field theory of batch normalization_" In arXiv preprint arXiv:1902.08129 , (2019)


- [Zhang et al. (2019)]: Zhang, Biao and Sennrich, Rico "_Root mean square layer normalization_" In Advances in Neural Information Processing Systems 32, (2019)


- [Wu et al. (2018)]: Wu, Yuxin and He, Kaiming "_Group normalization_" In Proceedings of the European conference on computer vision (ECCV) pp. 3--19, (2018)


- _[Lipschitz Continuity]_<br><small>_`https://en.wikipedia.org/wiki/Lipschitz_continuity`_ [accessed - Oct 2023]</small>


- _[Matrix Norm]_<br><small>_`https://en.wikipedia.org/wiki/Matrix_norm`_ [accessed - Oct 2023]</small>


[Ioffe et al. (2015)]:    <http://proceedings.mlr.press/v37/ioffe15.pdf>
    "Ioffe, Sergey and Szegedy, Christian \"Batch normalization: Accelerating deep network training by reducing internal covariate shift\" In  , (2015)"


[Lei Ba et al. (2016)]:    <https://arxiv.org/abs/1607.06450>
    "Ba, Jimmy Lei and Kiros, Jamie Ryan and Hinton, Geoffrey E \"Layer normalization\" In arXiv preprint arXiv:1607.06450 , (2016)"


[Miyato et al. (2018)]:    <https://arxiv.org/pdf/1802.05957.pdf>
    "Miyato, Takeru and Kataoka, Toshiki and Koyama, Masanori and Yoshida, Yuichi \"Spectral normalization for generative adversarial networks\" In arXiv preprint arXiv:1802.05957 , (2018)"


[Salimans et al. (2016)]:    <https://arxiv.org/pdf/1602.07868.pdf>
    "Salimans, Tim and Kingma, Durk P \"Weight normalization: A simple reparameterization to accelerate training of deep neural networks\" In Advances in neural information processing systems 29, (2016)"


[Santurkar et al. (2018)]:    <https://arxiv.org/pdf/1805.11604.pdf>
    "Santurkar, Shibani and Tsipras, Dimitris and Ilyas, Andrew and Madry, Aleksander \"How does batch normalization help optimization?\" In Advances in neural information processing systems 31, (2018)"


[Ulyanov et al. (2016)]:    <https://arxiv.org/abs/1607.08022>
    "Ulyanov, Dmitry and Vedaldi, Andrea and Lempitsky, Victor \"Instance normalization: The missing ingredient for fast stylization\" In arXiv preprint arXiv:1607.08022 , (2016)"


[Yang et al. (2019)]:    <https://arxiv.org/pdf/1902.08129>
    "Yang, Greg and Pennington, Jeffrey and Rao, Vinay and Sohl-Dickstein, Jascha and Schoenholz, Samuel S \"A mean field theory of batch normalization\" In arXiv preprint arXiv:1902.08129 , (2019)"


[Zhang et al. (2019)]:    <https://arxiv.org/pdf/1910.07467.pdf>
    "Zhang, Biao and Sennrich, Rico \"Root mean square layer normalization\" In Advances in Neural Information Processing Systems 32, (2019)"


[Wu et al. (2018)]:    <https://arxiv.org/abs/1803.08494>
    "Wu, Yuxin and He, Kaiming \"Group normalization\" In Proceedings of the European conference on computer vision (ECCV) pp.3--19, (2018)"


[Lipschitz Continuity]:    <https://en.wikipedia.org/wiki/Lipschitz_continuity>
    "Lipschitz Continuity"


[Matrix Norm]:    <https://en.wikipedia.org/wiki/Matrix_norm>
    "Matrix Norm"

</small>
</reference>
