---
date: 2024-01-01 00:00:00 +0000
layout: post
slug: 85a
status: done
title: N-Queens Problem
---

## N-Queens Problem
> The n-queens puzzle is the problem of placing `n` queens on an `n x n` chessboard such that no two queens attack each other. Given an integer `n`, return all distinct solutions to the n-queens puzzle. You may return the answer in any order.
>
> Each solution contains a distinct board configuration of the n-queens' placement, where 'Q' and '.' both indicate a queen and an empty space, respectively.

### Intuition

All indices of same diagonal share the same value for `(x-y)`. Similarly, all indices of anti diagonal share the same value for `(x+y)`.

**Backtracking**

```python
def n_queens(n: int) -> List[List[str]]:
    ans = []
    state = [["."] * n for _ in range(n)]
    m_row = defaultdict(int)
    m_col = defaultdict(int)
    m_diag = defaultdict(int)
    m_antidiag = defaultdict(int)

    def mark(x, y, V=1):
        m_row[x] += V
        m_col[y] += V
        m_diag[x - y] += V
        m_antidiag[x + y] += V

    def get_mark(x, y):
        return m_row[x] + m_col[y] + m_diag[x - y] + m_antidiag[x + y]


    def backtrack(row):
        if row == n:
            ans.append(["".join(c) for c in state])
            return

        for col in range(n):
            if get_mark(row, col) == 0:
                # keep queen
                mark(row, col, 1)
                state[row][col] = "Q"
                backtrack(row + 1)

                # remove queen
                state[row][col] = "."
                mark(row, col, -1)

    backtrack(0)
    return ans
```