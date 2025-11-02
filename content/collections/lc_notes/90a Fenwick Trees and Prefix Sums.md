---
date: 2024-01-01 00:00:00 +0000
layout: post
slug: '90a'
status: done
title: Fenwick Trees and Prefix Sums
tags:
- fenwick trees
- prefix sum
- rmq
---

### Fenwick Trees or Binary Indexed Tree
- Each index in the fenwick tree is responsible for a rnage of values in the original array. 
- Requires $O(n)$ storage.
- Can calculate prefix sums in $O(\log n)$ time.
- Point updates can also be performed in $O(\log n)$
- Can only do operations which are invertible. 

References
- <https://cp-algorithms.com/data_structures/fenwick.html>
- <https://www.youtube.com/watch?v=uSFzHCZ4E-8>
- <https://blog.kartynnik.info/posts/fenwick-trees-are-nothing-but>

```text
          0· 1· 2· 3· 4· 5· 6· 7· 8· 9·10·11·12·13·14·15
    A = [  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  ]

T[ 0] = [ ✚|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  ]
T[ 1] = [ ✚| ✚|  |  |  |  |  |  |  |  |  |  |  |  |  |  ]
T[ 2] = [  |  | ✚|  |  |  |  |  |  |  |  |  |  |  |  |  ]
T[ 3] = [ ✚| ✚| ✚| ✚|  |  |  |  |  |  |  |  |  |  |  |  ]
T[ 4] = [  |  |  |  | ✚|  |  |  |  |  |  |  |  |  |  |  ]
T[ 5] = [  |  |  |  | ✚| ✚|  |  |  |  |  |  |  |  |  |  ]
T[ 6] = [  |  |  |  |  |  | ✚|  |  |  |  |  |  |  |  |  ]
T[ 7] = [ ✚| ✚| ✚| ✚| ✚| ✚| ✚| ✚|  |  |  |  |  |  |  |  ]
T[ 8] = [  |  |  |  |  |  |  |  | ✚|  |  |  |  |  |  |  ]
T[ 9] = [  |  |  |  |  |  |  |  | ✚| ✚|  |  |  |  |  |  ]
T[10] = [  |  |  |  |  |  |  |  |  |  | ✚|  |  |  |  |  ]
T[11] = [  |  |  |  |  |  |  |  | ✚| ✚| ✚| ✚|  |  |  |  ]
T[12] = [  |  |  |  |  |  |  |  |  |  |  |  | ✚|  |  |  ]
T[13] = [  |  |  |  |  |  |  |  |  |  |  |  | ✚| ✚|  |  ]
T[14] = [  |  |  |  |  |  |  |  |  |  |  |  |  |  | ✚|  ]
T[15] = [ ✚| ✚| ✚| ✚| ✚| ✚| ✚| ✚| ✚| ✚| ✚| ✚| ✚| ✚| ✚| ✚]

```

```python
OP = lambda a, b: a+b
OP_INV = lambda a, b: a - b
E = lambda : 0

class FenwickTree:
    def __init__(self, A: List[int]):
        n = len(A)
        self.T = A.copy()
        for i in range(n):
            parent = i | (i + 1)
            if parent < n:
                self.T[parent] += self.T[i]

    def add(self, i, delta):
        n = len(self.T)
        while i < n:
            self.T[i] = OP(self.T[i], delta)
            i = i | (i + 1)

    def prefix_sum(self, i): # sum [0, i]
        res = E()
        while i >= 0:
            res = OP(result, self.T[i])
            i = (i & (i + 1)) - 1
        return result

    def range_sum(self, l, r):  # sum [l, r)
        return OP_INV(self.prefix_sum(r - 1) ,  self.prefix_sum(l - 1))

    def __getitem__(self, idx: int) -> int:
        return self.sum_range(idx, idx)

    def append(self, val):
        n = len(self.T)
        self.T.append(E())
        self.add(n, val)

```
