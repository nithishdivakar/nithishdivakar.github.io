---
date: 2024-01-01 00:00:00 +0000
layout: post
slug: 70a
status: done
title: Next Permutation
tags: [permutation]
---


## Next Permutation [LC#31]
> Given an array of integers nums, find the next permutation of nums.
>
> The next permutation of an array of integers is the next lexicographically greater permutation of its integer. More formally, if all the permutations of the array are sorted in one container according to their lexicographical order, then the next permutation of that array is the permutation that follows it in the sorted container. If such arrangement is not possible, the array must be rearranged as the lowest possible order (i.e., sorted in ascending order).

### Intuition
- [Step 1] Find the largest `i` such that `nums[i] < nums[i+1]`. If no such index exists, then this is the last sequence in the permutation. Reset array to sorted order (first element in the sequence).
- [Step 2] Find the largest index `j > i` such that `nums[i] < nums[j]`. Swap these 2 numbers
- [Step 3] Reverse the array from `i+1` till the end.

### Code
```python
    def next_permutation(self, nums: List[int]) -> List[int]:
        def swap(i, j):
            nums[i], nums[j] = nums[j], nums[i]

        def reverse(start, end):
            nums[start : end + 1] = nums[start : end + 1 : -1]

        n = len(nums)
        # Step 1
        i = n - 2
        while i >= 0 and nums[i] >= nums[i + 1]:
            i -= 1
            
        if i >= 0:
            # Step 2
            j = n - 1
            while nums[i] >= nums[j]:
                j -= 1
            swap(i, j)
        
        # Step 3
        reverse(i + 1, n - 1)
        return nums
```
### Time complexity
- $T(n) = O(n)$
- $S(n) = O(1)$