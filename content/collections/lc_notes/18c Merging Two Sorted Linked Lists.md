---
date: 2024-01-01 00:00:00 +0000
layout: post
slug: 18c
status: done
title: Merging Two Sorted Linked Lists
tags:
- linked list
---

## Merge Two Sorted Lists [LC#21]

You are given the heads of two sorted linked lists list1 and list2. Merge the two lists into one sorted list. The list should be made by splicing together the nodes of the first two lists.
Return the head of the merged linked list.
```python
# Definition for singly-linked list.
@dataclass
class ListNode:
    val: int = 0
    next: Optional[ListNode] = None
```

**Iterate and Merge**
- $T(n) = O(m+n)$; $S(n) = O(1)$

```python
def merge_two_sorted_lists(list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
      fake_head = ListNode()
      current = fake_head
      
      while list1 and list2:
          if list1.val < list2.val:
              current.next = list1
              list1 = list1.next
          else:
              current.next = list2
              list2 = list2.next
          current = current.next
      current.next = list1 if list1 else list2
      
      return fake_head.next
```