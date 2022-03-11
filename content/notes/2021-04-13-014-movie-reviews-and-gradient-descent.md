---
title : Movie Reviews and Gradient Descent
tags : [applied-ml]
date: 2021-04-13T05:04:51+05:30
draft: false
---

# Movie Reviews and Gradient Descent

The problem is simple; $m$ movies, $n$ users and we have the data of rating of movies by users. Now in reality, each user might have rated a few movies while total number of users and movies are huge. We can consider the whole ratings data as a matrix $n\times m$ matrix $R$ where $R_{ij}$ is the rating of $i^{th}$ movie by $j^{th}$ user.

We want a model which can predict the rating a user would have given a movie. Now the modelling part is easy as a matrix factorisation problem. We can assume every user is represented by a embedding $u_i$ and similarly, every movie has a embedding $m_j$. We simply want $$R_{ij}  \sim { u_i}^\intercal m_j$$ If we simply model the learning problem as
$$\mathop{\mathrm{arg\,min}}_{U,M} \\| {U}^\intercal M - R \\|_2$$
then we are implicitly assuming that all unavailable ratings are $0$. Since we have only a few ratings compared to all possible combinations of movies and users, the model will get biased towards $0$ ratings.
 
## Good Modelling

What we need to do instead is to simply model what the data is available us and nothing else. Essentially,
$$\mathop{\mathrm{arg\,min}}\_{u_i,m_j}  \sum_{(u_i,m_j,r_{ij})\in D} \left({u_i}^\intercal m_j - r_{ij}\right)^2$$

## Gradient Descent and Training

The updates for U and M according to gradient descent are
$$\begin{aligned}
u_i &\gets u_i -  2\alpha ({u_i}^\intercal m_j  - r_{ij})m_j
\\\\
m_j &\gets m_j - 2\alpha ({u_i}^\intercal m_j  - r_{ij})u_i\end{aligned}$$

To convert this to a batched gradient descent, we simply have to take a batch of ratings and work on updating only the concerned rows of $U$ and $M$. But we have to handle the case where **user id or movie id is repeated in our batch**. The gradient have to be averaged in such case. 

Let first look at a naive (slow but correct) code to do that. 

```python
def batch_update_slow(mb,ub,rb):
    # 45it/s
    residuals = np.einsum('ij, ij->i',U[ub,:],M[mb,:]) - rb

    U_updates = alpha * 2 * np.einsum('i,ij->ij',residuals, M[mb,:])
    M_updates = alpha * 2 * np.einsum('i,ij->ij',residuals, U[ub,:])
    
    for k in np.unique(ub):
        idxs = np.nonzero(ub==k)[0]
        U[k,:] = U[k,:] - U_updates[idxs].mean(axis=0)
    
    for k in np.unique(mb):
        idxs = np.nonzero(mb==k)[0]
        M[k,:] = M[k,:] - M_updates[idxs].mean(axis=0)
	return
```

Vectorising the for loops in the above code requires calculation of all gradients and then scaling it using frequency of each indices. The scaled gradients of each indices can them simply be added together to effectively get average gradient from each repeated indices. The vectorised version is significantly faster.

``` python
def batch_update(mb,ub,rb):
    # 800it/s
    
    # U <- U - 2a(U^TM-rb)M
    # M <- M - 2a(U^TM-rb)U
    
    residuals = np.einsum('ij, ij->i',U[ub,:],M[mb,:]) - rb


    ## Update U
    # U[ub,:] = U[ub,:] - alpha * 2 * residue * M[mb,:]
    
    # get unique user_ids, reverse mappings, and counts of each user_ids
    idxs, ixds, cnt = np.unique(ub,return_inverse=True, return_counts=True)
    
    # get frequency of each indices
    frequency = (1.0/cnt)[ixds]
    
    # compute full gradient, then scale each gradient by frequency 
    
    # gradient        = np.einsum('ij,i->ij',M[mb,:],residuals)
    # scaled_gradient = np.einsum('ij,i->ij',gradient,frequency)
    scaled_gradient   = np.einsum('ij,i,i->ij', M[mb,:], residuals, frequency)
    
    # Sum scaled gradient for unique user ids together
    
    F = lambda w: np.bincount(ixds, weights = w)
    aggregated_gradient = np.apply_along_axis(F, 0, scaled_gradient)
    
    # update U with the gradients
    U[idxs,:] = U[idxs,:] - alpha * 2 * aggregated_gradient
    
    
    ## Update M 
	# (similar steps as U)
    # M[mb,:] = M[mb,:] - alpha * 2 * residue * U[ub,:]

    idxs,ixds, cnt = np.unique(mb,return_inverse=True, return_counts=True)
    frequency = (1.0/cnt)[ixds]
    
    # gradient        = np.einsum('ij,i->ij',M[mb,:],residuals)
    # scaled_gradient = np.einsum('ij,i->ij',gradient,frequency)
    scaled_gradient   = np.einsum('ij,i,i->ij', U[ub,:], residuals, frequency)
    
    F = lambda w: np.bincount(ixds, weights = w)
    aggregated_gradient = np.apply_along_axis(F, 0, scaled_gradient)
    
    M[idxs,:] = M[idxs,:] - alpha * 2 * aggregated_gradient
	return
```

The fast version of the update step looks a bit unreadable, but its **16x** faster `:)`  