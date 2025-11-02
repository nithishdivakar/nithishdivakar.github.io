---
date: 2024-01-01 00:00:00 +0000
layout: post
slug: 02h01
status: done
tags:
- string
title: Reorganize String
---

## Reorganize String [LC#767]
> Given a string `s`, rearrange the characters of s so that any two adjacent characters are not the same. Return any possible rearrangement of s or return "" if not possible.

### Intuition
- If the character with largest frequency appears more that `(n+1)//2` times, then such an arrangement is not possible.
- Simply arrange max frequent character in interleaved indexes and fill out other characters in the gaps. 


### Code
```python
def reorganize_string(self, s: str) -> str:
    character_counts = Counter(s)
    n = len(s)
    if max(character_counts.values()) > (n + 1) // 2:
        return ""

    def interleaved_index_generator(n):
        for i in range(0, n, 2):
            yield i
        for i in range(1, n, 2):
            yield i

    characters = list(s)
    characters.sort(
        key=lambda char: (character_counts[char], char), 
        # break tie when 2 chars have same counts
        reverse=True
    )
    output = characters.copy()
    interleaved_index = interleaved_index_generator(n)
    for character in characters:
        output[next(interleaved_index)] = character
    return "".join(output)
```

### Time complexity
- $T(n) = O(n \log n)$  $S(n) = O(n)$. Time complexity is $O(n)$ if we sort while exploiting the fact that there are only constant number of characters.