---
date: 2024-01-01 00:00:00 +0000
layout: post
level: h2
slug: 20b
status: done
title: Longest Increasing Subsequence
---

## Longest Increasing Subsequence [LC#300]
> Given an integer array nums, return the length of the longest strictly increasing subsequence.


### Dynamic programming approach
- Find the length of longest increasing subsequence ending at i. 
    ```python
    def length_of_lis(nums: List[int]) -> int:
        if not nums: return 0
        max_length = [1] * len(nums)
        for i in range(1, len(nums)):
            for j in range(i):
                if nums[i] > nums[j]:
                    max_length[i] = max(max_length[i], max_length[j] + 1)
        return max(max_length)
    ```
- $T(n) + O(n^2)$; $S(n) = O(n)$

### Technique based on [patience sorting](https://www.cs.princeton.edu/courses/archive/spring13/cos423/lectures/LongestIncreasingSubsequence.pdf)
- If the number is larger than the largest element in the temporary array, append it. Otherwise, replace the found position with the current number.
- The length of the temporary array will give the length of the longest increasing subsequence.
- The temp array may not always have a valid subsequence, but its length will always be equal to longest subsequence.
    ```python
    from bisect import bisect_left
    
    def length_of_lis(nums: List[int]) -> int:
        if not nums: return 0
        tails = []
        for num in nums:
            pos = bisect_left(tails, num)
            if pos == len(tails):
                tails.append(num)
            else:
                tails[pos] = num
        return len(tails)
    ```
- $T(n) = O(n \log n)$; $S(n) = O(n)$