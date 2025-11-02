---
date: 2024-01-01 00:00:00 +0000
slug: '03a'
layout: post
status: doing
title: Implementing Self Attention
tags: [self attention, transformers]
---

## Implementing Self Attention
b is batch, t is tokens and d is token embedding size.

```python
def scaled_dot_attention(
    Q: Tensor[b, t, d],
    K: Tensor[b, t, d],
    V: Tensor[b, t, d]
) -> Tensor[b, t, d]:
    dot: Tensor[b, t, t] = torch.einsum('b i d , b j d -> b i j', Q, K) * sqrt(d)
    attention: Tensor[b, t, t] = torch.softmax(dot, dim=-1)
    out: Tensor[b, t, d] = torch.einsum('t i j , t j d -> t i d', attention, V)
    return out

def self_attention(X: Tensor[b, t, c]) -> Tensor[b, t, d]:
    Wq, Wk, Wv = ... # define weight matrices
    Q: Tensor[b, t, d] = torch.einsum('b i c, c d -> b i d', X, Wq)
    K: Tensor[b, t, d] = torch.einsum('b i c, c d -> b i d', X, Wk)
    V: Tensor[b, t, d] = torch.einsum('b i c, c d -> b i d', X, Wv)
    return scaled_dot_attention(Q, K, V)
```