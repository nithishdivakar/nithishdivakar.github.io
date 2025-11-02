---
date: 2024-01-01 00:00:00 +0000
layout: post
slug: 65a
status: done
tags:
- trie
- dp
title: Word break
---

## Word break [LC#139]
> Given a string and a vocabulary, return true if the string can be segmented into a space-separated sequence of one or more words from the vocabulary. Note that the same word in the vocabulary may be reused multiple times in the segmentation.

### Intuition
- Use a Trie for efficient prefix searching.
- Use a boolean array `reachable` to track if substrings can be segmented.
- From each reachable index, use the trie search to find more reachable index
- Return `reachable[n]` to determine if the entire string can be segmented.

### Code
```python
def word_break(string: str, vocabulary: List[str]) -> bool:
    n = len(string)
    TRIE = {}
    EOW = "$"
    for word in vocabulary:
        if len(word) > n:
            continue
        node = TRIE
        for char in word:
            if char not in node:
                node[char] = {}
            node = node[char]
        node[EOW] = ""

    reachable = [False] * (n + 1)
    reachable[0] = True

    for i in range(n + 1):
        if reachable[i]:
            node = TRIE
            j = i
            while j < n:
                if string[j] not in node:
                    break
                node = node[string[j]]
                if EOW in node:
                    reachable[j + 1] = True
                j += 1

    return reachable[n]
```

### Time complexity
`n = len(string), m = len(vocabulary), k = max(len(word) in vocabulary)`
- $T(n) = O(mk) + O(nk)$  trie construction and search
- $S(n) = O(mk) + O(n)$ trie and reachable