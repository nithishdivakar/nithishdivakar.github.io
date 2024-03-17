---
title: Sampling in a Sphere
tags : [statistics,probability]
date: 2024-03-17T21:44:15+05:30
start_date: 2024-03-10T09:36:53+05:30
draft: false
---

# Sampling in a Sphere
Understanding how to generate a uniform sample of points inside a sphere takes us through a few interesting topics. So let begin with the end in mind. 

The following algorithm generates a uniform sample of points inside sphere in n dimensions.

$$u_1, \ldots, u_{n+2} \sim \mathcal{N}(0,1)$$
$$x_1, \ldots, x_n = \frac{(u_1,\ldots, u_n)}{\sqrt{u_1^2+\ldots+u_{n+2}^{2}}}$$

There is a lot to unpack here.
- Why are we sampling from a normal distribution to get a uniform distribution?
- Why $n+2$ ?
- Why are we dropping 2 coordinates?

## What is inside a Sphere?
A sphere is defined as a set of points which are equidistant from a point known as center. For this article, we mostly deal with unit spheres. A unit n-sphere with center at origin can be defined as
$$ S^n = \\{x \in \mathbb{R}^{n} ~:~ \\\|x\\\| = 1\\} $$

This includes only the periphery of the region. Or the circumference. An n-ball however is the whole region inside the n-sphere. 
$$ B^n = \\{x \in \mathbb{R}^{n} ~:~ \\|x\\| \leq 1 \\}$$
Note that the $B^n$ is a closed ball so $S^n \subset B^n$. 

Some quick facts about the unit n-ball and n-sphere
- Both can be completely inscribed in the region $[-1,1]^n$
- [Volume of an n-ball][Volume of an n ball] is given by $$\operatorname{vol}[B^n]  = \frac{\pi^{n/2}}{\Gamma(\frac{n}{2}+1)}$$
  This fomula simplyfies to $\pi r^2$ and $\frac{4}{3}\pi r^2$ for a circle and 3d sphere. 

  
## When Spheres are Circles
In 2 dimensions, there is simple technique get uniformly sampling points within a circle. Rejection sampling. Generate unifom random samples inside $[-1,1]^2$ and reject all the samples which are outside the circle. 

```python
while True:
  x ~ U[-1,1]
  y ~ U[-1,1]
  if x^2+ y^2 <= 1:
    return (x,y)
```
However, efficiency of rejection sampling depends on how many samples are accepted; which is ratio of area of the circle to the area of the $2 \times 2$ square. and that about
$$\frac{\pi 1^2}{4} \approx 78.5\\\%$$ 

We can extend the technique for higher dimensions but it has a critical flaw. The curse of dimensionality. The efficiency of rejection sampling for generating uniform sampling of points for n-sphere is 

$$\frac{\operatorname{vol}[B^n]}{2^{n}}$$

In 3 dimensions the efficiency drops to $\approx 52.33\\%$ and by the time we get to 10 dimensions, its $ \frac{\pi^5/5!}{2^{10}} \approx 0.249\\% $. i.e we end up rejecting $99.7\\%$ of the generated points. It worse further up.

