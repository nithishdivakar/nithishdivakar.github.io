---
date: 2024-01-01 00:00:00 +0000
layout: post
slug: 27a
status: done
title: Longest Substring Without Repeating Characters
tags:
- two pointers
- sliding window
---

## Longest Substring Without Repeating Characters [LC#3]
> Given a string `s`, find the length of the longest substring without repeating characters.


**Sliding Window and 2 pointers**
- Start with `left` and `right` at 0.
- Expand: Move `right` to add characters and update counts until a repeat is found.
- Shrink: Move `left` to remove characters until all are unique.
- Track maximum length of the window.
- $T(n) = O(n)$; $S(n) = O(|char set|)$
    ```python
    def max_substring_without_repetition(s: str) -> int:
        char_count = defaultdict(int)
        left = 0
        ans = 0
        for right in range(len(s)):
            current_char = s[right]
            char_count[current_char] += 1 
            while char_count[current_char]>1:
                char_count[s[left]] -= 1 
                left += 1
            ans = max(ans, right-left+1)
        return ans
    ```
**Optimised Sliding window**
- Same as previous approach, but keep track last occurance of all characters seen so far.
- Jump to the next after last occurence whenever a character is encountered again.
- $T(n) = O(n)$; $S(n) = O(|char set|)$
    ```python
    def max_substring_without_repetition(s: str) -> int:
        last_found_at = {}
        left = 0
        ans = 0
        for right in range(len(s)):
            current_char = s[right]
            if current_char in last_found_at:
                left = max(left, last_found_at[current_char]+1)
            last_found_at[current_char] = right
            ans = max(ans, right - left +1)
        return ans
    ```