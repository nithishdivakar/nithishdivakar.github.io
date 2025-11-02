---
date: 2024-01-01 00:00:00 +0000
layout: post
slug: 18f
status: done
title: Detecting a Cycle in Linked List
tags:
- linked list
---

## Linked List Cycle [LC#141]
> Given head, the head of a linked list, determine if the linked list has a cycle in it. Return true if there is a cycle in the linked list. Otherwise, return false.

### Floyd's Turtle and hare algorithm
It relies on the fact that if two pointers are moving at different speeds within a cycle, their distances will reach a max length before being reset to zero at which point they will point to the same element. 

### Time complexity
- $T(n) = O(n)$ Will travel initial `n` of non-cyclic then `k` which is cycle length.
- $S(n) = O(n)$

### Code
```python
def has_cycle(head: Optional[ListNode]) -> bool:
    turtle, hare = ListNode(0, head), ListNode(0, head)
    while turtle and hare:
        if turtle == hare:
            return True
        turtle = turtle.next
        hare = hare.next.next if hare.next else None
    return False
```