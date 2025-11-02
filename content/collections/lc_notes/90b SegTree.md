---
date: 2024-01-01 00:00:00 +0000
layout: post
slug: '90b'
status: done
title: Segment Trees
tags:
- segment trees
- rmq
---


### Segment Trees
- Segment Trees are a data structure where each node is responsible for a range of values.
- Can do point updates in $O(\log n)$ and range queries in $O(\log n)$. 
- Requires $2\cdot n+1$ storage.
- Implemented as a collection of complete binary tree. 

```text
┌───────────────────────────────────────────────────────────────┐
│                               1:                              │     
│                             -----                             │
╔═══════════════════════════════╗───────────────────────────────┤
║               2:              ║               3:              │     
║             [3,11)            ║             -----             │
╟───────────────┬───────────────╫───────────────╔═══════════════╗
║       4:      │       5:      ║       6:      ║       7:      ║
║     [3,7)     │     [7,11)    ║     -----     ║     [1,3)     ║
╟───────┬───────┼───────┬───────╠═══════╦═══════╣───────┬───────╢
║   8:  │   9:  │  10:  │  11:  ║  12:  ║  13:  ║  14:  │  15:  ║
║ [3,5) │ [5,7) │ [7,9) │ [9,11)║[11,13)║   0   ║   1   │   2   ║
╟───┬───┼───┬───┼───┬───┼───┬───╫───┬───╠═══╤═══╩═══╤═══╪═══╤═══╝
║16:│17:│18:│19:│20:│21:│22:│23:║24:│25:║   │   │   │   │   │   |
║ 3 │ 4 │ 5 │ 6 │ 7 │ 8 │ 9 │10 ║11 │12 ║   │   │   │   │   │   │
╚═══╧═══╧═══╧═══╧═══╧═══╧═══╧═══╩═══╧═══╝───┴───┴───┴───┴───┴───┘
┌─────────┐
│Tree idx:│
│  range  │
└─────────┘
```
References
- <https://codeforces.com/blog/entry/18051>
- <https://www.youtube.com/watch?v=xztU7lmDLv8>

```python
OP = lambda a, b: min(a, b)
E = lambda : math.inf

class SegTree:
    def __init__(self, A: List[int]) -> None:
        n = len(A)
        self.T: List[int] = [E()] * (2 * n)
        for i in range(n):
            self.T[n + i] = A[i]

        for i in range(n - 1, 0, -1):
            self.T[i] = OP(self.T[2 * i] , self.T[2 * i + 1])

        self.n: int = n

    def __getitem__(self, i: int) -> int:
        return self.T[self.n + i]
    
    def point_update(self, i: int, value: int) -> None:
        i += self.n
        self.T[i] = value
        while i > 1:
            i //= 2
            self.T[i] = OP(self.T[2 * i] , self.T[2 * i + 1])

    def range_query(self, l: int, r: int) -> int: # [l, r)
        res_l, res_r = E(), E()
        l += self.n
        r += self.n

        while l < r:
            if l % 2 == 1:
                res_l = OP(res_l, self.T[l])
                l += 1
            if r % 2 == 1:
                r -= 1
                res_r = OP(self.T[r], res_r)
            l //= 2
            r //= 2
        return OP(res_l, res_r)
```
