---
date: 2024-01-01 00:00:00 +0000
layout: post
slug: 18e
status: done
title: Merge K Sorted Lists
tags:
- linked list
---

## Merge k Sorted Lists [LC#23]
> You are given an array of `k` linked-lists lists, each linked-list is sorted in ascending order. Merge all the linked-lists into one sorted linked-list and return it.


**Brute-Force**
- Merge all lists into one and sort the list
- $T(n) = O(n \log n)$ ; $S(n) = O(n)$

**Priority Queue or Min Heap**
- Create a min heap with first values of all the lists
- Repeatedly pop the root of min heap, add to the answer and push the next value of the list where root was from to the heap
- $T(n) = O(k  + n \log k)$ heapify + n pop root
- $S(n) = O(k)$ for the heap

```python
def merge_sorted_lists(lists: List[Optional[ListNode]]) -> Optional[ListNode]:
    class HeapNode:
        def __init__(self, node: ListNode):
            self.node = node
        def __lt__(self, other):
            return self.node.val < other.node.val
    
    heap = []
    current = dummy = ListNode(0)
    for lst in lists:
        if lst:
            heapq.heappush(heap, HeapNode(lst))
    
    while heap:
        node = heapq.heappop(heap).node
        current.next = node
        current = current.next
        if node.next:
            heapq.heappush(heap, HeapNode(node.next))

    return dummy.next
```

**Iterative Mergesort on sorted lists**
- Take 2 pairs of list and sort them together
- Do this iteratively until there is only 1 left
- $T(n) = O(n + n/2 + n/4 + ... +n/k) = O(n \log k)$
- $S(n) = O(1)$