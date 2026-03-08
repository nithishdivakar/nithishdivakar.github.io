---
title: About
date: 1991-10-13
publishdate: 1991-10-13
type: page
---

# DAXPY

> **D**ouble-precision **A**·**X** **P**lus **Y** is a subroutine from the LINPACK package, and a cornerstone of high-performance numerical computing.

The operation is deceptively simple:

$$Y \gets A \cdot X + Y$$

where $A$ is a scalar and $X$, $Y$ are vectors. Yet this single routine underlies nearly all of computational linear algebra; matrix factorisation, iterative solvers, least-squares problems. Its elegance lies not in complexity, but in composition: a primitive so well-optimised that everything built on top of it inherits that efficiency.

This site is organised around the same principle. Each piece of writing is meant to be small, focused, and self-contained. A building block rather than a monolith. Read one and understand one thing well. Read several and find that harder problems become tractable.

*The name is also a reminder that the most enduring ideas in computing are often the oldest ones.*

*See: DAXPY routine in [original specification](https://ntrs.nasa.gov/citations/19780018835) for [BLAS](https://en.wikipedia.org/wiki/Basic_Linear_Algebra_Subprograms).*

-- [Nithish Divakar](https://www.linkedin.com/in/ndivakar/)
