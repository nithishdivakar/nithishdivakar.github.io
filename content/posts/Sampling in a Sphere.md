---
title: Sampling in a Sphere
tags : [statistics]
date: 2024-03-10T09:36:53+05:30
start_date: 2024-03-10T09:36:53+05:30
draft: true
---

# Sampling in a Sphere

Generating random points which follows some distribution is one of those fundamental operations which underlky a lot of computations. But when we add constraints to the region where we are to generate these random points, things get interesting. These are generally studied under "Sampling on a Manifold" but in this post we look at sampling on the simplest manifold ... The sphere. 

Let begin with the end. The following algorithm can generate uniformly distributed points inside an n-dimensional unit sphere. 

$$u_1, \ldots, u_{n+2} \sim N(0,1)$$
$$x_1, \ldots, x_n = \frac{(u_1,\ldots, u_n)}{\sqrt{u_1^2+\ldots+u_{n+2}^{2}}}$$

There is a lot to unpack here. For example:
- Why are we sampling from a normal distribution if our end goal is to get a uniform distribution?
- Why are we simply dropping 2 dimension?

## What is inside a Sphere?
A sphere is defined as a set of points which are equidistant from a locus known as center. A unit sphere with origin as center can be defined as
$$ S^n = \\{x \in \mathbb{R}^{n} ~:~ \\\|x\\\|_2 = 1\\}$$

_In 2 dimensions, this definition is only include the circumference of the circle._

A n-dimensional ball however is the whole region inside the sphere. 
$$ B^n = \\{x \in \mathbb{R}^{n} ~:~ \\|x\\|_2 \leq 1 \\}$$
Note that the $B^n$ that we defined here is a closed ball so $S^n \subset B^n$.

Some facts about the n dimensional unit ball and sphere
- Both are completely inscribed in the region $[-1,1]^n$
- $$\operatorname{Vol}(B^n)  = \frac{\pi^{n/2}}{\Gamma(\frac{n}{2}+1)}$$
  
## When Spheres are Circles
In 2 dimensions, there is an easy technique to get uniformly distributed points within a circle by simply doing rejection sampling. Generate unifom random samples inside $[-1,1]^2$ and reject the samples which are outside the circle. 

```python
while True:
  x ~ U[-1,1]
  y ~ U[-1,1]
  if x^2+ y^2 <= 1:
    return (x,y)
```
However, efficiency of rejection sampling is depended on how much samples are rejected; which is ratio of area of the circle to the area of the $2 \times 2$ square. 
$$\frac{\pi 1^2}{4} \approx 78.5\\\%$$

We could do the same thing for higher dimensions but the efficiency is less. The fraction of sampel rejection sampling would accept is 

$$\frac{\operatorname{vol}(B^n)}{2^{n}}$$

In 3 dimensions the efficiency drops to $\approx 52.33\\%$ and by the time we get to 10 dimensions, its $ \frac{\pi^5/5!}{2^{10}} \approx 0.249\\% $. i.e we end up rejecting $99.7\\%$ of the points that are generated and it gets worse as we move to higher dimensions. 


## On the circumference
If we restrict ourselves to get uniform random point on the circuference of the circle, there is an easier techqnique by [Muller, Marsagliai]. Let talk about 2 dimensional case first. The technique is 

$$u,v \sim N(0,1)$$
$$x,y = \frac{u,v}{\sqrt{u^2+v^2}}$$

It seems a bit strange why this would generate random uniform points on the circle's circumference. Especially since we begin sampling from a normal distrbution. But the proof is simple. Let take a look at the join distribution of $(u,v)$. Since both are normally distributed and independent of each other, we have

$$f(u,v)  = \left(\frac{1}{\sqrt{2\pi}} e^{-\frac{1}{2}u^2}\right) \left(\frac{1}{\sqrt{2\pi}} e^{-\frac{1}{2}v^2}\right)$$
$$= \frac{1}{2\pi} e^{\frac{1}{2} (u^2+v^2)}$$

