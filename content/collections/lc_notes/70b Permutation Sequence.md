---
date: 2024-01-01 00:00:00 +0000
slug: '70b'
layout: post
status: done
title: Permutation Sequence
tags: [permutation]
---

## Permutation Sequence [LC#60]
> The set `[1, 2, 3, ..., n]` contains a total of `n!` unique permutations. Given `n` and `k`, return the `kth` permutation sequence.

### Intuition
- Let $F$ be the factorial number system representation of the number $k$ for the base $n$. Indexing of $k$ starts from $0$.
- For each digit $f$ in $F$, select the $f^{th}$ digit from the set of numbers and add it to the answer. After selecting, remove that digit from set.
- Example:
    - For $n=6$, $2982 = 4:0:4:1:0:0:0_!$ so the permutation is $(4,0,6,2,1,3,5)$
- Reference
    - [Factorial Number System](https://en.wikipedia.org/wiki/Factorial_number_system)

### Code
```python
def kth_permutation(n: int, k: int) -> str:
    factorials = [1]
    digits = ["1"]
    for i in range(1, n):
        factorials.append(factorials[-1] * i)
        digits.append(str(i + 1))

    output = []
    k -= 1
    for i in range(n - 1, -1, -1):
        # index = k // factorials[i]
        # k = k - idx * factorials[i]
        index, k = divmod(k, factorials[i])
        output.append(digits[index])
        del digits[index]
    return "".join(output)
```

### Time complexity
- $T(n) = O(n)$ 
- $S(n) = O(n)$
