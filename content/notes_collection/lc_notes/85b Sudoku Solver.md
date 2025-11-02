---
date: 2024-01-01 00:00:00 +0000
layout: post
slug: 85b
status: done
title: Sudoku Solver
---

## Sudoku Solver [LC#37]
> Write a program to solve a Sudoku puzzle by filling the empty cells. A sudoku solution must satisfy all of the following rules:
> 1. Each of the digits 1-9 must occur exactly once in each row.
> 2. Each of the digits 1-9 must occur exactly once in each column.
> 3. Each of the digits 1-9 must occur exactly once in each of the 9 3x3 sub-boxes of the grid.
> The '.' character indicates empty cells.

### Intuition
Backtracking

### Code
```python
def solve_sudoku(board: List[List[str]]) -> None:
    positions = []
    for i in range(9):
        for j in range(9):
            if board[i][j] == ".":
                positions.append((i, j))

    def get_possible_numbers(x, y):
        possible_numbers = set(["1", "2", "3", "4", "5", "6", "7", "8", "9"])
        cross = set()
        for i in range(9):
            cross.add(board[x][i])
            cross.add(board[i][y])

        for i in range((x // 3) * 3, (x // 3 + 1) * 3):
            for j in range((y // 3) * 3, (y // 3 + 1) * 3):
                cross.add(board[i][j])

        return possible_numbers.difference(cross)

    def backtrack(i):
        if i >= len(positions):
            return True

        x, y = positions[i]
        possible_numbers = get_possible_numbers(x, y)

        if not possible_numbers:
            return False

        for num in possible_numbers:
            board[x][y] = num
            if backtrack(i + 1):
                return True

        board[x][y] = "."
        return False

    backtrack(0)
```