## On the circumference
If we restrict ourselves to get uniform sampling of point on the circumference of the circle, there is an easier techqnique. The technique is an inversion of [Marsaglia's polar method][Marsaglia polar method] for generating standard normal random numbers. 

In 2D the technique is 

$$u,v \sim \mathcal{N}(0,1)$$
$$x,y = \frac{u,v}{\sqrt{u^2+v^2}}$$

It seems a bit strange why this would generate random uniform points on the circle's circumference. Especially since we begin sampling from a normal distribution. But the proof is simple. Let take a look at the join distribution of $(u,v)$. Since both are normally distributed and independent of each other, we have

$$f(u,v)  = \left(\frac{1}{\sqrt{2\pi}} e^{-\frac{1}{2}u^2}\right) \left(\frac{1}{\sqrt{2\pi}} e^{-\frac{1}{2}v^2}\right)$$
$$= \frac{1}{2\pi} e^{\frac{1}{2} (u^2+v^2)}$$

The joint distribution of $(u,v)$ only depends on its distance from origin ($u^2+v^2$) and is invariant to direction. The last step in the algorithm where we normalise both point by this distance projects all $(u,v)$'s to the circle's circumference without any rotation. So they are uniformly distributed on the circle. 

We can extend the proof to n-dimensions

$$f(u_1,\ldots, u_n)  = \prod_i \left(\frac{1}{\sqrt{2\pi}} e^{-\frac{1}{2}u_i^2}\right) = \frac{1}{(2\pi)^{n/2}} e^{\frac{1}{2}\\|u\\|^2} $$
and so does the technique. Generating random uniform points on n-sphere is
$$u_i \sim \mathcal{N}(0,1) $$
$$ x = \frac{u}{\\|u\\|} $$

But what about generating uniformly sampled points inside the circle?

## From circumference to the center
> Uniformly distributed points on an $S^{n+2}$ are uniformly distributed on $B^{n}$.

This elegant results first observed by [Harman and Lacko][Harman and Lacko (2010)] and later proved by [Voelker et al. (2017)]. Following this result, we can generate uniform sampling of points in $B^n$ by first generating uniform sampling of points in $S^{n+2}$ and dropping (any) 2 coordinates.



$$u_1, \ldots, u_{n+2} \sim \mathcal{N}(0,1)$$
$$x_1, \ldots, x_n = \frac{(u_1,\ldots, u_n)}{\sqrt{u_1^2+\ldots+u_{n+2}^{2}}}$$


## ... but one last thing

There is one more technique which uses projection from n-sphere to get uniform sampling on points on n-ball. The key obsevation is that an n-ball is a collection of n-spheres of different radius
i.e $$ B^n[1] =  \bigcup_{x=0}^{1} S^n[x]$$

So first we sample a point in $S^n[1]$ and then move the point somewhere between origin and circumference. But there is a catch. The area of $S^n[x]$ is proportional to $x^n$, so we have to normalize accordingly.  So

$$u_1, \ldots, u_{n} \sim \mathcal{N}(0,1)$$
$$r \sim \operatorname{U}[0,1]$$
$$x  = r^{1/n} \frac{u}{\\|u\\|}$$

## References
<reference>
 <small>


- [Harman and Lacko (2010)]: Harman, Radoslav and Lacko, Vladim{\'\i}r "_On decompositional algorithms for uniform sampling from n-spheres and n-balls_" In Journal of Multivariate Analysis 101, (2010)


- [Voelker et al. (2017)]: Voelker, Aaron R and Gosmann, Jan and Stewart, Terrence C "_Efficiently sampling vectors and coordinates from the n-sphere and n-ball_" In Centre for Theoretical Neuroscience-Technical Report 1, (2017)


- _[Marsaglia polar method]_<br><small>_`https://en.wikipedia.org/wiki/Marsaglia_polar_method`_ </small>


- _[Volume of an n ball]_<br><small>_`https://en.wikipedia.org/wiki/Volume_of_an_n-ball`_ </small>


[Harman and Lacko (2010)]:    <https://www.sciencedirect.com/science/article/pii/S0047259X10001211>
    "Harman, Radoslav and Lacko, Vladim{\'\i}r \"On decompositional algorithms for uniform sampling from n-spheres and n-balls\" In Journal of Multivariate Analysis 101, (2010)"


[Voelker et al. (2017)]:    <https://compneuro.uwaterloo.ca/files/publications/voelker.2017.pdf>
    "Voelker, Aaron R and Gosmann, Jan and Stewart, Terrence C \"Efficiently sampling vectors and coordinates from the n-sphere and n-ball\" In Centre for Theoretical Neuroscience-Technical Report 1, (2017)"


[Marsaglia polar method]:    <https://en.wikipedia.org/wiki/Marsaglia_polar_method>
    "Marsaglia's polar method"


[Volume of an n ball]:    <https://en.wikipedia.org/wiki/Volume_of_an_n-ball>
    "Volume of an n ball"

</small>
</reference>
