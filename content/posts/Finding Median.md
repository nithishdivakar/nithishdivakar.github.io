---
title: Finding Median
tags : [algorithms]
date: 2022-03-01T06:59:51+05:30
draft: false
---

# Finding Median
*Here is my [ELI5](https://www.dictionary.com/e/slang/eli5/) definition of a median.*

> "Median is the middle number when numbers are sorted". 

There is only a single middle number when the size list is odd. But if the size is even, there are 2 middle numbers. Then we take an average of those 2 numbers to be the median.

Median is useful when your data doesn't behave. Medians are part of "robust statistics" because they are not affected by outliers. Both $[1,2,100]$ and $[1,2,3]$  have 2 as their median while their means differ widely. You can see why medians are not affected by noise.


This post is all about computing medians from a list of numbers. The straightforward approach is to sort everything first and the middle element is the median. But can we do better?


## Quick Select
Quick select is similar to quicksort except that it doesn't sort the array. It semi sorts the array.

Given an element 'pivot', quick select partitions the array such all the smaller elements are moved to the left of the pivot and all the larger elements are moved to the right; essentially partition the array into two.  The partition procedure can be implemented using either [Lomuto](https://en.wikipedia.org/wiki/Quicksort#Lomuto_partition_scheme) or [Hoare](https://en.wikipedia.org/wiki/Quicksort#Hoare_partition_scheme) scheme, either run in linear time. 

Quick select takes a number $k$ as a parameter and finds the $k^{th}$ smallest number in the array. As a side effect, the first $k$ locations of the array contains the $k$ smallest elements after the procedure.  

For finding the median, we can use quick selection by setting $k$ to the middle location. 

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

size = len(A) + 1
m1 = quick_select(A, size//2)
m2 = quick_select(A, size - size//2)
median = (m1+m2)/2.0
```

The best-case and average-case complexity for quick select is both $O(n)$ but in the worst case, it takes $O(n^2)$ time. The worst case occurs when all the pivots we select results in an *unfavourable* partition of the array. 

Is there any way to guarantee that the pivot we select results in a *favourable* split?

## Median of Medians
The algorithm is easier to describe. Split the large list into smaller lists. Find medians of the smaller lists(recursively) and then find the median of those medians. Use this number as the pivot in the partition function of quick select.

```python
def median_small(A):
	size = len(A) + 1
	B = sorted(A)
	m1 = B[size//2]
	m2 = B[size - size//2]
	return (m1+m2)/2.0

def median_of_medians(A, d = 5):
	n = len(A)
	if n <= d:
		return median_small(A)

	medians = [median_small(A[i:i+d]) for i in range(0, n, d)]    
	pivot = median_of_medians(medians, d)
	return pivot

def quick_select(A, k):
	low, high = 0, len(A)-1

	while True:
		pivot = median_of_medians(A[low:high])

		index = partition(A, low, high, pivot)
		if index == k:
			return A[:k]
		if index < k:
			left = index + 1
		else:
			right = index - 1

size = len(A) + 1
m1 = quick_select(A, size//2)
m2 = quick_select(A, size - size//2)
median = (m1+m2)/2.0

```

Median of medians does not compute the real median. But it does give us something close. A guarantee that the selected pivot will always partition the array *favourably*.

A randomly selected element may end up partitioning the array *unfavourably* (i.e very little or no elements in one of the partitions). The recursion does not help reduce the running time in such a case. But what about the median of medians?


If $S_i$ is the $i^{th}$ segment of array $A$ with $|A|=n$, $|S_i|\geq 5$, $m_i=median(S_i)$, $m=median(m_1,m_2,\dots)$, we can infer that
1. Atleast 2 element in $S_i$ are smaller than $m_i$
2. Atleast half of $m_i$'s are smaller than $m$

Which implies at least $\frac{n/5}{2}\cdot 2=\frac{n}{5}$ elements of $A$ are smaller than $m$. Similarly,  at least $\frac{n}{5}$ elements in $A$ which are greater than $m$. So splitting the array with $m$ as pivot always results in a *favourable* split of the array. 

The run time of median of median procedure is also linear. 
 $$T(n) =  T(n/5)+ n/5 = O(n)$$

So if we use the median of medians for selecting pivot, the worst-case performance of quick select is improved to $O(n \log n)$. 

But then why a magical segment size of $5$? Why not 3? Would a larger number work? Read more [here](https://en.wikipedia.org/wiki/Median_of_medians)


## Median of sorted arrays
What if the numbers are in smaller sorted arrays and we need to find the median of the full list?

Here is the strategy. Given a pivot, we can count numbers smaller than the pivot in each of the sorted arrays using binary search. The smallest number for which this total count is $k$ is the $k^{th}$ smallest number in the whole collection. To find such a number, we can use binary search on the total range of numbers. 

```python
def find_kth(A:List[List[int]], k:int) -> float:
	if len(A)==1: return A[0][k-1]
	
	lo = min(a[0]  for a in A)
	hi = max(a[-1] for a in A)
	
	while lo < hi:
		mid = lo + (hi - lo)//2
        count = 0
		for a in A:
			count += bisect.bisect_right(a, mid)
		if count < k:
			lo = mid + 1
		else:
			hi = mid
	return hi

def median_sorted(A:List[List[int]]) -> float:
	A = [a for a in A if a] # remove all empty arrays
	size = sum(len(a) for a in A) + 1
	m1 = find_kth(A, size//2)
	m2 = find_kth(A, size - size//2)
	return (m1+m2)/2.0
```

The time complexity of this approach is $O(m\log n)$ where $m$ is no of arrays and $n$ is the size of the largest array. 

*To be precise, the time complexity is $O(b\cdot m \log n)$ where $b$ is the total number of bits used to represent the numbers. The difference between `hi` and `lo`  can be as large as $2^{b}$ and we are doing a binary search in that range. So, the number of steps the while loop runs is bounded by $O(b)$. In a realistic scenario, $b$ is always a constant like 32 or 64.* 


## Median with updates
So far we have been talking about arrays of fixed sizes.  What if the array grows over time with insertions? How do you find the median instantaneously? 

Essentially, we have to support 2 operations. `insert` and `find_median`. If insertion is a simple append operation, then finding the median would take $O(n)$ steps. If we always insert while maintaining sorted order which takes $O(n)$ steps, then finding the median would just be a lookup. Can we do better? 

We maintain 2 heaps; a max heap and a min-heap. The max heap always maintains the smaller half of elements while the min-heap maintains the larger half. The roots of both the heaps would be the middle element(s). 


```python
import heapq
L, R = [], []

def insert(num) -> None:
	heapq.heappush(R, num)
	itm = heapq.heappop(R)
	heapq.heappush(L, -itm)
	
	if len(R) < len(L): 
		# invariant: |R|-|L| = 0/1 
		itm = heapq.heappop(L)
		heapq.heappush(R, -itm)
	
def find_median() -> float:
	if len(L) == len(R):
		return (-L[0] + R[0])/2
	return R[0]
```

This scheme incurs a $O(\log n)$ steps for `insert` and $O(1)$ for `find_median`. 
*We do a bit of hack by inserting the negative of an element to simulate a max heap from a min-heap*.

## Median of a distribution
Let's say we have lots of numbers. But most of them are in a small range. How do you compute the median then?

We can store the statistics of the numbers by maintaining their frequencies in the valid range. For the numbers beyond the range, we store only the total counts (one for each end). This allows fast inserts and fast median finding operations. Let's see a sample implementation.  

```python
freq = Counter()
low, high = ?, ? # set the limits here
low_counter, count, high_counter = 0, 0, 0

def insert(num) -> None:
	if num < low:
		low_counter += 1
	elif num > high:
		high_counter += 1
	else:
		freq[num] += 1
		count += 1

def find_kth(k) -> float:
    count = low_counter
	for n in range(low, high+1):
		if count <= k <= (count + freq[n]):
			return n
		count += freq[n]
	return float('nan')

def find_median() -> float:
	size = low_counter + count + high_counter + 1
	m1 = find_kth(size//2)
	m2 = find_kth(size - size//2)
	return (m1 + m2)/2.0
```


Do you know any other weird scenarios where you need median computed? Let me know.