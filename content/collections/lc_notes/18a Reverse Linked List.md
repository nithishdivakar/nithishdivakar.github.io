---
date: 1000-01-01 00:00:00 +0000
layout: post
slug: 18a
status: done
title: Reverse Linked List
tags:
- linked list
---

## Reverse Linked List [LC#206]
> Given the head of a singly linked list, reverse the list, and return the reversed list.

### Iterative approach


                                             
```
     ┌────┐    ┌────┐    ┌────┐
 <-- │prev│    │curr│--> │next│-->
     └────┘    └────┘    └────┘
     ┌────┐    ┌────┐    ┌────┐
 <-- │prev│ <--│curr│    │next│-->
     └────┘    └────┘    └────┘
     ┌────┐    ┌────┐    ┌────┐
 <-- │    │ <--│prev│    │next│-->
     └────┘    └────┘    └────┘
     ┌────┐    ┌────┐    ┌────┐
 <-- │    │ <--│prev│    |curr│-->
     └────┘    └────┘    └────┘
```


```python
def fn(head):
    curr = head
    prev = None
    while curr:
        next_node = curr.next
        curr.next = prev
        prev = curr
        curr = next_node
    return prev
```
### Time Complexity
- $T(n) = O(n)$
- $S(n) = O(1)$