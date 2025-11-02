---
date: 2024-01-01 00:00:00 +0000
layout: post
slug: 27b
status: done
tags:
- two pointers
- sliding window
title: String Compression
---

## String Compression [LC#443]
> Given an array of characters chars, compress it using the following algorithm:
> Begin with an empty string s. For each group of consecutive repeating characters in chars:
> - If the group's length is 1, append the character to s.
> - Otherwise, append the character followed by the group's length.
>
> The compressed string s should not be returned separately, but instead, be stored in the input character array chars. Note that group lengths that are 10 or longer will be split into multiple characters in chars. After you are done modifying the input array, return the new length of the array.

### Intuition
- Two Pointers and sliding window

### Code
```python
def string_compress(chars: List[str]) -> int:
    left = 0
    pos = 0
    chars.append(" ") # to proccess last group
    for right in range(len(chars)):
        if chars[right] != chars[left]:
            length = right - left
            if length == 1:
                string = chars[left]
            else:
                string = f"{chars[left]}{length}"
            for c in string:
                chars[pos] = c
                pos += 1
            left = right
    return pos
```
### Time complexity
- $T(n) = O(n)$
- $S(n) = O(1)$