From this, we can conclude that the distrobution of $(u,v)$ only depends on its distance from origin ($u^2+v^2$). i.e. only dependent on magnitude and  invariant to direction. The last step in the algorithm where we normalise both point by this distance projects all (u,v)'s to the circle'c circumference without any change in the direction. Hence, we can conclude that these points are uniformly distributed on the circle. 

The same proof easily extends to n-dimensions as well

$$f(u_1,\ldots, u_n)  = \prod_i \left(\frac{1}{\sqrt{2\pi}} e^{-\frac{1}{2}u_i^2}\right) = \frac{1}{(2\pi)^{n/2}} e^{\frac{1}{2}\\|u\\|^2_2} $$

and so does the technique. Generating random uniform points on n-sphere is
$$u_i \sim N(0,1) $$
$$ x = \frac{u}{\\|u\\|^2_2} $$

But what about inside the circle?

## 



----
So what is happening here? Why are we sampling from a normal distribution to end up with a uniform distribution on a n-sphere? and why are we seemingly just dropping the last 2 dimensions?

To understand what is happening here, its a sweet story with a few twists and turns. It starts with a simple question.

**How do you generate uniform random points in a circle?** 

In 2 dimensions where spheres are circles, we can intuitively think like this.

Since a circle is defined by its boundary, $x^2+y^2 = 1^2$, We can generate $x$ first and $x \sim U[-1,1]$. Then to ensure the point falls in circle, we have to generate $y$ as $y \sim U[-\gamma(x), \gamma(x)]$ with $\gamma(x)=\sqrt{1 - x^2}$. Its easy to see this doesn't generate uniform points on the circle. A simple exlpanation is that y is not independent of x and a circle is uniform in all directions. 

In polar coordinates, things are a bit independent. The circle is only $r \leq 1$. (Did I mention we are only talking about unit circles in this article?). There is no $\theta$ in there bacause circle in all directions. So sampling can be $r \sim U[0,1]$ and $\theta \sim U[0,2\pi]$. However, this technique too is flawed. The area between $r \in [0.2,0.3]$ and $r \in [0.5,0.7]$ is different, but this technique generates same number of points in both.

So what do we do?

# Arxive

## Rejection Sampling
Rejection sampling is easy to describe and even easier to implement. Uniformly sample inside square $[-1,-1]^2$; check if the point is inside the unit circle; reject otherwise.

```python
while True:
  x ~ U[-1,1]
  y ~ U[-1,1]
  if x^2+ y^2 < 1:
    return (x,y)
```
This is a valid technique. It does generate uniform samples inside the circle. Its so right that the ratio of acceptance is used to approximate $\pi$. Acceptance rate is ratio area of the circle and the square. Which is about $\frac{\pi}{4} \approx 78.5\\\%$
In 3 dimensions it is $\frac{\frac{4}{3}\pi}{8} \approx 52.33\\%$


$$\left.\frac{\pi^{n/2}}{\Gamma(\frac{n}{2}+1)} \middle/ 2^n\right.$$

pi^5/5! / 1024

This technique seems like one we can easily extend to higher dimensions. But the one hamartia of this method is its efficiency. Acceptance rate is equal to ratio of area of circle and enclosing square. And when circles are spheres and squares are hypercubes, the techniques isn't very efficient. [TODO Give exzmple]


So lets look at a few analytical techniques. But we do have to take a detour. Not very far though. We have to first look at how to generate random uniform point ON the circle. 

## Volume of a n-ball
A ball is a region of space comprising of all points within fixed distance, called radius from a fixed point. Unit $n-$ball is $B^n$. We talk about closed ball here. i.e $S^n \in B^n$

Unit n-sphere $$ S^n = \\\{x\in \mathbb{R}^{n+1}: \\\|x\\\| =1\\\} $$
## Generating random Uniformly distributed points ON the circle
... or its circumference.

Polar (Maybe skip this)
$$\theta \sim U[0,2\pi]$$
$$x = \sin(\theta)$$
$$y = \cos(\theta)$$


