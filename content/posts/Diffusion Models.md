---
title: Diffusion Models
tags : []
date: 2023-04-22T10:21:00+05:30
startdate: 2023-04-22T10:21:00+05:30
draft: true
---




# Diffusion Models

## Transitions and markov kernels



## Two trajectories of diffusion

Diffusion is a process when a distribution $q(x_0)$ is gradually converted to a (well behaved) distribution $\pi(y)$ by repeated application of a [markov diffusion kernel][Markov kernel] $K_\pi(y|y^\prime;\beta)$ where $\beta$ is the diffusion rate. Definition taken from [Sohl-Dickstein et al. (2015)]

We can pictorically represent the diffusion process as follows.
$$x_0 \rightsquigarrow \cdots \rightsquigarrow x_t \to x_{t-1} \rightsquigarrow \cdots \rightsquigarrow x_T$$

Each transition in the process above is given by 

$$q(x_t|x_{t-1}) = K_\pi(x_t|x_{t-1};\beta_t)$$

<comment>A sequence of points forms trajectory. But how do we represent a specific type of trajectory? We use joint probability distribution. </comment>

The **forward trajectory** is starting with $q(x_0)$ and performing T steps of diffusion

$$q(x_{0:T}) = q(x_0)\prod_{t=1}^{T}q(x_t|x_{t-1})$$


We can similarly define a **reverse trajectory** where we start out with distribution $\pi(y)$ and end up with $p(x_0)=q(x_0)$.

$$p(x_T) = \pi(x_T)$$
$$p(x_{0:T}) = p(x_T)\prod_{t=1}^{T}p(x_{t-1}|x_{t})$$

## Diffusion based generative models
If the target distribution of the diffusion process $\pi(y)$ is a simple distribution like $N(0,I)$ then we can use this to design a generative model. 

If we start with data keep adding noise to it in small increment, over iterations, we can end up with just noise. If we can controll the variance schedule of the noise, we will end up with a sample from $N(0,I)$. We just described a forward trajectory of a diffusion. The following equation describes such a variance schedule. $\beta_t$ is slowly increased from 0 to 1.

$$q(x_t|x_{t-1}) = N(x_t; \left(\sqrt{1-\beta_t}\right)x_{t-1}, \beta_t I)$$

Now there is no value in adding noise. But the reverse trajectory would create an image from noise. If we learn the reverse transitions, we have a generative model. A diffusion based generative model.

$$p(x_T) = N(0,I)$$
$$p(x_{0:T}) = p(x_T)\prod_{t=1}^{T}p_\theta(x_{t-1}|x_{t})$$

---
q(x_T|x) \sim N(0,I) when T \to \infty

* p(x_0) is the data we get back from the generative model. We can train the reverse process by maximsing the probablity of p(x_0) being data. 

$$\log p(x) \geq E_ {q(z|x)}[\log p(x|z)] - D_ {KL}(q(z|x), p(z))$$


-
[Sohl-Dickstein et al. (2015)]

$$x_t \mathop{\longrightarrow}^{q(x_t|x_{t-1})} x_{t-1}$$
$$x_t \mathop{\longleftarrow}_ {p(x_{t-1}|x_t)} x_{t-1}$$



$$p(x) = \int_z p(x,z) dz$$
$$= \int_z p(x,z) \frac{q(z|x)}{q(z|x)} dz$$
$$= \int_z q(z|x) \frac{p(x,z)}{q(z|x)} dz$$
$$= \int_z q(z|x) \frac{p(x|z)p(z)}{q(z|x)} dz$$
$$= \int_z q(z|x) p(z) \frac{p(x|z)}{q(z|x)} dz$$


## Denoising diffusion probabilistic models

**Latent variable models as generative models**

Latent variable models assume that the original data distribution is produced by a process which stems from some innate property of the data. These innate properties are represented by latent vectors $z$. The oriignal distribution can be written in a marginal form. 

$$p(x) = \int p(x,z)dz$$

The generation process is given by $p(x|z)$. But, to first we have to model the posterior to discover these innate properties i.e. $p(z|x)$ <- this is wrong?? we should model p(z) and sample z and then generate data p(x|z). 

The posterior is often hard to compute. There are various techniques, variational inference [ref] among others, which approximates p(z|x) which a simpler distribution q(z)

* First we sample a latent variable from posterior $p(z|x)$ or its approximation. The generation process is evaluating $p(x|z)$
* As we did in Variational Inference, 

**diffusion**

Simply put, we progressively add noise to a data point until we reach isotropic gaussian. Now, generative process is reversing this.

$$x_0 \leadsto \cdots \leadsto x_{t} \to x_{t+1} \leadsto \cdots \leadsto x_T$$
[Ho et al. (2020)]

$$x_{t} \to x_{t-1} \equiv p_\theta(x_{t-1}|x_t)$$
$$x_{t-1} \to x_{t} \equiv q(x_{t}|x_{t-1})$$


