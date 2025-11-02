---
date: 2024-01-01 00:00:00 +0000
slug: '99'
layout: post
status: doing
title: KMP
tags: []
---

## KMP [LC#xxx]
> Question Description


REF: https://www.youtube.com/watch?v=EL4ZbRF587g

### Intuition

### Code
```python
class KMP:
    def __init__(self, pattern):
        # longest prefix suffix (LPS) array
        m = len(pattern)
        lps = [0]*m
        length = 0
        i = 1
        while i < m:
            if pattern[length] == pattern[i]:
                length += 1
                lps[i] = length
                i += 1
            else:
                if length != 0:
                    length = lps[length - 1] 
                else:
                    lps[i] = 0
                    i += 1

        self.lps = lps
        self.pattern = pattern
        
    def match(self, text):
        n = len(text)
        m = len(self.pattern)
        matches = []
        i = j = 0
        while i < n:
            if self.pattern[j] == text[i]:
                i += 1
                j += 1
            if j == m:
                matches.append(i - j)
                j = self.lps[j - 1]
            elif i < len(text) and self.pattern[j] != text[i]:
                if j != 0:
                    j = self.lps[j - 1]
                else:
                    i += 1
        return matches
```

### Time complexity
- $T(n) = $ 
- $S(n) = $
