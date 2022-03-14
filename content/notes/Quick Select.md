---
title: Quick Select
layout: post
tags : [algorithms]
date: 2022-03-14T08:30:00+05:30
draft: false
---
# Quick Select

The core technique in quick sort is partition procedure. The partition procedure partitions the array into 2 segments such that for a choosen pivot element, one segment has all element smaller or equal and the other has all element larger than pivot. 

The procedure itself has applications beyond quick sort like selecting the smallest $k$ elements if sorted order is not required. 

There are 2 main techniques to implement quick select. 

## Hoare's Method
Any element can be given as pivot. If we give an element which is not present in the array, the returned index would have the smallest element larger than pivot in the array. 

```python
def hoare_partition(A, low, high, pivot):
	left, right = low-1, high+1
	while True:
		while True:
			left += 1
			if A[left] >= pivot: break
		while True:
			right -= 1
			if A[right] <= pivot: break
		if left >= right:
			return right

		swap(A[left], A[right])
```


## Lomuto's Method
The procedure always select the last element in the array as pivot. For choosing any other element in the array as pivot, a preprocessing step which swaps the last element with the choosen pivot is needed. 

```python
def lomuto_partition(A, low, high):
	pivot = A[high]
	p = low - 1
	for j in range(low,  high): 
	    if A[j] <= pivot :
		      p = p + 1
		      swap(A[p], A[j]) 
	p = p + 1
	swap(A[p], A[high])
	return p 
```




## Finding $k$ smallest element in array
Also known as quick select, the procedure partially sorts the array.  

```python
def quick_select(A, k):
	low, high = 0, len(A)-1

	while True:
		pivot = random_index(low, high)
		index = partition(A, low, high, A[pivot])
		if index == k:
			return A[:k]
		if index < k:
			left = index + 1
		else:
			right = index - 1
```
Like quick sort, quick select has average linear time complexity, but  quadratic time complexity in worst case. 