**Connection between diffusion and latent variable models**

We assume that $x_0$ is the data variable and $x_{1:T}$ are its latent variables. Since we want the sequence of $x_0, ... ,x_T$ to be the sequence from diffusion process, we model it using Markov chain with transition probabilities defined. 

Diffusion models are latent variable models of form

$$p_\theta(x_0) = \int p_\theta(x_0,x_1:T) dx_{1:T}$$

The joint density is defined by a markov chain as

$$p(x_{0:T}) = p(x_T)\prod_{t=1}^{T} p_{\theta}(x_{t-1}|x_t)$$

$$p_{\theta}(x_{t-1}|x_t) = N(x_{t-1}; \mu_{\theta}(x_t,t),\Sigma_{\theta}(x_t,t))$$
$$p(x_T) = N(0,I)$$



## Score Function

Is considered gradient of the data distribution. But it is gradient of log  of data distribution. 
$$\nabla_x log p(x)$$


Why is it so great?
$$p(x) = \frac{e^{-f_\theta (x)}}{Z_\theta}$$  in energy based models.  $\theta$ is learnable parameters. 

$Z_\theta$ is intractable. 

$$\nabla_x \log p(x) = - \nabla_x f_\theta(x) - \nabla_x log Z_\theta = - \nabla_x f_\theta(x)$$ ...  No $Z_\theta$



Also, from langevin dynamics, we have a way to sample from $p(x)$ by using just $\nabla_x \log p(x)$

$$x_i+1 ← x_i + \epsilon \nabla_x \log p(x) + \sqrt{2\epsilon} z_i$$

$z_i \sim N(0,I)$

$K → \infty$ and $\epsilon \to 0$ then $x_K \sim p(x)$
ref: [Yang Song 2021 score]

[Welling et al. (2011)]

## Consistency Models
[Song et al. 2023]

## References
<small>

- [Ho et al. (2020)]: Ho, Jonathan, Ajay Jain, and Pieter Abbeel. "_[Denoising diffusion probabilistic models][Ho et al. (2020)]_". Advances in Neural Information Processing Systems 33 (2020): 6840-6851.

- [Sohl-Dickstein et al. (2015)]: Sohl-Dickstein, Jascha, Eric Weiss, Niru Maheswaranathan, and Surya Ganguli. "_[Deep unsupervised learning using nonequilibrium thermodynamics.][Sohl-Dickstein et al. (2015)]_" In International Conference on Machine Learning, pp. 2256-2265. PMLR, 2015.

- [Song et al. 2023]: Song, Yang, Prafulla Dhariwal, Mark Chen, and Ilya Sutskever. "_[Consistency models.][Song et al. 2023]_" arXiv preprint arXiv:2303.01469 (2023).

- [Welling et al. (2011)]: Welling, Max, and Yee W. Teh. "_[Bayesian learning via stochastic gradient Langevin dynamics.][Welling et al. (2011)]_" Proceedings of the 28th international conference on machine learning (ICML-11). 2011.

- _[Generative Modeling by Estimating Gradients of the Data Distribution][Yang Song 2021 score]_ by Yang Song

- _Markov kernel_ : [https://en.wikipedia.org/wiki/Markov_kernel][Markov kernel]

[Ho et al. (2020)]:    <https://arxiv.org/pdf/2006.11239.pdf>
    "Ho, Jonathan, Ajay Jain, and Pieter Abbeel. \"Denoising diffusion probabilistic models\". Advances in Neural Information Processing Systems 33 (2020): 6840-6851."
    
[Sohl-Dickstein et al. (2015)]:    <https://arxiv.org/pdf/1503.03585.pdf>
    "Sohl-Dickstein, Jascha, Eric Weiss, Niru Maheswaranathan, and Surya Ganguli. \"Deep unsupervised learning using nonequilibrium thermodynamics.\" In International Conference on Machine Learning, pp. 2256-2265. PMLR, 2015."
    
[Song et al. 2023]:    <https://arxiv.org/abs/2303.01469>
    "Song, Yang, Prafulla Dhariwal, Mark Chen, and Ilya Sutskever. \"Consistency models.\" arXiv preprint arXiv:2303.01469 (2023)."
    
[Welling et al. (2011)]:    <https://www.stats.ox.ac.uk/~teh/research/compstats/WelTeh2011a.pdf>
    "Welling, Max, and Yee W. Teh. \"Bayesian learning via stochastic gradient Langevin dynamics.\" Proceedings of the 28th international conference on machine learning (ICML-11). 2011."
    
[Yang Song 2021 score]:    <https://yang-song.net/blog/2021/score>
    "Generative Modeling by Estimating Gradients of the Data Distribution by Yang Song"
    
[Markov kernel]:    <https://en.wikipedia.org/wiki/Markov_kernel>
        "Markov kernel"
    
</small>
