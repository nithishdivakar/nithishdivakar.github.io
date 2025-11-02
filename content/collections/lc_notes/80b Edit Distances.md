---
date: 2024-01-01 00:00:00 +0000
layout: post
slug: 80b
status: done
tags:
- string
- dp
title: Edit Distances
---

## Edit Distance [LC#72]
> Given two strings word1 and word2, return the minimum number of operations required to convert word1 to word2. You have the following three operations permitted on a word:
> - Insert a character
> - Delete a character
> - Replace a character

### Intuition
Let `cost[i][j]` is the minimum edit distance (or the minimum number of operations) required to transform the first `i` characters of word1 into the first `j` characters of word2.

**Dynamic Programming** 
```python
def edit_distance(word1: str, word2: str) -> int:
    # Define the costs for operations
    costs = {'insert': 1, 'delete': 1, 'substitute': 1}
    m, n = len(word1), len(word2)
    
    cost = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Initialize the first row and column
    for i in range(m + 1):
        # Cost of deleting all characters from word1 to form word2
        cost[i][0] = i  * costs['delete']
    for j in range(n + 1):
        # Cost of inserting all characters to word1 to form word2
        cost[0][j] = j  * costs['insert']

    # Fill the cost matrix
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                cost[i][j] = cost[i - 1][j - 1]  # No operation needed
            else:
                cost[i][j] = min(
                    cost[i - 1][j] + costs['insert'],      # Insert
                    cost[i][j - 1] + costs['delete'],      # Delete
                    cost[i - 1][j - 1] + costs['substitute']  # Substitute
                )
    return cost[m][n]
```
- $T(n) = O(mn)$
- $S(n) = O(mn)$ but can be optimised to $O(\min(m,n))$